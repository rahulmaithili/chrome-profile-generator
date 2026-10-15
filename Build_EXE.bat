@echo off
title Building Chrome Profile Generator EXE - Mr.Rahul Scripts
cd /d "%~dp0"

echo ===================================================
echo  Chrome Profile Generator - Standalone EXE Builder
echo  Developed by Mr.Rahul Scripts
echo ===================================================
echo.
echo [*] Checking PyInstaller...
python -m PyInstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] PyInstaller not found. Installing...
    pip install pyinstaller
)

echo.
python -m PyInstaller --noconsole --onefile --icon="assets\icon.ico" --add-data "assets;assets" --version-file="version_info.txt" --manifest="app.manifest" --name "Chrome_Profile_Generator" --hidden-import=win32com --hidden-import=win32com.client --clean main.py

if exist "dist\Chrome_Profile_Generator.exe" (
    echo.
    echo [*] Copying EXE to main folder...
    copy /y "dist\Chrome_Profile_Generator.exe" "Chrome_Profile_Generator.exe" >nul
    echo.
    echo ===================================================
    echo  [SUCCESS] Chrome_Profile_Generator.exe is READY!
    echo  Developed by Mr.Rahul Scripts
    echo ===================================================
) else (
    echo.
    echo [!] Build failed. Please check the error log above.
)

pause
