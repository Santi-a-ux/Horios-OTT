@echo off
REM Script para instalar dependencias y correr el servidor

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ✅ Dependencias instaladas
echo.
echo Para iniciar el servidor, ejecuta:
echo   uvicorn main:app --reload
