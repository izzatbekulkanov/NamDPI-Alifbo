; NamDPI alifbo - Inno Setup Script
; Namangan davlat pedagogika instituti
; Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)

#define MyAppName "NamDPI alifbo"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Namangan davlat pedagogika instituti Raqamli ta'lim texnologiyalari markazi"
#define MyAppURL "https://nspi.uz"
#define MyAppExeName "NamDPI_Alifbo.exe"

[Setup]
AppId={{7A4B1389-7F33-4D88-9B5A-B47285C20188}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\NamDPI alifbo
DefaultGroupName=NamDPI alifbo
AllowNoIcons=yes
OutputDir=I:\translate\installer_output
OutputBaseFilename=NamDPI_Alifbo_Setup
SetupIconFile=I:\translate\app_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
CloseApplications=yes
CloseApplicationsFilter=NamDPI_Alifbo.exe,NDPI_Alifbo.exe

[Languages]
Name: "uzbek"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
uzbek.CreateDesktopIcon=Ish stolida "NamDPI alifbo" yorlig'ini (shortcut) yaratish
uzbek.AutoStart=Kompyuter yoqilganda "NamDPI alifbo" avtomatik ishga tushsin
uzbek.LaunchProgram=NamDPI alifbo dasturini hoziroq ishga tushirish

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startup"; Description: "{cm:AutoStart}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "I:\translate\dist\NamDPI_Alifbo\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "I:\translate\app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app_icon.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\app_icon.ico"
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startup; IconFilename: "{app}\app_icon.ico"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram}"; Flags: nowait postinstall skipifsilent
