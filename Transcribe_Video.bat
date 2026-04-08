@echo off
setlocal enabledelayedexpansion

:: --- SETTINGS ---
set MODEL=base
:: ----------------

title Whisper Transcriber (AutoSub Reels)

if "%~1"=="" (
    echo [ERROR] No file provided!
    echo.
    echo Usage: Drag and drop your video file onto this .bat file.
    echo.
    pause
    exit /b
)

echo ========================================
echo   AutoSub Reels: Transcription Tool
echo ========================================
echo.
echo Input File:  "%~1"
echo Model:       %MODEL%
echo.

:: Check if python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python and OpenAI Whisper.
    pause
    exit /b
)

:: Run transcription
python "%~dp0transcribe.py" "%~1" --model %MODEL%

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Transcription failed. 
    echo Make sure you have installed whisper: pip install openai-whisper
    pause
) else (
    echo.
    echo [SUCCESS] Transcription completed!
    echo You can now import the generated .srt file into After Effects.
    timeout /t 5
)
