@echo off
rem Tenta ativar o ambiente virtual (venv) se ele existir
if exist "venv\Scripts\activate.bat" call "venv\Scripts\activate.bat"

echo Iniciando o download de dados (Automacao web)...
python src\download_dados.py

if %errorlevel% neq 0 (
    echo Ocorreu um erro durante o download dos dados.
    pause
    exit /b %errorlevel%
)

echo Iniciando o processamento dos dados e geracao dos graficos...
python src\main.py

if %errorlevel% neq 0 (
    echo Ocorreu um erro durante o processamento.
    pause
    exit /b %errorlevel%
)

echo Processamento concluido com sucesso! Abrindo o mapa de calor...
start "" "output\graficos\mapa_calor_queimadas.html"
pause
