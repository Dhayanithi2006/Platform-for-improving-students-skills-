@echo off
title SkillTwin - Mobile Hotspot Setup
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║          SKILLTWIN MOBILE HOTSPOT SETUP GUIDE              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📱 Setting up mobile hotspot for SkillTwin access...
echo.

echo 🔧 Step 1: Enable Mobile Hotspot
echo.
echo 📋 Instructions:
echo    1. Press Windows Key + I to open Settings
echo    2. Click on "Network & Internet"
echo    3. Click on "Mobile hotspot"
echo    4. Turn ON "Share my internet connection"
echo    5. Set network name: "SkillTwin-Hotspot"
echo    6. Set password: "skilltwin123"
echo    7. Click "Save"
echo.

echo 🚀 Step 2: Start SkillTwin Servers
echo.
echo 📋 Instructions:
echo    1. Double-click: START_COMPLETE.bat
echo    2. Wait for servers to start
echo    3. Note the IP address shown
echo.

echo 📡 Step 3: Connect Other Devices
echo.
echo 📋 Instructions:
echo    1. On other device, open WiFi settings
echo    2. Connect to "SkillTwin-Hotspot"
echo    3. Enter password: "skilltwin123"
echo    4. Open browser
echo    5. Go to: http://[IP_ADDRESS]:3000
echo.

echo 🔍 Step 4: Find Your IP Address
echo.
echo 📋 Instructions:
echo    1. Open Command Prompt on main computer
echo    2. Type: ipconfig
echo    3. Look for "IPv4 Address" under "Wireless LAN adapter"
echo    4. Use this IP for access (e.g., 192.168.137.1)
echo.

echo 🌐 Example Access URLs:
echo.
echo 📱 Frontend: http://192.168.137.1:3000
echo 📡 Backend: http://192.168.137.1:5000/api
echo.

echo 🔐 Login Credentials:
echo.
echo 📧 Email: demo@skilltwin.com
echo 🔑 Password: demo123
echo.

echo ✅ Setup Complete!
echo.
echo 🎯 Benefits of Mobile Hotspot:
echo    ✅ Works anywhere with cellular data
echo    ✅ No internet connection required
echo    ✅ Secure with WPA2 encryption
echo    ✅ Multiple devices can connect
echo    ✅ Easy to set up and use
echo.

echo 📱 How Many Devices Can Connect?
echo    • Windows 10/11: Up to 8 devices
echo    • Can be increased in settings if needed
echo.

echo 🔧 Troubleshooting:
echo    ❌ "Can't connect to hotspot":
echo       • Make sure hotspot is turned ON
echo       • Check password spelling
echo       • Restart hotspot on main computer
echo.
echo    ❌ "Site can't be reached":
echo       • Verify SkillTwin servers are running
echo       • Check IP address with ipconfig
echo       • Try http://localhost:3000 on main computer first
echo.
echo    ❌ "Slow connection":
echo       • Check cellular signal strength
echo       • Limit number of connected devices
echo       • Close other apps using data
echo.

echo 🚀 Ready to Start?
echo.
echo 📋 Quick Checklist:
echo    ☐ Mobile hotspot enabled
echo    ☐ Network name: "SkillTwin-Hotspot"
echo    ☐ Password: "skilltwin123"
echo    ☐ SkillTwin servers running
echo    ☐ IP address noted
echo    ☐ Other device connected to hotspot
echo.

echo 🎉 Your SkillTwin is ready for multi-device access!
echo.

pause
