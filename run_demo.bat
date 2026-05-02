@echo off
REM Living README Agent - Quick Demo Script for Windows

echo 🤖 Living README Agent - Quick Demo
echo ====================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is required but not installed.
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is required but not installed.
    exit /b 1
)

echo ✓ Python found
echo ✓ Node.js found
echo.

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -q -r agent\requirements.txt
echo ✓ Python dependencies installed
echo.

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
cd target-app
call npm install --silent
cd ..
echo ✓ Node.js dependencies installed
echo.

REM Run the agent
echo 🚀 Running Living README Agent...
echo.
cd agent
python main.py
cd ..

echo.
echo ====================================
echo ✅ Demo Complete!
echo.
echo 📊 Check the reports in bob_sessions\
echo 📝 Review the updated target-app\README.md
echo 📖 See DEMO.md for more scenarios
echo.
pause

@REM Made with Bob
