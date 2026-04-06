@echo off
echo Construindo o pacote do BotCity...

rem Remove o arquivo .zip antigo se existir
if exist "bot.zip" del "bot.zip"

rem Usa o PowerShell para compactar os arquivos necessarios para o BotCity Maestro
powershell -command "Compress-Archive -Path 'bot.py', 'src', 'requirements.txt' -DestinationPath 'bot.zip' -Force"

echo ========================================
echo Build concluido com sucesso!
echo Envie o arquivo bot.zip para o BotCity Maestro.
echo ========================================
pause
