@echo off
setlocal
chcp 932 > nul

echo ========================================
echo  PDF to Office Converter
echo ========================================

:: #1 Search for uv in PATH
set "UV_PATH="
for /f "delims=" %%I in ('where uv 2^>nul') do (
    if not defined UV_PATH set "UV_PATH=%%I"
)

:: #2 Search in Python Scripts directory (for pip installations)
if not defined UV_PATH (
    for /f "usebackq delims=" %%I in (`python -c "import sysconfig; print(sysconfig.get_path('scripts'))" 2^>nul`) do (
        if exist "%%I\uv.exe" set "UV_PATH=%%I\uv.exe"
    )
)

:: #3 Search using Python Launcher
if not defined UV_PATH (
    for /f "usebackq delims=" %%I in (`py -3 -c "import sysconfig; print(sysconfig.get_path('scripts'))" 2^>nul`) do (
        if exist "%%I\uv.exe" set "UV_PATH=%%I\uv.exe"
    )
)

:: #4 Install uv using the official installer if not found
if not defined UV_PATH (
    echo.
    echo uv was not found.
    echo Installing uv...
    echo.

    powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"

    if errorlevel 1 (
        echo.
        echo Failed to install uv.
        goto :ERROR
    )

    :: Check the installation directory
    if exist "%USERPROFILE%\.local\bin\uv.exe" (
        set "UV_PATH=%USERPROFILE%\.local\bin\uv.exe"
    )
)

:: Final check for uv
if not defined UV_PATH (
    echo.
    echo uv.exe was not found.
    goto :ERROR
)

echo.
echo Using uv:
echo %UV_PATH%
echo.

:: Change to the project directory
cd /d "%~dp0"

:: Get the Python script name from the batch file name
set "SCRIPT_NAME=%~n0.py"

:: Run PDF conversion
"%UV_PATH%" run "%SCRIPT_NAME%" %*

set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo ========================================
echo  Process completed.
echo ========================================

pause
exit /b %EXIT_CODE%

:ERROR
echo.
pause
exit /b 1
