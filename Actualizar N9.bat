@echo off
echo Fecha:%date%
echo Hora:%time%
color 0B
echo ================================================================
echo. 
echo                     =   'Carga de Datos N9'   =
echo.                    Ingreso por Delito Especifico
echo. 
echo ================================================================
echo.
echo.
cd C:\Users\lcarv\OneDrive\repos_git\ModelingAndUpdate_GISData\0_scripts
"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" n9_update.py

echo Fecha:%date%
echo Hora:%time%
PAUSE
echo.
echo.
echo Para salir presiona una tecla.
pause>nul
exit

