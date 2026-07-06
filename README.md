# ระบบแบบสอบถามความต้องการใช้พลังงานออนไลน์ (PNGD SL-FO-014-09)

แปลงแบบฟอร์ม `PNGD_SL-FO-014_09_แบบสอบถามความต้องการใช้พลังงาน.pdf` เป็น online survey
พร้อมระบบหลังบ้าน และ export คำตอบกลับลงไฟล์ PDF ต้นฉบับ (ตำแหน่งตรงตามฟอร์มจริง)

## การใช้งาน

1. ดับเบิลคลิก `start_server.bat` (หรือรัน `python app.py`)
2. **ลิงก์สำหรับลูกค้า**: `http://<IP-เครื่องนี้>:5000/survey`
   - เช่น `http://10.236.44.53:5000/survey` (LAN บริษัท)
3. **ระบบหลังบ้าน**: `http://<IP-เครื่องนี้>:5000/admin`
   - Username: `admin`  Password: `pngd@2026`
   - เปลี่ยนได้ผ่าน environment variable `SURVEY_ADMIN_USER` / `SURVEY_ADMIN_PASSWORD`

## ระบบหลังบ้านทำอะไรได้

- ดูรายการแบบสอบถามทั้งหมดที่ลูกค้าส่งเข้ามา + ค้นหา (บริษัท/ผู้ติดต่อ/อีเมล)
- เปิดดูรายละเอียดคำตอบรายลูกค้า
- กรอกส่วน "เฉพาะเจ้าหน้าที่" (Existing/New Factory, วันที่รับ/บันทึกข้อมูล, Revision, ผู้บันทึก)
- พรีวิว / ดาวน์โหลด PDF ที่เติมคำตอบลงบนแบบฟอร์มต้นฉบับ SL-FO-014-09
- ลบรายการ

## ไฟล์สำคัญ

| ไฟล์ | หน้าที่ |
|---|---|
| `app.py` | เว็บแอป Flask (ฟอร์ม + หลังบ้าน) |
| `pdf_filler.py` | เติมคำตอบลง PDF ต้นฉบับ (พิกัดวัดจาก text layer ของฟอร์มจริง) |
| `original_form.pdf` | แบบฟอร์มต้นฉบับจาก network share |
| `data/survey.db` | ฐานข้อมูล SQLite เก็บคำตอบ |
| `templates/`, `static/` | หน้าเว็บ |
| `test_fill.py`, `test_e2e.py` | สคริปต์ทดสอบ (ใช้ตอนพัฒนา) |

## ติดตั้งบนเครื่องอื่น

```
pip install -r requirements.txt
python app.py
```
ต้องมีฟอนต์ไทย (Tahoma / Leelawadee UI — มีใน Windows อยู่แล้ว)

หมายเหตุ: หากฟอร์มต้นฉบับมีการปรับ revision ใหม่ ให้แทนที่ `original_form.pdf`
แล้วตรวจตำแหน่งด้วย `test_fill.py` (พิกัดใน `pdf_filler.py` อิงกับ revision 09)
