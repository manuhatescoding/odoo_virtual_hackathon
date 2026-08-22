$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$envFile = Join-Path $PSScriptRoot 'backend\.env'
if (Test-Path $envFile) {
	Get-Content $envFile | ForEach-Object {
		if ($_ -match '^\s*([^#][^=]*)=(.*)$') {
			[Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim())
		}
	}
}
$hostAddress = if ($env:HOST) { $env:HOST } else { '0.0.0.0' }
$port = if ($env:PORT) { $env:PORT } else { '8000' }
python -m uvicorn app.main:app --app-dir backend --host $hostAddress --port $port --reload
