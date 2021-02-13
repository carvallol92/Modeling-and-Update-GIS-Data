@echo off
echo Fecha:%date%
echo Hora:%time%
color 0B
echo ================================================================
echo. 
echo                     =   'Backup y Mantenimiento'   =
echo.                    
echo. 
echo ================================================================
echo.
echo.

"C:\Program Files\Python39\python.exe" nx_backup_mantenimiento.py

echo Fecha:%date%
echo Hora:%time%
PAUSE
echo.
echo.
echo Para salir presiona una tecla.
pause>nul
exit

