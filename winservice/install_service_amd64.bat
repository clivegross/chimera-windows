@echo off

rem install Chimera Backup Agent as Windows service for 64-bit machines

set relpath=Chimera\Chimera Backup Agent
set app=chimera.exe
set servicename=chimera-backup-agent
set displayname=Chimera Backup Agent
set description=Runs scheduled jobs to backup files to the cloud.

echo "%programfiles(x86)%\%relpath%\%app%"

echo nssm install %servicename% "%programfiles(x86)%\%relpath%\%app%"
nssm install %servicename% "%programfiles(x86)%\%relpath%\%app%"

echo nssm set %servicename% Application "%programfiles(x86)%\%relpath%\%app%"
nssm set %servicename% Application "%programfiles(x86)%\%relpath%\%app%"

echo nssm set %servicename% AppDirectory "%programfiles(x86)%\%relpath%"
nssm set %servicename% AppDirectory "%programfiles(x86)%\%relpath%"

echo nssm set %servicename% DisplayName "%displayname%"
nssm set %servicename% DisplayName "%displayname%"

echo nssm set %servicename% Description "%description%"
nssm set %servicename% Description "%description%"

nssm set %servicename% Start SERVICE_AUTO_START
nssm set %servicename% AppExit Default Exit