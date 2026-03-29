@echo off
echo Starting ETE Resource Portal Server...
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%my-backend"
node index.js
pause
