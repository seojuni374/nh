@echo off
setlocal EnableDelayedExpansion

echo Installing Claude Code...

:: Check for Node.js
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Node.js is not installed or not in PATH.
    echo Please install Node.js from https://nodejs.org/ and try again.
    exit /b 1
)

:: Check Node.js version (require >= 18)
for /f "tokens=1 delims=v" %%i in ('node --version') do set NODE_VER=%%i
for /f "tokens=1 delims=v" %%i in ('node --version 2^>nul') do (
    for /f "tokens=1 delims=." %%j in ("%%i") do set NODE_MAJOR=%%j
)
:: Strip leading 'v' if present
set NODE_VER_RAW=
for /f "tokens=*" %%i in ('node --version') do set NODE_VER_RAW=%%i
set NODE_VER_NUM=%NODE_VER_RAW:v=%
for /f "tokens=1 delims=." %%i in ("%NODE_VER_NUM%") do set NODE_MAJOR=%%i

if %NODE_MAJOR% LSS 18 (
    echo Error: Node.js version 18 or higher is required.
    echo Current version: %NODE_VER_RAW%
    echo Please upgrade Node.js from https://nodejs.org/ and try again.
    exit /b 1
)

:: Check for npm
where npm >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: npm is not installed or not in PATH.
    echo Please install Node.js ^(which includes npm^) from https://nodejs.org/ and try again.
    exit /b 1
)

:: Install Claude Code globally
echo Installing @anthropic-ai/claude-code...
npm install -g @anthropic-ai/claude-code
if %ERRORLEVEL% neq 0 (
    echo.
    echo Installation failed. Try running this script as Administrator,
    echo or run: npm install -g @anthropic-ai/claude-code
    exit /b 1
)

echo.
echo Claude Code installed successfully!
echo Run 'claude' to get started.
echo.

endlocal
