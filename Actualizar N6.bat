@echo off
echo Fecha:%date%
echo Hora:%time%
color 0B
echo ================================================================
echo. 
echo                  =   'Carga de Datos N6'   =
echo.         Poblacion Extranjera por situcion juridica
echo. 
echo ================================================================
echo.
echo.

"C:\Program Files\Python39\python.exe" n6_update.py

echo Fecha:%date%
echo Hora:%time%
PAUSE
echo.
echo.
echo Para salir presiona una tecla.
pause>nul
exit

