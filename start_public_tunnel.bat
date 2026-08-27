@echo off
title AI Memory Platform - Public Tunnel Launcher
color 0B
echo ========================================================
echo   Starting AI Memory Platform with Free Direct Public Link
echo   (No Cloud Accounts, No Cloud Databases Needed)
echo ========================================================
echo.

:: 1. Check Ollama
echo [1/4] Checking Ollama AI Service...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Ollama is already running.
) else (
    echo [INFO] Starting Ollama in background...
    start "" /B ollama serve
    timeout /t 3 /nobreak >nul
)

:: 2. Start Backend
echo [2/4] Starting FastAPI Backend...
start "AI Memory Platform - Backend" cmd /k "cd /d D:\AI-Memory-Platform\backend && ..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: 3. Start Frontend
echo [3/4] Starting Frontend Server...
start "AI Memory Platform - Frontend" cmd /k "cd /d D:\AI-Memory-Platform\frontend && npm run dev"

:: 4. Start Public Tunnel
echo [4/4] Generating your direct Public HTTPS URL...
timeout /t 4 /nobreak >nul
echo.
echo ========================================================
echo   Your direct public tunnel is starting below!
echo   Share or open the generated URL on your phone or any device.
echo ========================================================
echo.
npx --yes localtunnel --port 5173
pause
