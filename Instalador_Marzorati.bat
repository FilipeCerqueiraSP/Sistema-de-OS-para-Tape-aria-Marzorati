@echo off
REM =====================================================
REM INSTALADOR AUTOMATICO: PostgreSQL 18 + Banco Marzorati + App + Atalho
REM =====================================================

REM --- CONFIGURAÇÕES ---
set POSTGRES_EXE=%~dp0postgresql-18.6-1-windows-x64.exe
set POSTGRES_DIR=C:\Program Files\PostgreSQL\18
set POSTGRES_DATA=%POSTGRES_DIR%\data
set POSTGRES_PASSWORD=0000
set POSTGRES_PORT=5432

set BANCO_NOME=Marzorati
set SCRIPT_SQL=%~dp0script.sql
set APP_EXE=%~dp0Marzorati.exe
set SHORTCUT=%USERPROFILE%\Desktop\Marzorati.lnk

REM --- 1. Instalar PostgreSQL se não existir ---
if not exist "%POSTGRES_DIR%\bin\psql.exe" (
    echo Instalando PostgreSQL para o banco de dados...
    "%POSTGRES_EXE%" --mode unattended --superpassword "%POSTGRES_PASSWORD%" --servicename "postgresql-x64-18" --serverport %POSTGRES_PORT% --datadir "%POSTGRES_DATA%"
) else (
    echo PostgreSQL ja instalado.
)

REM --- 2. Iniciar serviço PostgreSQL ---
echo Iniciando servico PostgreSQL...
net start "postgresql-x64-18" 2>nul

REM --- 3. Esperar o serviço existir e estar rodando ---
echo Aguardando PostgreSQL ficar online...
:CheckServiceExist
sc query "postgresql-x64-18" >nul 2>&1
if errorlevel 1 (
    timeout /t 5 >nul
    goto CheckServiceExist
)

:CheckServiceRunning
sc query "postgresql-x64-18" | find "RUNNING" >nul
if errorlevel 1 (
    timeout /t 5 >nul
    goto CheckServiceRunning
)

REM --- 4. Definir senha para psql ---
set PGPASSWORD=%POSTGRES_PASSWORD%

REM --- 5. Esperar servidor aceitar conexões ---
echo Aguardando PostgreSQL aceitar conexoes...
:CheckDB
"%POSTGRES_DIR%\bin\psql.exe" -U postgres -d postgres -tAc "SELECT 1" >nul 2>&1
if errorlevel 1 (
    timeout /t 5 >nul
    goto CheckDB
)

REM --- 6. Criar banco Marzorati se nao existir ---
echo Verificando se o banco %BANCO_NOME% existe...
"%POSTGRES_DIR%\bin\psql.exe" -U postgres -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='%BANCO_NOME%'" | findstr 1 >nul
if errorlevel 1 (
    echo Criando banco de dados %BANCO_NOME%...
    "%POSTGRES_DIR%\bin\psql.exe" -U postgres -d postgres -c "CREATE DATABASE \"%BANCO_NOME%\";"
) else (
    echo Banco %BANCO_NOME% ja existe.
)

REM --- 7. Rodar script SQL ---
echo Executando script SQL para criar tabelas...
"%POSTGRES_DIR%\bin\psql.exe" -U postgres -d "%BANCO_NOME%" -f "%SCRIPT_SQL%"

REM --- 8. Rodar aplicacao ---
echo Abrindo aplicacao...
start "" "%APP_EXE%"



echo =====================================================
echo Instalacao concluida. Voce pode usar o atalho na area de trabalho.
pause
