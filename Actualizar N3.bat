@echo off
echo Fecha:%date%
echo Hora:%time%
color 0B
echo ================================================================
echo. 
echo                  =   'Carga de Datos N3'   =
echo.                       Rango de Edades
echo. 
echo ================================================================
echo.
echo.
cd C:\Users\lcarv\OneDrive\repos_git\ModelingAndUpdate_GISData\0_scripts
"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" n3_update.py

echo Fecha:%date%
echo Hora:%time%
PAUSE
echo.
echo.
echo Para salir presiona una tecla.
pause>nul
exit



