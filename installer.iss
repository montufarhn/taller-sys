[Setup]
AppName=Taller Pro Auto
AppVersion=1.0
DefaultDirName={pf}\Taller Pro Auto
DefaultGroupName=Taller Pro Auto
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=TallerProAuto_Installer
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\TallerProAutoService\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs
Source: "dist\TallerProAutoLauncher\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Taller Pro Auto"; Filename: "{app}\TallerProAutoLauncher.exe"
Name: "{commondesktop}\Taller Pro Auto"; Filename: "{app}\TallerProAutoLauncher.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Iconos:"; Flags: unchecked

[Run]
Filename: "{app}\TallerProAutoService.exe"; Parameters: "install --startup auto"; Description: "Instalar servicio de Taller Pro Auto"; Flags: waituntilterminated
Filename: "{app}\TallerProAutoService.exe"; Parameters: "start"; Description: "Iniciar servicio de Taller Pro Auto"; Flags: waituntilterminated
Filename: "{app}\TallerProAutoLauncher.exe"; Description: "Abrir Taller Pro Auto"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "{app}\TallerProAutoService.exe"; Parameters: "stop"; Flags: waituntilterminated
Filename: "{app}\TallerProAutoService.exe"; Parameters: "remove"; Flags: waituntilterminated
