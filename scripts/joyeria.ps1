[CmdletBinding()]
param(
    [ValidateSet('start', 'stop', 'status')]
    [string]$Action = 'start'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path $root 'backend'
$frontendApp = Join-Path $root 'frontend\app.py'
$stateDir = Join-Path $root '.runtime'
$apiPidFile = Join-Path $stateDir 'api.json'
$appPidFile = Join-Path $stateDir 'streamlit.json'
$apiPort = 3000
$appPort = 8501

function Get-ListenerIds([int]$Port) {
    $connections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if (-not $connections) {
        return @()
    }
    return @($connections | Select-Object -ExpandProperty OwningProcess -Unique)
}

function Get-ProcessDetails([int]$Id) {
    return Get-CimInstance Win32_Process -Filter "ProcessId = $Id" -ErrorAction SilentlyContinue
}

function Test-ExpectedProcess($Process, [string]$Service) {
    if (-not $Process) {
        return $false
    }

    $command = [string]$Process.CommandLine
    $executable = [string]$Process.ExecutablePath
    if ($Service -eq 'api') {
        $node = Get-Command node.exe -ErrorAction SilentlyContinue
        return $node -and $executable -ieq $node.Source -and $command -match '(?i)\bserver\.js\b'
    }

    $python = Get-Command python.exe -ErrorAction SilentlyContinue
    return $python -and $executable -ieq $python.Source -and
        $command -match '(?i)-m\s+streamlit\s+run.*app\.py' -and
        $command -match '(?i)--server\.port\s+8501'
}

function Write-ProcessRecord([int]$Id, [string]$File) {
    $process = Get-Process -Id $Id -ErrorAction Stop
    $details = Get-ProcessDetails $Id
    if (-not $details) {
        throw "No se pudo identificar el proceso $Id."
    }

    $record = [pscustomobject]@{
        pid = $Id
        startTimeUtcTicks = $process.StartTime.ToUniversalTime().Ticks
        executablePath = [string]$details.ExecutablePath
        commandLine = [string]$details.CommandLine
    }
    $record | ConvertTo-Json | Set-Content -LiteralPath $File -Encoding UTF8
}

function Test-ProcessRecord([string]$File, [string]$Service) {
    if (-not (Test-Path -LiteralPath $File)) {
        return $false
    }

    try {
        $record = Get-Content -LiteralPath $File -Raw | ConvertFrom-Json
        $process = Get-Process -Id ([int]$record.pid) -ErrorAction Stop
        $details = Get-ProcessDetails ([int]$record.pid)
        if (-not $details -or
            $process.StartTime.ToUniversalTime().Ticks -ne [long]$record.startTimeUtcTicks -or
            [string]$details.ExecutablePath -ine [string]$record.executablePath -or
            [string]$details.CommandLine -cne [string]$record.commandLine) {
            return $false
        }
        return Test-ExpectedProcess $details $Service
    } catch {
        return $false
    }
}

function Start-ManagedService(
    [string]$Service,
    [int]$Port,
    [string]$PidFile
) {
    if (Test-ProcessRecord $PidFile $Service) {
        Write-Host "$Service ya está iniciado por este controlador."
        return
    }

    $listenerIds = Get-ListenerIds $Port
    if ($listenerIds.Count -gt 0) {
        if ($listenerIds.Count -ne 1) {
            throw "El puerto $Port tiene varios procesos. No se inició $Service."
        }
        $existing = Get-ProcessDetails ([int]$listenerIds[0])
        if (-not (Test-ExpectedProcess $existing $Service)) {
            throw "El puerto $Port ya está ocupado por otro proceso; no se modificó."
        }
        Write-ProcessRecord ([int]$listenerIds[0]) $PidFile
        Write-Host "$Service ya estaba activo; quedó registrado para poder detenerlo."
        return
    }

    if ($Service -eq 'api') {
        $executable = (Get-Command node.exe -ErrorAction Stop).Source
        $stdout = Join-Path $stateDir 'api.log'
        $stderr = Join-Path $stateDir 'api-error.log'
        $process = Start-Process `
            -FilePath $executable `
            -ArgumentList 'server.js' `
            -WorkingDirectory $backendDir `
            -WindowStyle Hidden `
            -RedirectStandardOutput $stdout `
            -RedirectStandardError $stderr `
            -PassThru
    } else {
        $executable = (Get-Command python.exe -ErrorAction Stop).Source
        $stdout = Join-Path $stateDir 'streamlit.log'
        $stderr = Join-Path $stateDir 'streamlit-error.log'
        $arguments = "-m streamlit run `"$frontendApp`" --server.port $appPort --server.headless true --server.runOnSave true"
        $process = Start-Process `
            -FilePath $executable `
            -ArgumentList $arguments `
            -WorkingDirectory $root `
            -WindowStyle Hidden `
            -RedirectStandardOutput $stdout `
            -RedirectStandardError $stderr `
            -PassThru
    }

    Start-Sleep -Milliseconds 500
    Write-ProcessRecord $process.Id $PidFile

    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        if ((Get-ListenerIds $Port).Count -gt 0) {
            Write-Host "$Service iniciado en el puerto $Port."
            return
        }
        if (-not (Get-Process -Id $process.Id -ErrorAction SilentlyContinue)) {
            break
        }
        Start-Sleep -Seconds 1
    }

    if (Test-Path -LiteralPath $stderr) {
        Get-Content -LiteralPath $stderr -Tail 10
    }
    if (Test-Path -LiteralPath $stdout) {
        Get-Content -LiteralPath $stdout -Tail 10
    }
    throw "$Service no abrió el puerto $Port. Revisa los registros en .runtime."
}

function Stop-ManagedService([string]$Service, [int]$Port, [string]$PidFile) {
    if (-not (Test-ProcessRecord $PidFile $Service)) {
        $listenerIds = Get-ListenerIds $Port
        if ($listenerIds.Count -eq 1) {
            $existing = Get-ProcessDetails ([int]$listenerIds[0])
            if (Test-ExpectedProcess $existing $Service) {
                Write-ProcessRecord ([int]$listenerIds[0]) $PidFile
            }
        }
    }

    if (-not (Test-ProcessRecord $PidFile $Service)) {
        if (Test-Path -LiteralPath $PidFile) {
            Remove-Item -LiteralPath $PidFile -Force
        }
        Write-Host "$Service no está iniciado (o no pertenece a esta aplicación)."
        return
    }

    $record = Get-Content -LiteralPath $PidFile -Raw | ConvertFrom-Json
    Stop-Process -Id ([int]$record.pid) -Force
    Remove-Item -LiteralPath $PidFile -Force
    Write-Host "$Service detenido."
}

if ($Action -eq 'status') {
    Write-Host "API (3000): $(if ((Get-ListenerIds $apiPort).Count) { 'activa' } else { 'detenida' })"
    Write-Host "Tienda (8501): $(if ((Get-ListenerIds $appPort).Count) { 'activa' } else { 'detenida' })"
    exit 0
}

if (-not (Test-Path -LiteralPath $stateDir)) {
    New-Item -ItemType Directory -Path $stateDir -Force | Out-Null
}

if ($Action -eq 'start') {
    if (-not (Test-Path -LiteralPath (Join-Path $backendDir '.env'))) {
        throw "Falta backend\.env. Configura primero las variables locales del backend."
    }
    Start-ManagedService 'api' $apiPort $apiPidFile
    Start-ManagedService 'streamlit' $appPort $appPidFile
    Start-Process "http://localhost:$appPort"
    exit 0
}

Stop-ManagedService 'streamlit' $appPort $appPidFile
Stop-ManagedService 'api' $apiPort $apiPidFile
exit 0
