<# 本机便携开发助手：只操作仓库.local中的专用集群，不安装Windows服务。
setup首次创建随机本机密码；配置留在忽略目录，不打印或提交。
后续start/migrate/test/serve沿用该集群。stop只停止该目录的数据库进程。
#>
param(
    [ValidateSet('setup', 'start', 'stop', 'migrate', 'test', 'serve', 'replay')]
    [string]$Action = 'serve',
    [switch]$Live
)
$ErrorActionPreference = 'Stop'
$stageRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $stageRoot
$stageLocal = Join-Path $stageRoot '.local'
$stageBin = Join-Path $stageLocal 'stage2-postgres\pgsql\bin'
$stageData = Join-Path $stageLocal 'stage2-pgdata'
$stageConfig = Join-Path $stageLocal 'stage2-runtime.json'
$stagePython = Join-Path $stageRoot '.venv-py312\Scripts\python.exe'
$stageLog = Join-Path $stageLocal 'stage2-postgres.log'

if ($Action -eq 'setup') {
    if (Test-Path -LiteralPath $stageConfig) { throw '已有本机配置，使用start；setup不覆盖。' }
    if (Test-Path -LiteralPath $stageData) { throw '已有数据目录，setup不覆盖。' }
    if (-not (Test-Path -LiteralPath (Join-Path $stageBin 'initdb.exe'))) {
        throw '先按docs/STAGE2_RUNBOOK.md下载并解压便携PostgreSQL到.local/stage2-postgres。'
    }
    $stagePassword = [Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(24))
    $stagePwFile = Join-Path $stageLocal 'stage2-init-password.tmp'
    [IO.File]::WriteAllText($stagePwFile, $stagePassword)
    try {
        & (Join-Path $stageBin 'initdb.exe') -D $stageData -U stage2_local -A scram-sha-256 --pwfile=$stagePwFile --encoding=UTF8 --locale=C
        if ($LASTEXITCODE -ne 0) { throw '初始化失败。' }
    } finally { Remove-Item -LiteralPath $stagePwFile -ErrorAction SilentlyContinue }
    Add-Content -LiteralPath (Join-Path $stageData 'postgresql.conf') -Value "`nlisten_addresses = '127.0.0.1'`nport = 55432"
    @{ user = 'stage2_local'; password = $stagePassword; port = 55432 } |
        ConvertTo-Json | Set-Content -LiteralPath $stageConfig -Encoding utf8
    $Action = 'start'
}
if (-not (Test-Path -LiteralPath $stageConfig)) { throw '缺少本机配置，先执行setup。' }
$stageSettings = Get-Content -LiteralPath $stageConfig -Raw | ConvertFrom-Json
$env:PGPASSWORD = $stageSettings.password
$env:STAGE2_DATABASE_URL = "postgresql+psycopg://stage2_local:$($stageSettings.password)@127.0.0.1:55432/fujian_stage2_dev"
$env:STAGE2_TEST_DATABASE_URL = "postgresql+psycopg://stage2_local:$($stageSettings.password)@127.0.0.1:55432/fujian_stage2_test"

try {
    if ($Action -eq 'start') {
        & (Join-Path $stageBin 'pg_ctl.exe') status -D $stageData *> $null
        if ($LASTEXITCODE -ne 0) {
            # Start-Process -Wait会等待整个子进程树，数据库常驻会让它一直等待。
            # WaitForExit只等待pg_ctl启动助手，不等待已启动的postgres常驻进程。
            $stageProcess = Start-Process -FilePath (Join-Path $stageBin 'pg_ctl.exe') -ArgumentList @('start', '-D', ('"' + $stageData + '"'), '-l', ('"' + $stageLog + '"'), '-w') -WindowStyle Hidden -PassThru
            if (-not $stageProcess.WaitForExit(60000)) { throw '启动等待超时，检查数据库启动日志。' }
            if ($stageProcess.ExitCode -ne 0) { throw '启动失败，检查.local/stage2-postgres.log。' }
        }
        foreach ($stageDb in @('fujian_stage2_dev', 'fujian_stage2_test')) {
            $stageExists = & (Join-Path $stageBin 'psql.exe') -h 127.0.0.1 -p 55432 -U stage2_local -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$stageDb'"
            if ($LASTEXITCODE -ne 0) { throw '数据库连接失败。' }
            if ($stageExists -ne '1') {
                & (Join-Path $stageBin 'createdb.exe') -h 127.0.0.1 -p 55432 -U stage2_local $stageDb
                if ($LASTEXITCODE -ne 0) { throw '创建专用开发库失败。' }
            }
        }
        Write-Host '本机PostgreSQL已启动；开发/测试库就绪，连接凭证未输出。'
    } elseif ($Action -eq 'stop') {
        & (Join-Path $stageBin 'pg_ctl.exe') stop -D $stageData -m fast
        if ($LASTEXITCODE -ne 0) { throw '停止失败。' }
    } elseif ($Action -eq 'migrate') {
        & $stagePython -m alembic upgrade head
        if ($LASTEXITCODE -ne 0) { throw '迁移失败。' }
    } elseif ($Action -eq 'test') {
        $env:STAGE2_DATABASE_URL = $env:STAGE2_TEST_DATABASE_URL
        & $stagePython -m alembic upgrade head
        if ($LASTEXITCODE -ne 0) { throw '测试库迁移失败。' }
        & $stagePython -X utf8 -m pytest tests -q
        if ($LASTEXITCODE -ne 0) { throw '测试未通过。' }
    } elseif ($Action -eq 'replay') {
        & $stagePython -X utf8 -m learning_app.cli replay --demo
        if ($LASTEXITCODE -ne 0) { throw '回放失败。' }
    } elseif ($Action -eq 'serve') {
        $stageArgs = @('-X', 'utf8', '-m', 'learning_app.cli', 'serve', '--demo')
        if ($Live) { $stageArgs += '--live' }
        & $stagePython @stageArgs
        if ($LASTEXITCODE -ne 0) { throw '服务退出异常。' }
    }
} finally {
    Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
    Remove-Item Env:STAGE2_DATABASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:STAGE2_TEST_DATABASE_URL -ErrorAction SilentlyContinue
}
