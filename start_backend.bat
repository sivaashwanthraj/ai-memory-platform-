@echo off
title AI Memory Platform - Backend
color 0B
echo Starting FastAPI Backend...
cd /d "D:\AI-Memory-Platform\backend"
"..\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
