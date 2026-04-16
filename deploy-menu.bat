@echo off
REM Interactive Deployment Helper for GitHub Pages + PythonAnywhere
REM This script guides you through the deployment process

setlocal enabledelayedexpansion

echo.
echo ========================================
echo GitHub Pages + PythonAnywhere Deployer
echo ========================================
echo.

:menu
echo What would you like to do?
echo.
echo 1. Update API URLs (configure for PythonAnywhere)
echo 2. Initialize Git repository
echo 3. Commit and push to GitHub
echo 4. Prepare backend for PythonAnywhere
echo 5. View deployment guide
echo 6. View quick start guide
echo 7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto update_urls
if "%choice%"=="2" goto init_git
if "%choice%"=="3" goto push_git
if "%choice%"=="4" goto deploy_backend
if "%choice%"=="5" goto view_deployment
if "%choice%"=="6" goto view_quickstart
if "%choice%"=="7" goto exit
echo Invalid choice. Please try again.
goto menu

:update_urls
echo.
echo Updating API URLs...
echo.
set /p username="Enter your PythonAnywhere username: "
if "!username!"=="" (
    echo Error: Username required
    pause
    goto menu
)

node update-api-urls.js https://!username!.pythonanywhere.com

if errorlevel 1 (
    echo.
    echo Error: Node.js not found or script failed
    echo Make sure Node.js is installed and you're in the project directory
) else (
    echo.
    echo ✅ API URLs updated successfully!
    echo Next: Commit changes and push to GitHub
)
pause
goto menu

:init_git
echo.
echo Initializing Git repository...
echo.

if exist .git (
    echo Git repository already initialized
) else (
    git init
    if errorlevel 1 (
        echo Error: Git not found. Please install Git.
        echo Download from: https://git-scm.com/download/win
    ) else (
        echo ✅ Git repository initialized
    )
)

pause
goto menu

:push_git
echo.
echo Pushing to GitHub...
echo.

git add .
set /p message="Enter commit message (press Enter for default): "
if "!message!"=="" (
    set message=Deploy to GitHub Pages with PythonAnywhere backend
)

git commit -m "!message!"

echo.
echo Now pushing to GitHub...
echo.
git push origin main

if errorlevel 1 (
    echo.
    echo Note: If push failed, you may need to:
    echo 1. Set up Git credentials
    echo 2. Create the repository on GitHub first
    echo 3. Add remote: git remote add origin https://github.com/hmh-8138/ete-resources.git
)

pause
goto menu

:deploy_backend
echo.
echo Preparing backend for PythonAnywhere deployment...
echo.

call deploy-backend.bat YOUR_USERNAME

pause
goto menu

:view_deployment
echo.
echo Opening DEPLOYMENT_GUIDE.md...
echo.

if exist DEPLOYMENT_GUIDE.md (
    start notepad DEPLOYMENT_GUIDE.md
) else (
    echo File not found: DEPLOYMENT_GUIDE.md
)

pause
goto menu

:view_quickstart
echo.
echo Opening QUICK_START.md...
echo.

if exist QUICK_START.md (
    start notepad QUICK_START.md
) else (
    echo File not found: QUICK_START.md
)

pause
goto menu

:exit
echo.
echo Goodbye!
echo.
echo Remember to:
echo 1. Update API URLs with your PythonAnywhere username
echo 2. Push code to GitHub
echo 3. Enable GitHub Pages in repository settings
echo 4. Deploy backend to PythonAnywhere
echo 5. Configure CORS on backend
echo.
pause
