@echo off
REM Deploy backend to PythonAnywhere
REM This script prepares the backend for deployment

if "%1"=="" (
    echo Usage: deploy-backend.bat YOUR_PYTHONANYWHERE_USERNAME
    echo.
    echo Example: deploy-backend.bat john2025
    echo.
    echo This will create a deployment package you can upload to PythonAnywhere
    exit /b 1
)

set PYTHONANYWHERE_USERNAME=%1

echo ========================================
echo PythonAnywhere Backend Deployment
echo ========================================
echo Username: %PYTHONANYWHERE_USERNAME%
echo Backend URL: https://%PYTHONANYWHERE_USERNAME%.pythonanywhere.com
echo.

echo Preparing backend for deployment...
cd my-backend

if exist backend-deploy.zip (
    echo Removing old deployment package...
    del backend-deploy.zip
)

echo Creating deployment package...
REM Using 7-Zip if available, otherwise built-in compression
if exist "C:\Program Files\7-Zip\7z.exe" (
    echo Using 7-Zip to compress...
    "C:\Program Files\7-Zip\7z.exe" a -r backend-deploy.zip . -x!node_modules -x!uploads -x!.env*
) else (
    echo Please install 7-Zip or manually create a zip file excluding:
    echo - node_modules folder
    echo - uploads folder
    echo - .env files
    exit /b 1
)

cd ..

echo.
echo ========================================
echo Package Created Successfully!
echo ========================================
echo Location: my-backend\backend-deploy.zip
echo.
echo Next steps:
echo 1. Log in to PythonAnywhere (https://www.pythonanywhere.com)
echo 2. Go to Files section
echo 3. Upload backend-deploy.zip
echo 4. Extract the zip
echo 5. Open Bash console and run:
echo    cd backend-deploy
echo    npm install
echo    npm start
echo.
echo 6. Configure Web app to use your Node.js app
echo 7. Enable CORS for: https://hmh-8138.github.io
echo.
pause
