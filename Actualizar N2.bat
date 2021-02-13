@echo off
echo Fecha:%date%
echo Hora:%time%
color 0B
echo ================================================================
echo. 
echo                   =   'Carga de Datos N2'   =
echo.            Capacidad, Poblacion Penal y Hacinamiento
echo. 
echo ================================================================
echo.
echo.
cd C:\carga_inpe2020\0_scripts
"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" n2_update.py

echo Fecha:%date%
echo Hora:%time%
PAUSE
echo.
echo.
echo Para salir presiona una tecla.
pause>nul
exit

