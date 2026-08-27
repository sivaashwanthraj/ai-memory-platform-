@echo off
setlocal enabledelayedexpansion
title Push AI Memory Platform to GitHub
color 0A
set PATH=D:\AI-Memory-Platform\git\cmd;%PATH%

echo ========================================================
echo         Push AI Memory Platform to GitHub
echo ========================================================
echo.

:: Check if git repo exists
if not exist ".git" (
    echo Initializing Git repository...
    git init
    git branch -M main
)

:: Configure git user if not set
git config user.name >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    git config user.name "AI Memory Developer"
    git config user.email "developer@example.com"
)

echo Adding files...
git add .
git commit -m "Initial commit for 24/7 Cloud Deployment"

echo.
echo ========================================================
echo  Please paste your GitHub Repository URL below
echo  (Example: https://github.com/yourusername/ai-memory-platform.git)
echo ========================================================
set /p REPO_URL="GitHub Repo URL: "

if "%REPO_URL%"=="" (
    echo No URL entered. Aborting.
    pause
    exit /b
)

:: Set remote
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%

echo.
echo Pushing files to GitHub...
git push -u origin main

echo.
echo ========================================================
echo  Upload complete! Check your repository on GitHub.com
echo ========================================================
pause
