@echo off
title SkillTwin - Public Access with ngrok
color 0E

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║          SKILLTWIN PUBLIC ACCESS - NGROK SETUP              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🌐 Setting up public access for SkillTwin...
echo.

echo 📋 Prerequisites:
echo    • SkillTwin servers running
echo    • Internet connection
echo    • ngrok installed (or will download)
echo.

echo 🔍 Checking if ngrok is installed...
where ngrok >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ ngrok not found. Downloading...
    echo.
    echo 📥 Downloading ngrok...
    powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/b4jInx9Mwtjk/ngrok-stable-windows-amd64.zip' -OutFile 'ngrok.zip'"
    echo.
    echo 📦 Extracting ngrok...
    powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"
    echo ✅ ngrok installed successfully!
    del ngrok.zip
) else (
    echo ✅ ngrok already installed!
)

echo.
echo 🚀 Starting public access tunnel...
echo.

echo 📡 Creating tunnel for React frontend (port 3000)...
start "SkillTwin Frontend - Public" cmd /k "ngrok http 3000"

echo.
echo 📡 Creating tunnel for Backend API (port 5000)...
start "SkillTwin Backend - Public" cmd /k "ngrok http 5000"

echo.
echo ⏳ Waiting for tunnels to establish...
timeout /t 10 /nobreak >nul

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🌐 PUBLIC URLS READY!                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📱 Share these URLs with anyone to access SkillTwin:
echo.
echo 🔗 Frontend (React App):
echo    Look for: https://xxxxx.ngrok.io
echo    This will redirect to the SkillTwin login page
echo.
echo 🔗 Backend API:
echo    Look for: https://xxxxx.ngrok.io  
echo    This provides API access for the application
echo.
echo 📝 Instructions:
echo    1. Check the ngrok windows for the public URLs
echo    2. Share the frontend URL with users
echo    3. Users can login with: demo@skilltwin.com / demo123
echo    4. All features work through the tunnel
echo.
echo 🔒 Security Notes:
echo    • URLs are temporary (change on restart)
echo    • HTTPS encryption is provided by ngrok
echo    • Anyone with the URL can access the app
echo    • Consider upgrading to ngrok paid plan for custom domains
echo.
echo 🛑 To stop: Close the ngrok windows or press Ctrl+C
echo.

echo 🌐 Opening ngrok dashboard for monitoring...
start https://dashboard.ngrok.com/

echo.
echo ✅ Public access setup complete!
echo 🚀 SkillTwin is now accessible from anywhere!
echo.

pause
