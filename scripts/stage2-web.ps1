param([switch]$SkipInstall)
$ErrorActionPreference = 'Stop'
$stageRoot = Split-Path -Parent $PSScriptRoot
$stagePnpm = Get-Command pnpm -ErrorAction SilentlyContinue
if ($stagePnpm) {
    $stagePnpmPath = $stagePnpm.Source
} else {
    $stagePnpmPath = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\fallback\pnpm.cmd'
}
if (-not (Test-Path -LiteralPath $stagePnpmPath)) { throw '需要Node22.12+与pnpm11.25.0；参见阶段2运行手册。' }
Push-Location -LiteralPath (Join-Path $stageRoot 'web')
try {
    if (-not $SkipInstall) {
        & $stagePnpmPath install --frozen-lockfile
        if ($LASTEXITCODE -ne 0) { throw '前端依赖安装失败。' }
    }
    & $stagePnpmPath run build
    if ($LASTEXITCODE -ne 0) { throw '前端类型检查或构建失败。' }
} finally { Pop-Location }
