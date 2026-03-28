@echo off
REM Virtual Try-On Application Launcher
echo ========================================
echo    Virtual Try-On Application
echo ========================================
echo.
echo Starting the application...
echo The browser will open automatically at http://localhost:7860
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd /d "%~dp0"
python app.py

pause
