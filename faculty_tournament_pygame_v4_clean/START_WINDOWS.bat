@echo off
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
    python -m pip install -r requirements.txt
    python main.py
) else (
    py -m pip install -r requirements.txt
    py main.py
)
pause
