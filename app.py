# -*- coding: utf-8 -*-
"""
PNGD SL-FO-014-09 — Online energy-demand questionnaire
- /survey        : customer-facing form (questions identical to the PDF)
- /admin         : back office — list, view, export filled PDF per customer
"""
import base64
import json
import os
import re
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (Flask, g, redirect, render_template, request, send_file,
                   session, url_for, abort, flash)
import io

import anthropic

from pdf_filler import fill_pdf
from pdf_filler_009 import fill_slfo009
from translations import LANGS, make_t, review_i18n

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "survey.db")
os.makedirs(DATA_DIR, exist_ok=True)

# When DATABASE_URL is set (e.g. Neon Postgres on Render) use Postgres,
# otherwise fall back to a local SQLite file.
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
USE_PG = bool(DATABASE_URL)
if USE_PG:
    import psycopg2
    import psycopg2.extras

ADMIN_USER = os.environ.get("SURVEY_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("SURVEY_ADMIN_PASSWORD", "pngd@2026")

app = Flask(__name__)
app.secret_key = os.environ.get("SURVEY_SECRET_KEY", "pngd-sl-fo-014-09-secret")

# ---------------------------------------------------------------- attachments
# Stored as blobs in the database (not local disk) so they survive Render's
# ephemeral filesystem across deploys/restarts.
ALLOWED_ATTACHMENT_MIME = {
    "application/pdf",
    "image/jpeg", "image/png", "image/webp", "image/gif", "image/heic", "image/heif",
}
ALLOWED_ATTACHMENT_EXT = {".pdf", ".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif"}
MAX_ATTACHMENT_BYTES = 10 * 1024 * 1024  # 10 MB per file
app.config["MAX_CONTENT_LENGTH"] = 60 * 1024 * 1024  # generous cap for the whole request

# ---------------------------------------------------------------- database

def get_db():
    if "db" not in g:
        if USE_PG:
            g.db = psycopg2.connect(DATABASE_URL)
        else:
            g.db = sqlite3.connect(DB_PATH)
            g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def db_execute(sql, params=(), fetch=None, returning_id=False):
    """Run a query on either backend. Placeholders in `sql` use '?'.
    fetch: 'all' | 'one' | None. returning_id: return new row id on INSERT."""
    db = get_db()
    if USE_PG:
        sql = sql.replace("?", "%s").replace(" LIKE ", " ILIKE ")
        if returning_id:
            sql += " RETURNING id"
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql, params)
        result = None
        if returning_id:
            result = cur.fetchone()["id"]
        elif fetch == "all":
            result = cur.fetchall()
        elif fetch == "one":
            result = cur.fetchone()
        db.commit()
        cur.close()
        return result
    cur = db.execute(sql, params)
    result = None
    if returning_id:
        result = cur.lastrowid
    elif fetch == "all":
        result = cur.fetchall()
    elif fetch == "one":
        result = cur.fetchone()
    db.commit()
    return result


