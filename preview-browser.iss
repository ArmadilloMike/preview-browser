#define MyAppName "Preview Browser"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "ArmadilloMike.Dev"
#define MyAppURL "https://github.com/ArmadilloMike/preview-browser"
#define MyAppExeName "link-handler.exe"
#define MyAppIconName "app.ico"
#define DoubleAmp(Value) StringChange(Value, "&", "&&")
#define EscapeConstArgument(Value) StringChange(StringChange(StringChange(Value, "%", "%25"), ",", "%2c"), "}", "%7d")

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppId={{6A4C0185-DF5B-470D-8BF8-132FD7C12B0B}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
SetupIconFile=assets\{#MyAppIconName}
UninstallDisplayIcon={app}\{#MyAppIconName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupArchitecture=x64
DisableProgramGroupPage=yes
LicenseFile=license.txt
PrivilegesRequired=lowest
OutputBaseFilename=previewbrowser
SolidCompression=yes
WizardStyle=modern windows11

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\link-handler\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\preview-browser\preview-browser.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\link-handler\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\preview-browser\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\{#MyAppIconName}"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
; 1. Define the URL Protocol Handler (ProgID)
Root: HKCU; Subkey: "Software\Classes\PreviewBrowserHTML"; ValueType: string; ValueName: ""; ValueData: "Preview Browser Document"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\PreviewBrowserHTML"; ValueType: string; ValueName: "URL Protocol"; ValueData: ""
Root: HKCU; Subkey: "Software\Classes\PreviewBrowserHTML\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppIconName}"
Root: HKCU; Subkey: "Software\Classes\PreviewBrowserHTML\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

; 2. Register the Application Capabilities
Root: HKCU; Subkey: "Software\PreviewBrowser\Capabilities"; ValueType: string; ValueName: "ApplicationName"; ValueData: "{#MyAppName}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\PreviewBrowser\Capabilities"; ValueType: string; ValueName: "ApplicationDescription"; ValueData: "Preview Browser Link Router"
Root: HKCU; Subkey: "Software\PreviewBrowser\Capabilities\URLAssociations"; ValueType: string; ValueName: "http"; ValueData: "PreviewBrowserHTML"
Root: HKCU; Subkey: "Software\PreviewBrowser\Capabilities\URLAssociations"; ValueType: string; ValueName: "https"; ValueData: "PreviewBrowserHTML"

; 3. Register under StartMenuInternet (Required to appear in Windows Default Apps)
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\PreviewBrowser"; ValueType: string; ValueName: ""; ValueData: "{#MyAppName}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\PreviewBrowser\Capabilities"; ValueType: string; ValueName: "ApplicationName"; ValueData: "{#MyAppName}"
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\PreviewBrowser\Capabilities"; ValueType: string; ValueName: "ApplicationDescription"; ValueData: "Preview Browser Link Router"
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\PreviewBrowser\Capabilities\URLAssociations"; ValueType: string; ValueName: "http"; ValueData: "PreviewBrowserHTML"
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\PreviewBrowser\Capabilities\URLAssociations"; ValueType: string; ValueName: "https"; ValueData: "PreviewBrowserHTML"
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\PreviewBrowser\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppIconName}"
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\PreviewBrowser\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"""

; 4. Add to RegisteredApplications so Windows Settings indexes it
Root: HKCU; Subkey: "Software\RegisteredApplications"; ValueType: string; ValueName: "PreviewBrowser"; ValueData: "Software\PreviewBrowser\Capabilities"; Flags: uninsdeletevalue

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIconName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#DoubleAmp(MyAppName)}}"; Flags: nowait postinstall skipifsilent
Filename: "ms-settings:defaultapps?registeredAppUser=PreviewBrowser"; Description: "Open Windows Settings to set {#MyAppName} as your default browser. This must be done for the app to work."; Flags: shellexec nowait postinstall skipifsilent