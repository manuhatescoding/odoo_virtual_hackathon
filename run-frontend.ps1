$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
npm.cmd --prefix frontend run dev -- --host 0.0.0.0