def init_db():
    if USE_PG:
        conn = psycopg2.connect(DATABASE_URL)
        with conn, conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS submissions (
                    id SERIAL PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    company_name TEXT,
                    contact_person TEXT,
                    email TEXT,
                    data TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS attachments (
                    id SERIAL PRIMARY KEY,
                    submission_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    mimetype TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    data BYTEA NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS iso_documents (
                    id SERIAL PRIMARY KEY,
                    submission_id INTEGER,
                    form_code TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'draft',
                    data TEXT NOT NULL,
                    created_by TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contract_requests (
                    id SERIAL PRIMARY KEY,
                    company_name TEXT,
                    status TEXT NOT NULL DEFAULT 'draft',
                    terms_data TEXT NOT NULL DEFAULT '{}',
                    info_data TEXT NOT NULL DEFAULT '{}',
                    created_by TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contract_documents (
                    id SERIAL PRIMARY KEY,
                    contract_request_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    mimetype TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    data BYTEA NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
        conn.close()
    else:
        with sqlite3.connect(DB_PATH) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    company_name TEXT,
                    contact_person TEXT,
                    email TEXT,
                    data TEXT NOT NULL
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS attachments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    submission_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    mimetype TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    data BLOB NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS iso_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    submission_id INTEGER,
                    form_code TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'draft',
                    data TEXT NOT NULL,
                    created_by TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS contract_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT,
                    status TEXT NOT NULL DEFAULT 'draft',
                    terms_data TEXT NOT NULL DEFAULT '{}',
                    info_data TEXT NOT NULL DEFAULT '{}',
                    created_by TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS contract_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contract_request_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    mimetype TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    data BLOB NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)


init_db()


def _attachment_allowed(fs):
    if not fs or not fs.filename:
        return False
    ext = os.path.splitext(fs.filename)[1].lower()
    if ext not in ALLOWED_ATTACHMENT_EXT:
        return False
    if fs.mimetype and fs.mimetype not in ALLOWED_ATTACHMENT_MIME:
        return False
    return True


def save_attachments(submission_id, category, files):
    """Validate + store uploaded files as blobs. Silently skips anything
    that fails validation — attachments are optional supporting documents,
    not required fields, so a bad file shouldn't block the submission."""
    db = get_db()
    saved = 0
    for fs in files:
        if not _attachment_allowed(fs):
            continue
        blob = fs.read()
        if not blob or len(blob) > MAX_ATTACHMENT_BYTES:
            continue
        filename = os.path.basename(fs.filename)[:200]
        mimetype = fs.mimetype or "application/octet-stream"
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if USE_PG:
            with db.cursor() as cur:
                cur.execute(
                    "INSERT INTO attachments"
                    " (submission_id, category, filename, mimetype, size_bytes, data, created_at)"
                    " VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (submission_id, category, filename, mimetype, len(blob),
                     psycopg2.Binary(blob), created))
            db.commit()
        else:
            db.execute(
                "INSERT INTO attachments"
                " (submission_id, category, filename, mimetype, size_bytes, data, created_at)"
                " VALUES (?,?,?,?,?,?,?)",
                (submission_id, category, filename, mimetype, len(blob), blob, created))
            db.commit()
        saved += 1
    return saved


def list_attachments(submission_id):
    return db_execute(
        "SELECT id, category, filename, mimetype, size_bytes, created_at FROM attachments"
        " WHERE submission_id = ? ORDER BY category, id", (submission_id,), fetch="all")


def get_attachment(aid, submission_id):
    return db_execute(
        "SELECT * FROM attachments WHERE id = ? AND submission_id = ?",
        (aid, submission_id), fetch="one")

# ---------------------------------------------------------------- Existing Customer: contract requests

CONTRACT_DOC_CATEGORIES = [
    ("biz_cert", "สำเนาหนังสือรับรองการจดทะเบียนบริษัท (ไม่เกิน 6 เดือน)"),
    ("poa", "สำเนาหนังสือมอบอำนาจ (กรณีมอบอำนาจ)"),
    ("vat_cert", "สำเนาหนังสือรับรอง ภ.พ.20"),
    ("memorandum", "สำเนาหนังสือบริคณห์สนธิ"),
    ("id_authorized", "สำเนาบัตรประชาชน/พาสปอร์ตผู้มีอำนาจลงนาม"),
    ("id_witness", "สำเนาบัตรประชาชน/พาสปอร์ตพยาน"),
    ("proposal_letter", "หนังสือข้อเสนอเงื่อนไขส่งจ่ายก๊าซฯ"),
    ("land_permit", "สำเนาใบอนุญาตให้ใช้ที่ดิน/หนังสือยินยอมใช้สถานที่"),
]
CONTRACT_DOC_CATEGORY_KEYS = [c[0] for c in CONTRACT_DOC_CATEGORIES]
# Which of the checklist categories are worth sending to OCR — legal identity
# documents that carry the company/person data the form asks for.
CONTRACT_DOC_OCR_CATEGORIES = {"biz_cert", "vat_cert", "memorandum", "id_authorized", "id_witness"}

CONTRACT_INFO_TEXT_FIELDS = [
    "company_name_th", "company_name_en", "tel", "fax", "industrial_estate",
    "address_cert_th", "address_cert_en", "address_vat_th", "address_vat_en",
    "address_factory_th", "address_factory_en", "address_invoice_th", "address_invoice_en",
    "authorized_name_1", "authorized_name_2", "authorized_position",
    "witness_name_1", "witness_name_2", "witness_position",
    "contact_person", "contact_mobile", "remark",
]
CONTRACT_INFO_MULTI_FIELDS = ["doc_purpose", "contract_lang"]
CONTRACT_INFO_BOOL_FIELDS = [f"doc_{k}" for k in CONTRACT_DOC_CATEGORY_KEYS]
# Fields OCR is allowed to propose values for (kept separate from the full
# field list since OCR should never touch contact_person/remark etc.)
CONTRACT_INFO_OCR_FIELDS = [
    "company_name_th", "company_name_en", "industrial_estate",
    "address_cert_th", "address_cert_en", "address_vat_th", "address_vat_en",
    "authorized_name_1", "authorized_name_2", "authorized_position",
    "witness_name_1", "witness_name_2", "witness_position",
]


def collect_contract_info_form(form):
    data = {}
    for f in CONTRACT_INFO_TEXT_FIELDS:
        data[f] = form.get(f, "").strip()
    for f in CONTRACT_INFO_MULTI_FIELDS:
        data[f] = form.getlist(f)
    for f in CONTRACT_INFO_BOOL_FIELDS:
        data[f] = bool(form.get(f))
    return data


def list_contract_requests():
    return db_execute("SELECT * FROM contract_requests ORDER BY id DESC", fetch="all")


def _load_contract_request(cid):
    row = db_execute("SELECT * FROM contract_requests WHERE id = ?", (cid,), fetch="one")
    if row is None:
        abort(404)
    return row, json.loads(row["info_data"] or "{}")


def save_contract_documents(contract_id, category, files):
    db = get_db()
    saved = 0
    for fs in files:
        if not _attachment_allowed(fs):
            continue
        blob = fs.read()
        if not blob or len(blob) > MAX_ATTACHMENT_BYTES:
            continue
        filename = os.path.basename(fs.filename)[:200]
        mimetype = fs.mimetype or "application/octet-stream"
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if USE_PG:
            with db.cursor() as cur:
                cur.execute(
                    "INSERT INTO contract_documents"
                    " (contract_request_id, category, filename, mimetype, size_bytes, data, created_at)"
                    " VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (contract_id, category, filename, mimetype, len(blob),
                     psycopg2.Binary(blob), created))
            db.commit()
        else:
            db.execute(
                "INSERT INTO contract_documents"
                " (contract_request_id, category, filename, mimetype, size_bytes, data, created_at)"
                " VALUES (?,?,?,?,?,?,?)",
                (contract_id, category, filename, mimetype, len(blob), blob, created))
            db.commit()
        saved += 1
    return saved


def list_contract_documents(contract_id):
    return db_execute(
        "SELECT id, category, filename, mimetype, size_bytes, created_at FROM contract_documents"
        " WHERE contract_request_id = ? ORDER BY category, id", (contract_id,), fetch="all")


def get_contract_document(doc_id, contract_id):
    return db_execute(
        "SELECT * FROM contract_documents WHERE id = ? AND contract_request_id = ?",
        (doc_id, contract_id), fetch="one")


OCR_MODEL = "claude-sonnet-5"
OCR_MAX_DOCS = 6


def _contract_ocr_documents(contract_id):
    return db_execute(
        "SELECT category, filename, mimetype, data FROM contract_documents"
        " WHERE contract_request_id = ? ORDER BY id", (contract_id,), fetch="all")


def ocr_fill_contract_info(contract_id):
    """Read the legal documents attached to a contract request (company cert,
    VAT cert, ID cards, ...) and use Claude's vision to propose values for the
    blank fields of the customer info form. Only fills fields that are
    currently empty — never overwrites something staff already typed."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("ยังไม่ได้ตั้งค่า ANTHROPIC_API_KEY บนเซิร์ฟเวอร์")

    docs = [d for d in _contract_ocr_documents(contract_id)
            if d["category"] in CONTRACT_DOC_OCR_CATEGORIES]
    if not docs:
        raise RuntimeError("ยังไม่มีเอกสารที่อ่านได้ — กรุณาแนบไฟล์ก่อน (หนังสือรับรอง/ภ.พ.20/บัตรประชาชน)")

    content = [{
        "type": "text",
        "text": (
            "You are reading Thai company legal documents (business registration "
            "certificate, VAT registration certificate ภ.พ.20, memorandum of "
            "association, national ID cards / passports of authorized signatories "
            "and witnesses) for a natural gas supply contract renewal.\n"
            "Extract the following fields and return ONLY a single JSON object "
            "(no markdown fences, no commentary) with exactly these keys: "
            + json.dumps(CONTRACT_INFO_OCR_FIELDS) + "\n"
            "Rules: company_name_th/company_name_en are the registered company "
            "name in Thai/English. address_cert_th/en is the registered address "
            "on the business registration certificate. address_vat_th/en is the "
            "address on the VAT (ภ.พ.20) certificate. authorized_name_1/2 are "
            "the authorized signatories' full names, authorized_position is "
            "their position/title. witness_name_1/2 and witness_position are "
            "for any witnesses if identifiable, otherwise leave blank. Use an "
            "empty string for any field you cannot find with confidence — "
            "never guess."
        ),
    }]
    for d in docs[:OCR_MAX_DOCS]:
        blob = bytes(d["data"])
        b64 = base64.b64encode(blob).decode("ascii")
        if d["mimetype"] == "application/pdf":
            content.append({"type": "document",
                            "source": {"type": "base64", "media_type": "application/pdf", "data": b64}})
        else:
            content.append({"type": "image",
                            "source": {"type": "base64", "media_type": d["mimetype"], "data": b64}})

    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=OCR_MODEL, max_tokens=1024,
        messages=[{"role": "user", "content": content}])
    raw = "".join(block.text for block in resp.content if block.type == "text").strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        extracted = json.loads(raw)
    except ValueError:
        raise RuntimeError("โมเดลตอบกลับมาไม่เป็น JSON ที่อ่านได้ — ลองใหม่อีกครั้ง")

    _row, data = _load_contract_request(contract_id)
    filled = 0
    for key in CONTRACT_INFO_OCR_FIELDS:
        value = (extracted.get(key) or "").strip()
        if value and not (data.get(key) or "").strip():
            data[key] = value
            filled += 1
    if filled:
        db_execute(
            "UPDATE contract_requests SET info_data = ?, updated_at = ? WHERE id = ?",
            (json.dumps(data, ensure_ascii=False),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"), contract_id))
    return filled

# ---------------------------------------------------------------- form fields

TEXT_FIELDS = [
    "inquiry_other", "company_name", "address", "contact_person", "email",
    "nationality", "business_type", "mobile", "tel", "fax",
    "plant_location", "land_plot", "steam_pressure", "purpose_other",
    "ng_supply_date", "ng_pressure",
    "product_current", "product_expansion", "startup_current", "startup_expansion",
    "ophour_current", "ophour_expansion", "opday_current", "opday_expansion",
    "elec_base", "elec_peak", "elec_offpeak",
    "pea_kv", "mea_kv", "self_mw", "self_method", "elec_source_other",
    "chiller_avg", "chiller_base",
    "pdpa_name", "pdpa_title",
]
for _n in (1, 2, 3):
    TEXT_FIELDS += [f"fuel{_n}_type_other", f"fuel{_n}_unit_other"]
    TEXT_FIELDS += [f"chiller{_n}_rt", f"chiller{_n}_type", f"chiller{_n}_cop"]
for _r in range(1, 13):
    TEXT_FIELDS.append(f"month_label_{_r}")
    for _n in (1, 2, 3):
        TEXT_FIELDS += [f"fuel{_n}_cons_{_r}", f"fuel{_n}_price_{_r}"]
for _y in range(1, 8):
    TEXT_FIELDS += [f"year_{_y}", f"cons_year_{_y}", f"cap_year_{_y}"]
for _m in range(1, 5):
    TEXT_FIELDS += [f"machine{_m}_type", f"machine{_m}_capacity", f"machine{_m}_ophour",
                    f"machine{_m}_days", f"machine{_m}_character", f"machine{_m}_qty"]

RADIO_FIELDS = ["inquiry_method", "fuel1_type", "fuel2_type", "fuel3_type",
                "fuel1_grade", "fuel2_grade", "fuel3_grade",
                "fuel1_unit", "fuel2_unit", "fuel3_unit"]
MULTI_FIELDS = ["purpose", "elec_source"]
BOOL_FIELDS = ["elec_bill", "elec_profile", "chiller_profile", "pdpa_accept"]
STAFF_FIELDS = ["staff_factory", "staff_received_date", "staff_recorded_date",
                "staff_revision", "staff_recorder"]

# ---------------------------------------------------------------- ISO E-Document: SL-FO-009

ISO009_TEXT_FIELDS = [
    "company_name", "area", "project_no", "revision_no", "form_date",
    "land_plot_address", "pipe_distance_m", "surveyor_name", "surveyor_date",
    "commissioning_date", "gas_consumption_mmbtu_yr",
]
for _r in (1, 2, 3):
    ISO009_TEXT_FIELDS += [f"mrs{_r}_pressure", f"mrs{_r}_max_flow"]
    for _y in range(1, 16):
        ISO009_TEXT_FIELDS.append(f"mrs{_r}_year{_y}")

ISO009_RADIO_FIELDS = ["factory_type", "pipe_within_500m", "gas_heating_zone",
                        "estimate_scope", "connection_type"]
ISO009_MULTI_FIELDS = ["purpose"]
ISO009_BOOL_FIELDS = ["attach_hardcopy", "attach_electronic", "attach_potential_demand"]


def collect_iso009_form(form):
    data = {}
    for f in ISO009_TEXT_FIELDS + ISO009_RADIO_FIELDS:
        data[f] = form.get(f, "").strip()
    for f in ISO009_MULTI_FIELDS:
        data[f] = form.getlist(f)
    for f in ISO009_BOOL_FIELDS:
        data[f] = bool(form.get(f))
    return data


def slfo009_autofill(survey_data):
    """Pre-fill SL-FO-009 fields from an existing Energy Survey (SL-FO-014)
    submission, so the surveyor only types what's genuinely new."""
    data = {f: "" for f in ISO009_TEXT_FIELDS + ISO009_RADIO_FIELDS}
    for f in ISO009_MULTI_FIELDS:
        data[f] = []
    for f in ISO009_BOOL_FIELDS:
        data[f] = False

    data["company_name"] = survey_data.get("company_name", "")
    data["form_date"] = datetime.now().strftime("%d/%m/%Y")
    data["surveyor_date"] = datetime.now().strftime("%d/%m/%Y")

    location = survey_data.get("plant_location", "").strip()
    land_plot = survey_data.get("land_plot", "").strip()
    if location and land_plot:
        data["land_plot_address"] = f"{location} — แปลงที่ {land_plot}"
    else:
        data["land_plot_address"] = location or land_plot

    data["commissioning_date"] = survey_data.get("ng_supply_date", "")
    data["gas_consumption_mmbtu_yr"] = survey_data.get("cons_year_1", "")
    for y in range(1, 8):
        data[f"mrs1_year{y}"] = survey_data.get(f"cap_year_{y}", "")
    return data


def list_iso_documents(submission_id=None):
    if submission_id is not None:
        return db_execute(
            "SELECT * FROM iso_documents WHERE submission_id = ? ORDER BY id DESC",
            (submission_id,), fetch="all")
    return db_execute("SELECT * FROM iso_documents ORDER BY id DESC", fetch="all")


def _load_iso_document(doc_id):
    row = db_execute("SELECT * FROM iso_documents WHERE id = ?", (doc_id,), fetch="one")
    if row is None:
        abort(404)
    return row, json.loads(row["data"])


def collect_form(form):
    data = {}
    for f in TEXT_FIELDS + RADIO_FIELDS:
        data[f] = form.get(f, "").strip()
    for f in MULTI_FIELDS:
        data[f] = form.getlist(f)
    for f in BOOL_FIELDS:
        data[f] = bool(form.get(f))
    data["form_date"] = datetime.now().strftime("%d/%m/%Y")
    return data

# ---------------------------------------------------------------- language

@app.before_request
def pick_language():
    lang = request.args.get("lang")
    if lang in LANGS:
        session["lang"] = lang


@app.context_processor
def inject_translator():
    lang = session.get("lang", "th")
    has_logo = os.path.exists(os.path.join(BASE_DIR, "static", "logo.png"))
    return {"t": make_t(lang), "lang": lang, "review_i18n": review_i18n(lang),
            "has_logo": has_logo}


def tr(key):
    return make_t(session.get("lang", "th"))(key)


# ---------------------------------------------------------------- customer

@app.route("/")
def index():
    return redirect(url_for("survey"))


@app.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        data = collect_form(request.form)
        if not data["company_name"]:
            flash(tr("flash_company"))
            return render_template("survey.html", data=data), 400
        if not data["pdpa_accept"]:
            flash(tr("flash_consent"))
            return render_template("survey.html", data=data), 400
        new_id = db_execute(
            "INSERT INTO submissions (created_at, company_name, contact_person, email, data)"
            " VALUES (?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             data["company_name"], data["contact_person"], data["email"],
             json.dumps(data, ensure_ascii=False)),
            returning_id=True)
        save_attachments(new_id, "fuel", request.files.getlist("fuel_attachments"))
        save_attachments(new_id, "machine", request.files.getlist("machine_attachments"))
        return redirect(url_for("thanks", ref=new_id))
    return render_template("survey.html", data={})


@app.route("/thanks")
def thanks():
    return render_template("thanks.html", ref=request.args.get("ref", ""))

# ---------------------------------------------------------------- admin

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        if (request.form.get("username") == ADMIN_USER
                and request.form.get("password") == ADMIN_PASSWORD):
            session["admin"] = True
            return redirect(request.args.get("next") or url_for("admin_home"))
        error = "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/home")
