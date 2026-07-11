@echo off
title Dashboard Updater
cd /d "%~dp0"

echo ==========================================
echo   Premier Energies Dashboard Updater
echo ==========================================
echo.

echo [1/4] Running ingest.py ...
python ingest.py
if %errorlevel% neq 0 (
    echo ERROR: ingest.py failed. Check your Excel files.
    pause
    exit /b 1
)
echo Done.
echo.

echo [2/4] Running build_dashboard.py ...
python build_dashboard.py
if %errorlevel% neq 0 (
    echo ERROR: build_dashboard.py failed.
    pause
    exit /b 1
)
echo Done.
echo.

echo [3/4] Staging files for git ...
git add data.json index.html
echo Done.
echo.

echo [4/4] Committing and pushing to GitHub ...
git commit -m "Update data"
git push origin main
if %errorlevel% neq 0 (
    echo ERROR: Git push failed. Check your internet connection or GitHub access.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   Done! Dashboard will be live in ~2 min
echo   at your Vercel URL.
echo ==========================================
echo.
pause
