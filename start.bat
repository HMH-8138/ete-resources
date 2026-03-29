@echo off
setlocal

echo Starting ETE Resource Portal backend on port 3000...

rem Resolve project root from this script location
set "ROOT_DIR=%~dp0"
set "BACKEND_DIR=%ROOT_DIR%my-backend"

if not exist "%BACKEND_DIR%\index.js" (
	echo [ERROR] Backend entry file not found: "%BACKEND_DIR%\index.js"
	pause
	exit /b 1
)

where node >nul 2>&1
if errorlevel 1 (
	if exist "C:\Program Files\nodejs\node.exe" (
		set "NODE_EXE=C:\Program Files\nodejs\node.exe"
		set "NPM_CMD=C:\Program Files\nodejs\npm.cmd"
	) else (
		echo [ERROR] Node.js is not installed or not in PATH.
		echo Install Node.js from https://nodejs.org and try again.
		pause
		exit /b 1
	)
)

if not defined NODE_EXE (
	set "NODE_EXE=node"
	set "NPM_CMD=npm"
)

pushd "%BACKEND_DIR%"

if not exist "node_modules" (
	echo Installing backend dependencies...
	call "%NPM_CMD%" install
	if errorlevel 1 (
		echo [ERROR] Failed to install dependencies.
		popd
		pause
		exit /b 1
	)
)

echo Launching server...
"%NODE_EXE%" index.js

popd
pause
