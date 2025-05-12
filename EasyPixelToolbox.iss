[Setup]
AppName=EasyPixelToolbox
AppVersion=1.0
DefaultDirName={pf}\EasyPixelToolbox
DefaultGroupName=EasyPixelToolbox
UninstallDisplayIcon={app}\EasyPixelToolbox.exe
OutputBaseFilename=EasyPixelToolbox_Installer
Compression=lzma
SolidCompression=yes

[Languages]
Name: "default"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\EasyPixelToolbox.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\EasyPixelToolbox"; Filename: "{app}\EasyPixelToolbox.exe"
Name: "{group}\Uninstall EasyPixelToolbox"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\EasyPixelToolbox.exe"; Description: "Lanzar EasyPixelToolbox"; Flags: nowait postinstall skipifsilent
