# Dip watcher: polls quotes every ~15 min during market hours (Task Scheduler) and launches a
# Claude trigger run ONLY when a watched condition fires. Costs nothing while nothing happens.
#
# Conditions (config: _tools/dip_watch_config.json, maintained by the trading runs):
#   buy_watch  [symbols]        -> fires when live <= 1.03 * prior close (name became buyable)
#   stop_watch {symbol: cost}   -> fires when live <= 0.75 * avg cost   (-25% stop breached)
#   dip3_watch {symbol: t1fill} -> fires when live <= 0.95 * tranche-1 fill (tranche-3 eligible)
# Each condition fires at most once per day (state: dip_watch_state.json).
# -DryRun: evaluate and print, but never write state or launch Claude.
param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$repo = Split-Path $PSScriptRoot -Parent
Set-Location $repo
$cfgPath = Join-Path $PSScriptRoot "dip_watch_config.json"
$statePath = Join-Path $PSScriptRoot "dip_watch_state.json"
$lockPath = Join-Path $PSScriptRoot "dip_watch.lock"

if (-not (Test-Path $cfgPath)) { exit 0 }

# Market-hours window guard (local = PT): weekdays 06:55-12:40, between the two main runs.
$now = Get-Date
if (-not $DryRun) {
    if ($now.DayOfWeek -eq 'Saturday' -or $now.DayOfWeek -eq 'Sunday') { exit 0 }
    $mins = $now.Hour * 60 + $now.Minute
    if ($mins -lt 415 -or $mins -gt 760) { exit 0 }
}

# One trigger run at a time; a stale lock (>45 min) is assumed crashed.
if (Test-Path $lockPath) {
    $age = (Get-Date) - (Get-Item $lockPath).LastWriteTime
    if ($age.TotalMinutes -lt 45) { exit 0 } else { Remove-Item $lockPath -Force -Confirm:$false }
}

$cfg = Get-Content $cfgPath -Raw -Encoding UTF8 | ConvertFrom-Json
$today = Get-Date -Format "yyyy-MM-dd"
$fired = @()
if (Test-Path $statePath) {
    $s = Get-Content $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($s.date -eq $today) { $fired = @($s.triggered) }
}

function Get-Quote([string]$sym) {
    $u = "https://query1.finance.yahoo.com/v8/finance/chart/$($sym)?interval=1d&range=1d"
    try {
        $r = Invoke-RestMethod -Uri $u -Headers @{ "User-Agent" = "Mozilla/5.0" } -TimeoutSec 15
        $m = $r.chart.result[0].meta
        [pscustomobject]@{ price = [double]$m.regularMarketPrice; prevClose = [double]$m.chartPreviousClose }
    } catch { $null }
}

$buyWatch = @(); if ($cfg.buy_watch) { $buyWatch = @($cfg.buy_watch) }
$stopProps = @(); if ($cfg.stop_watch) { $stopProps = @($cfg.stop_watch.PSObject.Properties) }
$dip3Props = @(); if ($cfg.dip3_watch) { $dip3Props = @($cfg.dip3_watch.PSObject.Properties) }

$symbols = @($buyWatch) + @($stopProps | ForEach-Object { $_.Name }) + @($dip3Props | ForEach-Object { $_.Name }) | Select-Object -Unique
$quotes = @{}
foreach ($s in $symbols) {
    $q = Get-Quote $s
    if ($q -and $q.price -gt 0 -and $q.prevClose -gt 0) { $quotes[$s] = $q }
    Start-Sleep -Milliseconds 300
}

$triggers = @()
foreach ($s in $buyWatch) {
    $k = "$s-buy"
    if ($fired -contains $k -or -not $quotes.ContainsKey($s)) { continue }
    $q = $quotes[$s]
    if ($q.price -le 1.03 * $q.prevClose) {
        $triggers += "$s became buyable: live $($q.price) is within 3% of prior close $($q.prevClose) (unfilled tranche/starter)"
        $fired += $k
    }
}
foreach ($p in $stopProps) {
    $k = "$($p.Name)-stop"
    if ($fired -contains $k -or -not $quotes.ContainsKey($p.Name)) { continue }
    $q = $quotes[$p.Name]
    if ($q.price -le 0.75 * [double]$p.Value) {
        $triggers += "$($p.Name) breached the -25% stop: live $($q.price) vs avg cost $($p.Value)"
        $fired += $k
    }
}
foreach ($p in $dip3Props) {
    $k = "$($p.Name)-dip3"
    if ($fired -contains $k -or -not $quotes.ContainsKey($p.Name)) { continue }
    $q = $quotes[$p.Name]
    if ($q.price -le 0.95 * [double]$p.Value) {
        $triggers += "$($p.Name) pulled back >=5% from its tranche-1 fill $($p.Value): live $($q.price) - tranche-3 add eligible"
        $fired += $k
    }
}

if ($DryRun) {
    "Quotes:"; foreach ($s in $quotes.Keys) { "  $s live=$($quotes[$s].price) prevClose=$($quotes[$s].prevClose)" }
    if ($triggers.Count -eq 0) { "No triggers." } else { "WOULD TRIGGER:"; $triggers | ForEach-Object { "  - $_" } }
    exit 0
}

@{ date = $today; triggered = $fired } | ConvertTo-Json | Out-File $statePath -Encoding utf8
if ($triggers.Count -eq 0) { exit 0 }

New-Item -ItemType File -Path $lockPath -Force | Out-Null
try {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $hm = Get-Date -Format "HHmm"
    New-Item -ItemType Directory -Force -Path (Join-Path $repo "briefs/transcripts") | Out-Null
    $reasonBlock = ($triggers | ForEach-Object { "- $_" }) -join "`n"
    $prompt = @"
You are a DIP-WATCH TRIGGER run (started $stamp local, America/Los_Angeles) for the AI
supply-chain trading experiment in this repo. The quote watcher fired on:

$reasonBlock

1. Read TRADING-POLICY.md and obey it exactly (status flag, hard limits, guards, Directives).
2. Verify each trigger against LIVE Robinhood quotes (the watcher uses delayed data) - act only
   if the condition truly holds at live prices.
3. Act ONLY on the triggering condition(s) plus any urgent risk you notice (stops, circuit
   breaker). This is NOT a full slot run: no discovery, no reflection, no other opening buys.
4. Log every order/fill in trading_log.csv. Write a short brief to briefs/$today-dipwatch-$hm.md.
   After any fill, update _tools/dip_watch_config.json (remove filled buy_watch names, add new
   positions to stop_watch with avg cost).
5. If you executed any order OR anything urgent happened, email the brief: run
   powershell -NoProfile -ExecutionPolicy Bypass -File _tools/send_digest.ps1 -BriefPath briefs/$today-dipwatch-$hm.md -Slot dipwatch
6. If a trigger does not hold at live prices, do nothing and note it in the brief.

Finish with a one-paragraph plain-language summary.
"@
    & claude -p $prompt `
        --model "claude-opus-4-8" `
        --allowed-tools "Read,Write,Edit,Glob,Grep,Bash,WebSearch,WebFetch,mcp__claude_ai_robinhood,mcp__claude_ai_Gmail" `
        --max-turns 80 |
        Out-File -FilePath (Join-Path $repo "briefs/transcripts/$today-dipwatch-$hm.txt") -Encoding utf8
}
finally {
    Remove-Item $lockPath -Force -Confirm:$false
}
exit 0
