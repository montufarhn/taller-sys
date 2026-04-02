# Empaquetado e Instalador para Taller Pro Auto

Este proyecto se puede empaquetar como una aplicación de Windows con un instalador que crea un acceso directo en el escritorio.

## Qué hace
- `taller_service.py`: define el servicio de Windows que arranca el servidor Uvicorn.
- `launcher.py`: arranca el servicio desde el escritorio, muestra la IP local y abre el navegador.
- `build_installer.bat`: construye los ejecutables con PyInstaller y luego genera un instalador con Inno Setup.
- `installer.iss`: script de Inno Setup que copia la aplicación al directorio de instalación, crea el acceso directo y registra el servicio.

## Requisitos previos
- Python 3.11 o 3.12 instalado en Windows.
- `pip install -r requirements.txt`
- `pyinstaller` instalado: `pip install pyinstaller`
- Inno Setup instalado en Windows (por ejemplo, Inno Setup 6).

## Cómo generar el instalador
1. Abre una terminal PowerShell en la carpeta del proyecto.
2. Ejecuta:
   ```powershell
   python build_installer.bat
   ```
3. Si Inno Setup no está en la variable de entorno `ISCC`, el script buscará automáticamente en:
   - `%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe`
   - `%ProgramFiles%\Inno Setup 6\ISCC.exe`

4. Al finalizar, encontrarás el instalador en la carpeta `Output\`.

## Uso después de instalar
- Instala la aplicación con el instalador generado.
- El instalador registra el servicio de Windows `Taller Pro Auto` con inicio automático.
- Se creará un acceso directo en el escritorio llamado `Taller Pro Auto`.
- Al ejecutar el acceso directo, el lanzador intentará iniciar el servicio si no está en ejecución y abrirá el navegador.
- El lanzador mostrará:
  - `http://127.0.0.1:8000`
  - y la(s) IP(s) local(es) de red desde las cuales otros usuarios pueden conectarse.

## Nota sobre la base de datos
- El sistema usa SQLite por defecto con `sqlite:///./taller.db`.
- El archivo de base de datos se creará en la carpeta de instalación si no existe.
