# -*- coding: utf-8 -*-
"""
PNGD SL-FO-014-09 — Online energy-demand questionnaire
- /survey        : customer-facing form (questions identical to the PDF)
- /admin         : back office — list, view, export filled PDF per customer
"""
import json
import os
import re
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (Flask, g, redirect, render_template, request, send_file,
                   session, url_for, abort, flash)
import io

from pdf_filler import fill_pdf
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
            return redirect(request.args.get("next") or url_for("admin_list"))
        error = "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


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
    return render_template("admin_view.html", row=row, d=data,
                           fuel_files=fuel_files, machine_files=machine_files)


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
    db_execute("DELETE FROM submissions WHERE id = ?", (sid,))
    flash(f"ลบรายการ #{sid} แล้ว")
    return redirect(url_for("admin_list"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
