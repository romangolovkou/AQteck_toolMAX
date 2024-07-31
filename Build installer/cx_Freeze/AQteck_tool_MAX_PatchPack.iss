; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{598AA9FD-1145-4030-92C8-DC578F409437}
AppName=AQteck tMAX PatchPack __VERSION__
AppVersion=__VERSION__
;AppVerName=AQteck tool MAX v0.01
AppPublisher=AQteck
DefaultDirName={pf}\AQteck tool MAX\
;ChangesAssociations=yes
;DefaultGroupName=AQteck tool MAX
DisableProgramGroupPage=yes
AllowNoIcons=yes
; LicenseFile=License.txt
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=admin
OutputDir=Output
OutputBaseFilename=AQteck tMAX PatchPack __VERSION__
SetupIconFile=..\..\cx_Freeze_result\UI\icons\AQico_silver.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"

;[Tasks]
;Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
;Source: "..\..\cx_Freeze_result\AQteck tool MAX.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\cx_Freeze_result\110_device_conf\*"; DestDir: "{app}\110_device_conf"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

;[Registry]
;Root: HKA; Subkey: "Software\Classes\\OpenWithProgids"; ValueType: string; ValueName: "AQteck tool MAXFile"; ValueData: ""; Flags: uninsdeletevalue
;Root: HKA; Subkey: "Software\Classes\AQteck tool MAXFile"; ValueType: string; ValueName: ""; ValueData: "AQteck tool MAX File"; Flags: uninsdeletekey
;Root: HKA; Subkey: "Software\Classes\AQteck tool MAXFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\AQteck tool MAX.exe,0"
;Root: HKA; Subkey: "Software\Classes\AQteck tool MAXFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\AQteck tool MAX.exe"" ""%1"""
;Root: HKA; Subkey: "Software\Classes\Applications\AQteck tool MAX.exe\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

;[Icons]
;Name: "{group}\AQteck tool MAX"; Filename: "{app}\AQteck tool MAX.exe"
;Name: "{autodesktop}\AQteck tool MAX"; Filename: "{app}\AQteck tool MAX.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\AQteck tool MAX.exe"; Description: "{cm:LaunchProgram,AQteck tool MAX}"; Flags: nowait postinstall skipifsilent

[Messages]
english.AppNotFound=The application was not found. Please make sure it is installed before applying the patch.
ukrainian.AppNotFound=Програму не знайдено. Переконайтесь, що вона встановлена, перш ніж застосовувати патч.

[Code]

function InitializeSetup(): Boolean;
begin
Result := False;
  if DirExists(ExpandConstant('{pf}\AQteck tool MAX')) then
  begin
    Result := True;
  end
  else
  begin
    MsgBox(ExpandConstant('{cm:AppNotFound}'), mbError, MB_OK);
  end;
end;