@login_required
def admin_home():
    return render_template("admin_home.html")


@app.route("/admin")
@login_required
def admin_list():
    q = request.args.get("q", "").strip()
    if q:
        rows = db_execute(
            "SELECT id, created_at, company_name, contact_person, email, data FROM submissions"
            " WHERE company_name LIKE ? OR contact_person LIKE ? OR email LIKE ?"
            " ORDER BY id DESC", (f"%{q}%", f"%{q}%", f"%{q}%"), fetch="all")
    else:
        rows = db_execute(
            "SELECT id, created_at, company_name, contact_person, email, data FROM submissions"
            " ORDER BY id DESC", fetch="all")
    counts = db_execute(
        "SELECT submission_id, COUNT(*) AS cnt FROM attachments GROUP BY submission_id",
        fetch="all")
    count_map = {c["submission_id"]: c["cnt"] for c in counts}
    items = []
    for r in rows:
        d = json.loads(r["data"])
        items.append({"id": r["id"], "created_at": r["created_at"],
                      "company_name": r["company_name"],
                      "contact_person": r["contact_person"], "email": r["email"],
                      "pdpa": bool(d.get("pdpa_accept")),
                      "attachments": count_map.get(r["id"], 0)})
    return render_template("admin_list.html", rows=items, q=q)


