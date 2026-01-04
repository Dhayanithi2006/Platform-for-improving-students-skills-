@echo off
title SkillTwin - React Frontend & Backend Launcher
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    SKILLTWIN PLATFORM                          ║
echo ║              React Frontend & Backend Launcher                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📋 SYSTEM CHECK...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
) else (
    echo ✅ Python installed
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
) else (
    echo ✅ Node.js installed
)

echo.
echo 🚀 STARTING SKILLTWIN PLATFORM...
echo.

REM Start Backend
echo 📡 Starting Flask Backend Server...
cd "c:\Users\Dhayanithi M U\OneDrive\Documents\Hackathon\Skill Twin\Platform-for-improving-students-skills-\backend"
start "SkillTwin Backend" cmd /k "echo 📍 Flask Backend: http://127.0.0.1:5000 && python app.py"

timeout /t 3 /nobreak >nul

REM Start React Frontend
echo ⚛️ Starting React Frontend...
cd "c:\Users\Dhayanithi M U\OneDrive\Documents\Hackathon\Skill Twin\Platform-for-improving-students-skills-\frontend"
start "SkillTwin React" cmd /k "echo 📍 React Frontend: http://0.0.0.0:3000 && npm start"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 SKILLTWIN READY!                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📌 ACCESS URLs:
echo    • React Frontend: http://0.0.0.0:3000 (Multi-Device)
echo    • React Local: http://localhost:3000
echo    • React Network: http://10.10.4.83:3000
echo    • Flask API: http://127.0.0.1:5000/api
echo.
echo 🔐 DEMO CREDENTIALS:
echo    • Email: demo@skilltwin.com
echo    • Password: demo123
echo.
echo 🎯 FEATURES:
echo    • ✅ Complete Authentication System
echo    • ✅ Student Performance Dashboard
echo    • ✅ Adaptive Testing Engine
echo    • ✅ Paper Analysis with ML
echo    • ✅ Learning Recommendations
echo    • ✅ Secure Exam Environment
echo    • ✅ Multi-Device Network Access
echo    • ✅ Production Deployment Ready
echo.
echo 📚 DOCUMENTATION:
echo    • README.md - Complete setup guide
echo.
echo 🚀 Backend and React servers are running in separate windows.
echo    Close this window to keep servers running.
echo.

REM Open browsers
start http://localhost:3000
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000

echo.
echo 🌐 Opening React application in default browser...
echo.
echo Press any key to exit this launcher (servers will continue running)...
pause >nul
