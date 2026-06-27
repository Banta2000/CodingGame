@echo off
setlocal ENABLEDELAYEDEXPANSION

REM newpy.bat — Copy a Python template to a new file in one step (Windows cmd)
REM Usage:
REM   newpy.bat NewFileName.py [TemplatePath]
REM Notes:
REM   - If .py is omitted on NewFileName, it will be added.
REM   - If TemplatePath is omitted, _template_simple.py in this folder is used.

set "SCRIPT_DIR=%~dp0"
set "DEFAULT_TEMPLATE=%SCRIPT_DIR%_template_simple.py"

IF "%~1"=="" (
  echo Usage: %~n0 NewFileName.py [TemplatePath]
  echo.
  echo Copies the template to the given file name.
  echo If no template is provided, it defaults to:
  echo   %DEFAULT_TEMPLATE%
  exit /b 1
)

set "TARGET=%~1"

REM Add .py extension if missing
for %%I in ("%TARGET%") do set "EXT=%%~xI"
if "%EXT%"=="" set "TARGET=%TARGET%.py"

REM Resolve to absolute path
for %%I in ("%TARGET%") do set "TARGET_ABS=%%~fI"

REM Ensure parent directory exists
for %%I in ("%TARGET_ABS%") do set "PARENT=%%~dpI"
if not exist "%PARENT%" (
  mkdir "%PARENT%" || (
    echo Failed to create directory "%PARENT%".
    exit /b 1
  )
)

REM Determine template
set "TEMPLATE=%DEFAULT_TEMPLATE%"
if not "%~2"=="" set "TEMPLATE=%~2"

if not exist "%TEMPLATE%" (
  echo Template not found: "%TEMPLATE%"
  exit /b 1
)

if exist "%TARGET_ABS%" (
  echo File already exists: "%TARGET_ABS%"
  exit /b 1
)

copy /Y "%TEMPLATE%" "%TARGET_ABS%" >nul
if errorlevel 1 (
  echo Copy failed.
  exit /b 1
)

echo Created "%TARGET_ABS%" from "%TEMPLATE%".
endlocal
exit /b 0
