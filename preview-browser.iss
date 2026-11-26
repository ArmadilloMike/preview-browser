#define MyAppName "Preview Browser"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "ArmadilloMike.Dev"
#define MyAppURL "https://github.com/ArmadilloMike/preview-browser"
#define MyAppExeName "link-handler.exe"
#define DoubleAmp(Value) StringChange(Value, "&", "&&")
#define EscapeConstArgument(Value) StringChange(StringChange(StringChange(Value, "%", "%25"), ",", "%2c"), "}", "%7d")

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppId={{6A4C0185-DF5B-470D-8BF8-132FD7C12B0B}
;AppVerName={cm:NameAndVersion,{#EscapeConstArgument(MyAppName)},{#EscapeConstArgument(MyAppVersion)}}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
; "ArchitecturesAllowed=x64compatible" specifies that Setup cannot run on anything but x64 and Windows 11 on Arm.
ArchitecturesAllowed=x64compatible
; "ArchitecturesInstallIn64BitMode=x64compatible" requests that the install be done in "64-bit mode" on x64 or Windows 11 on Arm.
; This means it should use the native 64-bit Program Files directory and the 64-bit view of the registry.
ArchitecturesInstallIn64BitMode=x64compatible
; Uncomment the following line to use a 64-bit installer.
SetupArchitecture=x64
DisableProgramGroupPage=yes
LicenseFile=C:\Users\1744304\PycharmProjects\preview-browser\license.txt
; Remove the following line to run in administrative install mode (install for all users).
PrivilegesRequired=lowest
OutputBaseFilename=previewbrowser
SolidCompression=yes
WizardStyle=modern windows11

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "C:\Users\1744304\PycharmProjects\preview-browser\dist\link-handler\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\1744304\PycharmProjects\preview-browser\dist\preview-browser\preview-browser.exe"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files.

[Registry]
; 1. Define the URL Protocol Handler (ProgID)
Root: HKCU; Subkey: "Software\Classes\PreviewBrowserHTML"; ValueType: string; ValueName: ""; ValueData: "Preview Browser Document"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\PreviewBrowserHTML"; ValueType: string; ValueName: "URL Protocol"; ValueData: ""
Root: HKCU; Subkey: "Software\Classes\PreviewBrowserHTML\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\link-router.exe,0"
Root: HKCU; Subkey: "Software\Classes\PreviewBrowserHTML\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\link-router.exe"" ""%1"""

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
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\PreviewBrowser\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\link-router.exe,0"
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\PreviewBrowser\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\link-router.exe"""

; 4. Add to RegisteredApplications so Windows Settings indexes it
Root: HKCU; Subkey: "Software\RegisteredApplications"; ValueType: string; ValueName: "PreviewBrowser"; ValueData: "Software\PreviewBrowser\Capabilities"; Flags: uninsdeletevalue


[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#DoubleAmp(MyAppName)}}"; Flags: nowait postinstall skipifsilent