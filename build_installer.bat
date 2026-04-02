@echo off
setlocal
cd /d %~dp0

echo =============================================
echo Construyendo ejecutables con PyInstaller...
echo =============================================

python -m PyInstaller --noconfirm --onedir --name TallerProAutoService --add-data "index.html;." --hidden-import=win32timezone --hidden-import=win32serviceutil --hidden-import=win32event --hidden-import=main --hidden-import=database --hidden-import=models taller_service.py
if errorlevel 1 (
    echo ERROR: PyInstaller falló en TallerProAutoService.
    pause
    exit /b 1
)

python -m PyInstaller --noconfirm --onedir --name TallerProAutoLauncher launcher.py
if errorlevel 1 (
    echo ERROR: PyInstaller falló en TallerProAutoLauncher.
    pause
    exit /b 1
)

echo.
echo =============================================
echo Construyendo instalador con Inno Setup...
echo =============================================

if defined ISCC (
    "%ISCC%" installer.iss
) else if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" installer.iss
) else if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles%\Inno Setup 6\ISCC.exe" installer.iss
) else (
    echo ERROR: No se encontró ISCC.exe. Instala Inno Setup o configura la variable de entorno ISCC.
    pause
    exit /b 1
)

if errorlevel 1 (
    echo ERROR: La compilación del instalador falló.
    pause
    exit /b 1
)

echo.
echo Instalador generado correctamente.
echo Busca el archivo .exe dentro de Output\
pause