def _load_submission(sid):
    row = db_execute("SELECT * FROM submissions WHERE id = ?", (sid,), fetch="one")
    if row is None:
        abort(404)
    return row, json.loads(row["data"])


@app.route("/admin/<int:sid>")
@login_required
def admin_view(sid):
    row, data = _load_submission(sid)
    attachments = list_attachments(sid)
    fuel_files = [a for a in attachments if a["category"] == "fuel"]
    machine_files = [a for a in attachments if a["category"] == "machine"]
    iso_docs = list_iso_documents(sid)
    return render_template("admin_view.html", row=row, d=data,
                           fuel_files=fuel_files, machine_files=machine_files,
                           iso_docs=iso_docs)


@app.route("/admin/<int:sid>/attachment/<int:aid>")
@login_required
def admin_attachment(sid, aid):
    row = get_attachment(aid, sid)
    if row is None:
        abort(404)
    blob = bytes(row["data"])
    return send_file(io.BytesIO(blob), mimetype=row["mimetype"],
                     as_attachment=bool(request.args.get("download")),
                     download_name=row["filename"])

# ---------------------------------------------------------------- ISO E-Document

@app.route("/admin/iso")
@login_required
def admin_iso_list():
    rows = list_iso_documents()
    items = [{"id": r["id"], "form_code": r["form_code"], "status": r["status"],
             "created_at": r["created_at"], "updated_at": r["updated_at"],
             "company_name": json.loads(r["data"]).get("company_name", "-"),
             "submission_id": r["submission_id"]}
            for r in rows]
    return render_template("admin_iso_list.html", rows=items)


