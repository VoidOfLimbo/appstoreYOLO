; AppStore Installer Script for Inno Setup
; This script creates an installer with version checking and update capabilities
;
; Prerequisites:
; 1. Install Inno Setup from https://jrsoftware.org/isdl.php
; 2. Build the application with PyInstaller (run setup.py)
; 3. Compile this script with Inno Setup Compiler
;
; Version-aware features:
; - Checks if application is already installed
; - Compares installed version with new version
; - Updates only if new version is newer
; - Preserves user data during updates

#define MyAppName "AppStore"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "AppStore Team"
#define MyAppURL "https://www.example.com"
#define MyAppExeName "AppStore.exe"
#define MyAppID "{{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}"

[Setup]
; App identification
AppId={#MyAppID}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation settings
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer\output
OutputBaseFilename=AppStore_Setup_{#MyAppVersion}
SetupIconFile=..\assets\icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Version information
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Installer
VersionInfoCopyright=Copyright (C) 2025 {#MyAppPublisher}

; Architecture
ArchitecturesInstallIn64BitMode=x64

; Uninstall
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main executable and all files from PyInstaller output
Source: "..\dist\AppStore\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
var
  IsUpgrade: Boolean;
  OldVersion: String;
  
// Read version from version.txt file
function GetInstalledVersion(): String;
var
  VersionFile: String;
  Lines: TArrayOfString;
begin
  Result := '';
  VersionFile := ExpandConstant('{app}\config\version.txt');
  
  if FileExists(VersionFile) then
  begin
    if LoadStringsFromFile(VersionFile, Lines) then
    begin
      if GetArrayLength(Lines) > 0 then
        Result := Trim(Lines[0]);
    end;
  end;
end;

// Compare two version strings
// Returns: -1 if V1 < V2, 0 if V1 = V2, 1 if V1 > V2
function CompareVersions(V1, V2: String): Integer;
var
  P1, P2: Integer;
  N1, N2: Integer;
  S1, S2: String;
begin
  Result := 0;
  
  while (Length(V1) > 0) or (Length(V2) > 0) do
  begin
    // Extract next component from V1
    P1 := Pos('.', V1);
    if P1 > 0 then
    begin
      S1 := Copy(V1, 1, P1 - 1);
      Delete(V1, 1, P1);
    end
    else
    begin
      S1 := V1;
      V1 := '';
    end;
    
    // Extract next component from V2
    P2 := Pos('.', V2);
    if P2 > 0 then
    begin
      S2 := Copy(V2, 1, P2 - 1);
      Delete(V2, 1, P2);
    end
    else
    begin
      S2 := V2;
      V2 := '';
    end;
    
    // Convert to integers
    if S1 = '' then N1 := 0 else N1 := StrToIntDef(S1, 0);
    if S2 = '' then N2 := 0 else N2 := StrToIntDef(S2, 0);
    
    // Compare
    if N1 < N2 then
    begin
      Result := -1;
      Exit;
    end
    else if N1 > N2 then
    begin
      Result := 1;
      Exit;
    end;
  end;
end;

// Check if this is an upgrade installation
function InitializeSetup(): Boolean;
var
  UninstallKey: String;
  InstalledVersion: String;
  NewVersion: String;
  Comparison: Integer;
  Message: String;
begin
  Result := True;
  IsUpgrade := False;
  NewVersion := '{#MyAppVersion}';
  
  // Check if application is already installed
  UninstallKey := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppID}_is1');
  
  if RegKeyExists(HKLM, UninstallKey) or RegKeyExists(HKCU, UninstallKey) then
  begin
    // Application is installed, get version
    InstalledVersion := GetInstalledVersion();
    
    if InstalledVersion <> '' then
    begin
      OldVersion := InstalledVersion;
      IsUpgrade := True;
      
      // Compare versions
      Comparison := CompareVersions(NewVersion, InstalledVersion);
      
      if Comparison > 0 then
      begin
        // New version is newer - proceed with upgrade
        Message := 'AppStore version ' + InstalledVersion + ' is currently installed.' + #13#10 +
                   'This will upgrade to version ' + NewVersion + '.' + #13#10#13#10 +
                   'Do you want to continue?';
        Result := MsgBox(Message, mbConfirmation, MB_YESNO) = IDYES;
      end
      else if Comparison < 0 then
      begin
        // Installed version is newer
        Message := 'A newer version (' + InstalledVersion + ') is already installed.' + #13#10 +
                   'You are trying to install version ' + NewVersion + '.' + #13#10#13#10 +
                   'It is not recommended to downgrade.' + #13#10 +
                   'Do you want to continue anyway?';
        Result := MsgBox(Message, mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES;
      end
      else
      begin
        // Same version
        Message := 'AppStore version ' + InstalledVersion + ' is already installed.' + #13#10 +
                   'Do you want to reinstall?';
        Result := MsgBox(Message, mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES;
      end;
    end;
  end;
end;

// Customize wizard page text based on upgrade status
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpWelcome then
  begin
    if IsUpgrade then
    begin
      WizardForm.WelcomeLabel2.Caption := 
        'This will upgrade ' + '{#MyAppName}' + ' from version ' + OldVersion + 
        ' to version {#MyAppVersion} on your computer.' + #13#10#13#10 +
        'Your settings and data will be preserved.' + #13#10#13#10 +
        'It is recommended that you close all other applications before continuing.' + #13#10#13#10 +
        'Click Next to continue, or Cancel to exit Setup.';
    end;
  end;
end;

// Update version file after installation
procedure CurStepChanged(CurStep: TSetupStep);
var
  VersionFile: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Ensure version.txt is updated with new version
    VersionFile := ExpandConstant('{app}\config\version.txt');
    SaveStringToFile(VersionFile, '{#MyAppVersion}', False);
  end;
end;
