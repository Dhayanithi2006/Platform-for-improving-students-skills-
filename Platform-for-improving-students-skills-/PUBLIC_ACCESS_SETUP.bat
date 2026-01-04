@echo off
title SkillTwin Public Access Setup
color 0E

echo.
echo ============================================================
echo              SKILLTWIN PUBLIC ACCESS SETUP
echo ============================================================
echo.

echo Current Server Status:
echo ------------------------
echo Frontend: http://localhost:3000 (Running)
echo Backend:  http://localhost:5000 (Running)
echo.

echo PUBLIC ACCESS OPTIONS:
echo ======================
echo.
echo 1. MOBILE HOTSPOT (Recommended for quick setup)
echo    - Enable mobile hotspot on your computer
echo    - Other devices connect to your hotspot
echo    - Access URL: http://192.168.137.1:3000
echo.
echo 2. SAME NETWORK ACCESS
echo    - Devices on same WiFi/network
echo    - Access URL: http://10.10.37.167:3000
echo.
echo 3. PORT FORWARDING (Advanced)
echo    - Forward ports 3000 and 5000 in router
echo    - Access via your public IP
echo.
echo 4. CLOUD DEPLOYMENT (Production)
echo    - Deploy to Vercel/Render for permanent access
echo.

echo LOGIN CREDENTIALS:
echo ==================
echo Email: demo@skilltwin.com
echo Password: demo123
echo.

echo TESTING CURRENT SETUP:
echo =====================
echo.
echo Testing local access...
curl -s http://localhost:3000 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Frontend accessible locally
) else (
    echo [ERROR] Frontend not responding
)

curl -s http://localhost:5000/api/health >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Backend API responding
) else (
    echo [ERROR] Backend API not responding
)

echo.
echo NETWORK INFORMATION:
echo ====================
echo.
ipconfig | findstr "IPv4"
echo.
echo Your local network IP should be: 10.10.37.167
echo.

echo QUICK START GUIDE:
echo ==================
echo.
echo For Mobile Hotspot:
echo 1. Press Windows Key + Settings
echo 2. Network & Internet > Mobile hotspot
echo 3. Turn ON "Share my internet connection"
echo 4. Set name: SkillTwin-Hotspot
echo 5. Set password: skilltwin123
echo 6. Share http://192.168.137.1:3000 with users
echo.

echo For Same Network:
echo 1. Ensure devices are on same WiFi
echo 2. Share http://10.10.37.167:3000 with users
echo 3. Users login with demo credentials
echo.

echo ============================================================
echo                    SETUP COMPLETE!
echo ============================================================
echo.
echo Your SkillTwin application is ready for multi-user access!
echo Choose an access method above and share the URL.
echo.

pause
