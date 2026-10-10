@echo off
setlocal
rem Keep all project operations separate from the legacy .venv.
cd /d "%~dp0.."
if errorlevel 1 exit /b 2
set "UV_PROJECT_ENVIRONMENT=%CD%\.venv-py312"
set "UV_PYTHON_INSTALL_DIR=%CD%\.local\python"
set "UV_CACHE_DIR=%CD%\.local\uv-cache"
if not exist ".local\uv-tool\Scripts\uv.exe" (
    echo uv is missing. See project_steps\00_03_reproducible_env\README.md for setup.
    exit /b 2
)
".local\uv-tool\Scripts\uv.exe" %*
exit /b %ERRORLEVEL%
