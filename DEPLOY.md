# คู่มือ Deploy ขึ้น Render (ฟรี) + Neon Database (ฟรี)

ผลลัพธ์: ได้ลิงก์ `https://pngd-gas-survey.onrender.com/survey` ที่ลูกค้าเปิดจากที่ไหนก็ได้
ข้อมูลเก็บใน Neon Postgres — **ไม่หายแม้เว็บ restart**

---

## ขั้นที่ 1: สร้างฐานข้อมูลฟรีที่ Neon (~3 นาที)

1. ไปที่ **https://neon.tech** → กด **Sign Up** (ล็อกอินด้วย Google ได้)
2. กด **Create a project**
   - Project name: `gas-survey`
   - Region: เลือก **Singapore (ap-southeast-1)** (ใกล้ไทยที่สุด)
3. เมื่อสร้างเสร็จ หน้า Dashboard จะแสดง **Connection string** หน้าตาแบบนี้:
   ```
   postgresql://user:password@ep-xxxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
   ```
4. **คัดลอกเก็บไว้** — จะใช้ในขั้นที่ 3

## ขั้นที่ 2: เอาโค้ดขึ้น GitHub (~5 นาที)

1. สมัคร/ล็อกอิน **https://github.com**
2. กด **New repository** → ตั้งชื่อ `gas-survey` → เลือก **Private** → Create
3. ที่เครื่องนี้ เปิด PowerShell ในโฟลเดอร์ `D:\Claude Code\gas-survey` แล้วรัน:
   ```
   git remote add origin https://github.com/<ชื่อผู้ใช้ของคุณ>/gas-survey.git
   git push -u origin main
   ```
   (git repository ในเครื่องเตรียมไว้ให้แล้ว มี commit พร้อม push)

## ขั้นที่ 3: สร้างเว็บบน Render (~5 นาที)

1. ไปที่ **https://render.com** → Sign Up (ล็อกอินด้วยบัญชี GitHub เลยสะดวกสุด)
2. กด **New → Web Service** → เลือก repo `gas-survey`
3. Render จะอ่าน `render.yaml` อัตโนมัติ ตรวจว่าได้ค่าตามนี้:
   - Runtime: **Python**, Plan: **Free**
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`
4. ในหัวข้อ **Environment Variables** ใส่:
   | Key | Value |
   |---|---|
   | `DATABASE_URL` | connection string จาก Neon (ขั้นที่ 1) |
   | `SURVEY_ADMIN_PASSWORD` | รหัสผ่านหลังบ้านที่ต้องการ (อย่าใช้ค่า default) |
5. กด **Deploy** รอ ~2-3 นาที

## เสร็จแล้ว — ลิงก์ที่ได้

- ฟอร์มลูกค้า: `https://<ชื่อที่ตั้ง>.onrender.com/survey`
- หลังบ้าน: `https://<ชื่อที่ตั้ง>.onrender.com/admin`

## หมายเหตุ

- **แผนฟรีเว็บจะหลับ** เมื่อไม่มีคนใช้ 15 นาที คนแรกที่เปิดรอ ~50 วินาที (ข้อมูลไม่หาย แค่ช้าตอนปลุก)
  - ลดอาการได้โดยตั้ง ping ฟรีที่ https://uptimerobot.com ให้เรียกลิงก์ทุก 10 นาที
- อัปเดตโค้ดครั้งถัดไป: แก้ไฟล์ → `git add -A; git commit -m "..."; git push` → Render deploy ให้เอง
- ฐานข้อมูล Neon ฟรี 0.5 GB — แบบสอบถามหลายหมื่นชุดก็ยังไม่เต็ม
- เครื่องนี้ยังใช้แบบ LAN ได้เหมือนเดิม (`start_server.bat` — ใช้ SQLite ในเครื่อง แยกกับข้อมูลบน Neon)
