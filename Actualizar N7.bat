@echo off
echo Fecha:%date%
echo Hora:%time%
color 0B
echo ================================================================
echo. 
echo                     =   'Carga de Datos N7'   =
echo.                         Grado Academico
echo. 
echo ================================================================
echo.
echo.
cd C:\carga_inpe2020\0_scripts
"C:\Program Files\Python39\python.exe" n7_update.py

echo Fecha:%date%
echo Hora:%time%
PAUSE
echo.
echo.
echo Para salir presiona una tecla.
pause>nul
exit

