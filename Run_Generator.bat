@echo off
title Google Chrome Profile Generator - Developed by Mr.Rahul Scripts
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit...
    pause >nul
)
