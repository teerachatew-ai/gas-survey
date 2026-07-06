@echo off
REM เปิด Windows Firewall ให้เครื่องอื่นในเครือข่ายเข้าถึงแบบสอบถามที่ port 5000
REM คลิกขวาไฟล์นี้ แล้วเลือก "Run as administrator"
netsh advfirewall firewall add rule name="PNGD Gas Survey (TCP 5000)" dir=in action=allow protocol=TCP localport=5000 profile=domain,private
echo.
echo เพิ่ม rule เรียบร้อย - เครื่องอื่นเปิดลิงก์ http://10.236.44.53:5000/survey ได้แล้ว
pause
