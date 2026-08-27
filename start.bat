@echo off
title AI Memory Platform Launcher
color 0A
echo ========================================================
echo       Starting AI Memory Platform (Local / Wi-Fi)
echo ========================================================
echo.

:: 1. Check Ollama
echo [1/3] Checking Ollama AI Service...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Ollama is already running.
) else (
    echo [INFO] Starting Ollama in background...
    start "" /B ollama serve
    timeout /t 3 /nobreak >nul
)

:: 2. Start Backend
echo [2/3] Starting FastAPI Backend on port 8000 ...
start "AI Memory Platform - Backend" cmd /k "cd /d D:\AI-Memory-Platform\backend && ..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: 3. Start Frontend
echo [3/3] Starting Vite Frontend on port 5173 ...
start "AI Memory Platform - Frontend" cmd /k "cd /d D:\AI-Memory-Platform\frontend && npm run dev"

:: Open Browser
echo.
echo ========================================================
echo   Application is running!
echo.
echo   Local PC:    http://localhost:5173
echo   Phone/Wi-Fi: http://10.178.53.165:5173
echo   Backend API: http://127.0.0.1:8000/docs
echo ========================================================
timeout /t 3 /nobreak >nul
start http://localhost:5173
exit
