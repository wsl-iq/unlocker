@echo off
setlocal
set "exePath=%~dp0unlocker.py"
set "shortcutPath=%USERPROFILE%\Desktop\Unlocker.lnk"
powershell -command "$ws=New-Object -ComObject WScript.Shell; $sc=$ws.CreateShortcut('%shortcutPath%'); $sc.TargetPath='%exePath%'; $sc.WorkingDirectory='%~dp0'; $sc.Save()"
echo Shortcut created successfully on Desktop as Unlocker.lnk
pause