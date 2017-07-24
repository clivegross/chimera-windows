@echo off

rem install Chimera Backup Agent as Windows service for 32-bit machines

set relpath=Chimera\Chimera Backup Agent
set app=chimera.exe
set servicename=chimera-backup-agent
set displayname=Chimera Backup Agent
set description=Runs scheduled jobs to backup files to the cloud.

echo "%programfiles%\%relpath%\%app%"

echo nssm install %servicename% "%programfiles%\%relpath%\%app%"
nssm install %servicename% "%programfiles%\%relpath%\%app%"

echo nssm set %servicename% Application "%programfiles%\%relpath%\%app%"
nssm set %servicename% Application "%programfiles%\%relpath%\%app%"

echo nssm set %servicename% AppDirectory "%programfiles%\%relpath%"
nssm set %servicename% AppDirectory "%programfiles%\%relpath%"

echo nssm set %servicename% DisplayName "%displayname%"
nssm set %servicename% DisplayName "%displayname%"

echo nssm set %servicename% Description "%description%"
nssm set %servicename% Description "%description%"

nssm set %servicename% Start SERVICE_AUTO_START
nssm set %servicename% AppExit Default Exit