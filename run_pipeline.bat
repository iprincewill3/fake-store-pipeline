@echo off
setlocal

REM === Go to your project root ===
cd /d "C:\Users\admin\OneDrive\Documents\fake-store-pipeline" || (
  echo ERROR: Could not cd into project folder.
  exit /b 1
)

REM === Make logs folder if missing ===
if not exist "logs" mkdir "logs"

REM === Build a safe timestamp via PowerShell (locale-agnostic) ===
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%i

REM === Sanity checks ===
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: .venv\Scripts\python.exe not found.
  exit /b 1
)
if not exist "flows.py" (
  echo ERROR: flows.py not found in project root.
  exit /b 1
)

REM === Run with venv's Python directly (no activate needed) ===
".\.venv\Scripts\python.exe" "flows.py" >> "logs\run_%TS%.log" 2>&1

REM === Show where the log went ===
echo Wrote log to logs\run_%TS%.log
endlocal