@app.route("/admin/<int:sid>/iso/new", methods=["POST"])
@login_required
def admin_iso_new(sid):
    _row, survey_data = _load_submission(sid)
    form_code = request.form.get("form_code", "SL-FO-009")
    data = slfo009_autofill(survey_data)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    doc_id = db_execute(
        "INSERT INTO iso_documents (submission_id, form_code, status, data, created_by, created_at, updated_at)"
        " VALUES (?, ?, 'draft', ?, ?, ?, ?)",
        (sid, form_code, json.dumps(data, ensure_ascii=False), "", now, now),
        returning_id=True)
    return redirect(url_for("admin_iso_edit", doc_id=doc_id))


@app.route("/admin/iso/<int:doc_id>", methods=["GET", "POST"])
@login_required
def admin_iso_edit(doc_id):
    row, data = _load_iso_document(doc_id)
    if request.method == "POST":
        new_data = collect_iso009_form(request.form)
        new_data["company_name"] = data.get("company_name", "")  # not user-editable here
        db_execute(
            "UPDATE iso_documents SET data = ?, status = ?, updated_at = ? WHERE id = ?",
            (json.dumps(new_data, ensure_ascii=False),
             "completed" if request.form.get("mark_completed") else row["status"],
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"), doc_id))
        flash("บันทึกข้อมูลแล้ว")
        return redirect(url_for("admin_iso_edit", doc_id=doc_id))
    return render_template("admin_iso009_form.html", row=row, d=data)


@app.route("/admin/iso/<int:doc_id>/pdf")
@login_required
def admin_iso_pdf(doc_id):
    row, data = _load_iso_document(doc_id)
    pdf_bytes = fill_slfo009(data)
    company = re.sub(r"[^0-9A-Za-zก-๙ _.-]+", "", data.get("company_name") or "customer")[:60]
    fname = f"SL-FO-009-19_{doc_id:04d}_{company or 'customer'}.pdf"
    return send_file(io.BytesIO(pdf_bytes), mimetype="application/pdf",
                     as_attachment=bool(request.args.get("download")),
                     download_name=fname)


@app.route("/admin/iso/<int:doc_id>/delete", methods=["POST"])
@login_required
def admin_iso_delete(doc_id):
    row, _data = _load_iso_document(doc_id)
    sid = row["submission_id"]
    db_execute("DELETE FROM iso_documents WHERE id = ?", (doc_id,))
    flash(f"ลบเอกสาร ISO #{doc_id} แล้ว")
    if request.form.get("next") == "list":
        return redirect(url_for("admin_iso_list"))
    return redirect(url_for("admin_view", sid=sid) if sid else url_for("admin_iso_list"))

# ---------------------------------------------------------------- Existing Customer: contract requests

@app.route("/admin/contracts")
@login_required
def admin_contracts_list():
    rows = list_contract_requests()
    return render_template("admin_contracts_list.html", rows=rows)


@app.route("/admin/contracts/new", methods=["POST"])
@login_required
def admin_contract_new():
    company_name = request.form.get("company_name", "").strip()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info_data = {f: "" for f in CONTRACT_INFO_TEXT_FIELDS}
    for f in CONTRACT_INFO_MULTI_FIELDS:
        info_data[f] = []
    for f in CONTRACT_INFO_BOOL_FIELDS:
        info_data[f] = False
    cid = db_execute(
        "INSERT INTO contract_requests (company_name, status, terms_data, info_data, created_at, updated_at)"
        " VALUES (?, 'draft', '{}', ?, ?, ?)",
        (company_name, json.dumps(info_data, ensure_ascii=False), now, now),
        returning_id=True)
    return redirect(url_for("admin_contract_view", cid=cid))


@app.route("/admin/contracts/<int:cid>")
@login_required
def admin_contract_view(cid):
    row, data = _load_contract_request(cid)
    docs = list_contract_documents(cid)
    return render_template("admin_contract_view.html", row=row, d=data, docs=docs)


@app.route("/admin/contracts/<int:cid>/delete", methods=["POST"])
@login_required
def admin_contract_delete(cid):
    db_execute("DELETE FROM contract_documents WHERE contract_request_id = ?", (cid,))
    db_execute("DELETE FROM contract_requests WHERE id = ?", (cid,))
    flash(f"ลบคำขอต่อสัญญา #{cid} แล้ว")
    return redirect(url_for("admin_contracts_list"))


@app.route("/admin/contracts/<int:cid>/info", methods=["GET", "POST"])
@login_required
def admin_contract_info(cid):
    row, data = _load_contract_request(cid)
    if request.method == "POST":
        new_data = collect_contract_info_form(request.form)
        db_execute(
            "UPDATE contract_requests SET company_name = ?, info_data = ?, updated_at = ? WHERE id = ?",
            (new_data.get("company_name_th") or row["company_name"],
             json.dumps(new_data, ensure_ascii=False),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cid))
        for key, _label in CONTRACT_DOC_CATEGORIES:
            save_contract_documents(cid, key, request.files.getlist(f"doc_{key}_files"))
        flash("บันทึกข้อมูลแล้ว")
        return redirect(url_for("admin_contract_info", cid=cid))
    docs = list_contract_documents(cid)
    docs_by_cat = {}
    for doc in docs:
        docs_by_cat.setdefault(doc["category"], []).append(doc)
    return render_template("admin_contract_info_form.html", row=row, d=data,
                           categories=CONTRACT_DOC_CATEGORIES, docs_by_cat=docs_by_cat)


@app.route("/admin/contracts/<int:cid>/info/ocr", methods=["POST"])
@login_required
def admin_contract_ocr(cid):
    _load_contract_request(cid)  # 404s if missing
    try:
        filled = ocr_fill_contract_info(cid)
    except Exception as e:
        flash(f"อ่านข้อมูลอัตโนมัติไม่สำเร็จ: {e}")
    else:
        flash(f"อ่านข้อมูลอัตโนมัติสำเร็จ — เติมข้อมูลให้ {filled} ช่อง (ตรวจสอบและแก้ไขได้ตามจริง)"
              if filled else "อ่านเอกสารแล้ว แต่ไม่พบข้อมูลใหม่ที่มั่นใจพอจะเติมให้อัตโนมัติ")
    return redirect(url_for("admin_contract_info", cid=cid))


@app.route("/admin/contracts/<int:cid>/documents/<int:doc_id>")
@login_required
def admin_contract_document(cid, doc_id):
    row = get_contract_document(doc_id, cid)
    if row is None:
        abort(404)
    blob = bytes(row["data"])
    return send_file(io.BytesIO(blob), mimetype=row["mimetype"],
                     as_attachment=bool(request.args.get("download")),
                     download_name=row["filename"])


@app.route("/admin/contracts/<int:cid>/documents/<int:doc_id>/delete", methods=["POST"])
@login_required
def admin_contract_document_delete(cid, doc_id):
    db_execute("DELETE FROM contract_documents WHERE id = ? AND contract_request_id = ?", (doc_id, cid))
    flash("ลบไฟล์แนบแล้ว")
    return redirect(url_for("admin_contract_info", cid=cid))


@app.route("/admin/<int:sid>/staff", methods=["POST"])
@login_required
def admin_staff(sid):
    row, data = _load_submission(sid)
    for f in STAFF_FIELDS:
        data[f] = request.form.get(f, "").strip()
    db_execute("UPDATE submissions SET data = ? WHERE id = ?",
               (json.dumps(data, ensure_ascii=False), sid))
    flash("บันทึกข้อมูลส่วนเจ้าหน้าที่แล้ว")
    return redirect(url_for("admin_view", sid=sid))


@app.route("/admin/<int:sid>/pdf")
@login_required
def admin_pdf(sid):
    row, data = _load_submission(sid)
    pdf_bytes = fill_pdf(data)
    company = re.sub(r"[^0-9A-Za-zก-๙ _.-]+", "", row["company_name"] or "customer")[:60]
    fname = f"SL-FO-014-09_{sid:04d}_{company or 'customer'}.pdf"
    return send_file(io.BytesIO(pdf_bytes), mimetype="application/pdf",
                     as_attachment=bool(request.args.get("download")),
                     download_name=fname)


@app.route("/admin/<int:sid>/delete", methods=["POST"])
@login_required
def admin_delete(sid):
    db_execute("DELETE FROM attachments WHERE submission_id = ?", (sid,))
    db_execute("DELETE FROM iso_documents WHERE submission_id = ?", (sid,))
    db_execute("DELETE FROM submissions WHERE id = ?", (sid,))
    flash(f"ลบรายการ #{sid} แล้ว")
    return redirect(url_for("admin_list"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
