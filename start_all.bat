@echo off
rem ==========================================
rem Myria System Startup Script V3 (Final Fix)
rem ==========================================

rem --- 設定 ---
set SBV2_PATH=F:\aisisterprogram.1\sshpython\SBV2\Style-Bert-VITS2
rem -----------
rem -----------
rem Port cleanup (Kill process on port 5000 and 8000)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    if not "%%a"=="0" taskkill /F /PID %%a
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    if not "%%a"=="0" taskkill /F /PID %%a
)
rem -----------

echo Starting Project Myria...

rem 1. Start Ollama
echo [1/3] Launching Ollama Brain...
rem Ignore error if already running
start "Myria - Brain (Ollama)" cmd /k "ollama serve"

timeout /t 3 /nobreak >nul

rem 2. Start Style-Bert-VITS2
echo [2/3] Launching Voice Server (SBV2)...
if exist "%SBV2_PATH%" (
    rem Enter virtual environment and run
    start "Myria - Voice (SBV2)" cmd /k "cd /d %SBV2_PATH% && call venv\Scripts\activate.bat && python server_fastapi.py"
) else (
    echo [ERROR] Folder not found! Check settings.
    pause
)

timeout /t 15 /nobreak >nul

rem 3. Start Discord Bot (Body)
echo [3/3] Launching Discord Bot Body...
timeout /t 5 /nobreak >nul

rem Bot Startup (Simplified)
start "Myria - Body (Discord Bot)" cmd /k "call .\.venv\Scripts\activate && python -m src.bot.main"

echo All systems initialized.
pause