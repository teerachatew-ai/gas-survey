@echo off
title PNGD Gas Survey Server (SL-FO-014-09)
cd /d "D:\Claude Code\gas-survey"
echo ==============================================================
echo  PNGD Online Survey - SL-FO-014-09
echo  Customer link : http://%COMPUTERNAME%:5000/survey
echo  Back office   : http://%COMPUTERNAME%:5000/admin
echo  (or use this PC's IP address instead of %COMPUTERNAME%)
echo ==============================================================
python app.py
pause
