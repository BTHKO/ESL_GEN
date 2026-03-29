# HKO ESL - Deploy & Test All Workers
# Run from: C:\Users\hkome\Desktop\Project\
# Command:  cd C:\Users\hkome\Desktop\Project; .\DEPLOY_AND_TEST.ps1

Set-StrictMode -Off
$ErrorActionPreference = "Continue"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " HKO ESL Worker Deploy & Test" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# ── STEP 1: Show what JS files exist ──────────────────────────
Write-Host "`n[1] Worker files found:" -ForegroundColor Yellow
Get-ChildItem "C:\Users\hkome\Desktop\Project\*.js" | ForEach-Object {
    Write-Host "  $($_.Name)" -ForegroundColor White
}

# ── STEP 2: Read wrangler.toml ────────────────────────────────
Write-Host "`n[2] Current wrangler.toml:" -ForegroundColor Yellow
Get-Content "C:\Users\hkome\Desktop\Project\wrangler.toml"

# ── STEP 3: Show deployed workers and their URLs ──────────────
Write-Host "`n[3] Checking deployed worker URLs..." -ForegroundColor Yellow

$workers = @("hko-imager", "hko-audio", "hko-converter")
$urls = @{}

foreach ($w in $workers) {
    $url = "https://$w.mrhkruger.workers.dev"
    $urls[$w] = $url
    try {
        $r = Invoke-WebRequest -Uri "$url/" -Method GET -TimeoutSec 8 -ErrorAction SilentlyContinue
        Write-Host "  $w => $url [HTTP $($r.StatusCode)]" -ForegroundColor Green
    } catch {
        $code = $_.Exception.Response.StatusCode.value__
        if ($code) {
            Write-Host "  $w => $url [HTTP $code - responding but needs config]" -ForegroundColor Yellow
        } else {
            Write-Host "  $w => $url [DNS FAIL - not deployed or wrong subdomain]" -ForegroundColor Red
        }
    }
}

# ── STEP 4: Show content of each worker JS ────────────────────
Write-Host "`n[4] Worker source file heads (first 5 lines each):" -ForegroundColor Yellow
$jsFiles = @(
    "C:\Users\hkome\Desktop\Project\content-generator.js",
    "C:\Users\hkome\Desktop\Project\media-generator.js",
    "C:\Users\hkome\Desktop\Project\generate.js",
    "C:\Users\hkome\Desktop\Project\lms.js"
)
foreach ($f in $jsFiles) {
    if (Test-Path $f) {
        Write-Host "`n  --- $([System.IO.Path]::GetFileName($f)) ---" -ForegroundColor Cyan
        Get-Content $f | Select-Object -First 8 | ForEach-Object { Write-Host "  $_" }
    }
}

# ── STEP 5: Output diagnosis ──────────────────────────────────
Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host " DIAGNOSIS - paste output above back to Claude" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Account: 74da814fca5b914ecf575f49f662933e"
Write-Host "Workers found: hko-imager, hko-audio, hko-converter"
Write-Host "Project folder: C:\Users\hkome\Desktop\Project\"
Write-Host ""
Write-Host "NEXT: paste this entire output to Claude" -ForegroundColor Green
