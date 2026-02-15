@echo off
echo Building CLI Tool...
python -m PyInstaller --onefile ..\cli\fiberhome_keygen.py
if %ERRORLEVEL% NEQ 0 (
    echo CLI Build Failed!
    exit /b %ERRORLEVEL%
)

echo Building GUI Tool...
python -m PyInstaller --onefile ..\gui\fiberhome_gui.py
if %ERRORLEVEL% NEQ 0 (
    echo GUI Build Failed!
    exit /b %ERRORLEVEL%
)

echo Build Complete! Check the 'dist' folder.
pause
