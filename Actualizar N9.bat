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

"C:\Program Files\Python39\python.exe" n9_update.py

echo Fecha:%date%
echo Hora:%time%
PAUSE
echo.
echo.
echo Para salir presiona una tecla.
pause>nul
exit

