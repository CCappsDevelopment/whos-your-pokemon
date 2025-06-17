@echo off
REM Windows build script for Who's Your Pokemon
REM Run this script on a Windows machine

echo ============================================================
echo Who's Your Pokemon - Windows Builder
echo ============================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.7+ first.
    pause
    exit /b 1
)

REM Install required packages
echo 📦 Installing required packages...
pip install pyinstaller pillow requests

REM Check if required files exist
if not exist "main.py" (
    echo ❌ main.py not found. Please run this from the project root directory.
    pause
    exit /b 1
)

if not exist "assets\question_mark.ico" (
    echo 📸 Creating Windows icon...
    python -c "from PIL import Image; img = Image.open('assets/question_mark.png'); img.save('assets/question_mark.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])"
)

echo 🔨 Building Who's Your Pokemon for Windows...

REM Run PyInstaller with Windows-specific settings
pyinstaller ^
    --name="Whos Your Pokemon" ^
    --windowed ^
    --onedir ^
    --icon=assets/question_mark.ico ^
    --add-data="data_sources/pokemon_data.json;data_sources" ^
    --add-data="assets;assets" ^
    --clean ^
    --noconfirm ^
    main.py

if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo ✅ Build completed successfully!
echo 📦 Application built at: dist\Whos Your Pokemon
echo 🚀 To run: double-click "dist\Whos Your Pokemon\Whos Your Pokemon.exe"

REM Create a simple launcher
echo 📎 Creating launcher...
echo @echo off > "dist\Whos Your Pokemon\Run Game.bat"
echo cd /d "%%~dp0" >> "dist\Whos Your Pokemon\Run Game.bat"
echo start "" "Whos Your Pokemon.exe" >> "dist\Whos Your Pokemon\Run Game.bat"

echo ✅ Created launcher: "Run Game.bat"

echo.
echo ============================================================
echo 🎉 Windows Build Complete!
echo Your app is ready in the 'dist' folder
echo ============================================================
pause
