# HKO ESL Generator - Production Run
# Calls live workers to generate all 12 A2 lessons + audio + images + SCORM
# Run: cd C:\Users\hkome\Desktop\Project; .\GENERATE_ALL.ps1

$CONTENT_WORKER = "https://hko-content.mrhkruger-content.workers.dev"
$MEDIA_WORKER   = "https://hko-media.mrhkruger-content.workers.dev"
$OUT            = "C:\Users\hkome\Desktop\ESL_OUTPUT"

New-Item -ItemType Directory -Force -Path $OUT | Out-Null
New-Item -ItemType Directory -Force -Path "$OUT\lessons" | Out-Null
New-Item -ItemType Directory -Force -Path "$OUT\audio" | Out-Null
New-Item -ItemType Directory -Force -Path "$OUT\images" | Out-Null
New-Item -ItemType Directory -Force -Path "$OUT\scorm" | Out-Null

$lessons = @(
  @{num=1;  title="I Started in HR Five Years Ago";         grammar="Past Simple Regular Verbs";          voice="maria"},
  @{num=2;  title="I Didnt Expect So Many Applications";    grammar="Past Simple Negative Forms";         voice="carlos"},
  @{num=3;  title="We Received 50 Applications";            grammar="Past Simple Quantities";             voice="patricia"},
  @{num=4;  title="The Interview Went Well";                grammar="Past Simple Irregular Verbs";        voice="carlos"},
  @{num=5;  title="Im Going to Review the CVs Tomorrow";    grammar="Future Going To";                    voice="maria"},
  @{num=6;  title="Ill Send You the Job Description";       grammar="Future Will Offers and Promises";    voice="patricia"},
  @{num=7;  title="What Will Happen Next";                  grammar="Future Questions Will";              voice="carlos"},
  @{num=8;  title="This Candidate Is Better Than That One"; grammar="Comparatives";                       voice="patricia"},
  @{num=9;  title="Shes the Most Qualified Candidate";      grammar="Superlatives";                       voice="maria"},
  @{num=10; title="Our Process Is Faster Now";              grammar="Comparative Superlative Adverbs";    voice="carlos"},
  @{num=11; title="Have You Worked Here Long";              grammar="Present Perfect For and Since";      voice="maria"},
  @{num=12; title="Weve Just Hired Three People";           grammar="Present Perfect Just Already Yet";   voice="carlos"}
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host " HKO A2 - Full Course Generation" -ForegroundColor Cyan
Write-Host " Output: $OUT" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# ── TEST WORKERS ─────────────────────────────────────────────
Write-Host "`n[0] Testing workers..." -ForegroundColor Yellow

try {
    $r = Invoke-WebRequest -Uri "$CONTENT_WORKER/" -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "  hko-content: OK ($($r.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  hko-content: $($_.Exception.Message)" -ForegroundColor Red
}

try {
    $r = Invoke-WebRequest -Uri "$MEDIA_WORKER/" -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "  hko-media:   OK ($($r.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  hko-media:   $($_.Exception.Message)" -ForegroundColor Red
}

# ── GENERATE EACH LESSON ─────────────────────────────────────
$results = @()

foreach ($l in $lessons) {
    $num = $l.num.ToString("D2")
    Write-Host "`n[L$num] $($l.title)" -ForegroundColor Yellow

    # 1. Generate lesson HTML
    $body = @{
        level       = "A2"
        lessonNumber = $l.num
        title        = $l.title
        grammar      = $l.grammar
        voice        = $l.voice
        context      = "HR professionals Chile mining outsourcing SENCE CEFR A2"
    } | ConvertTo-Json

    $lessonFile = "$OUT\lessons\HKO_A2_L$num.html"
    try {
        $r = Invoke-RestMethod -Uri "$CONTENT_WORKER/generate" -Method POST `
             -ContentType "application/json" -Body $body -TimeoutSec 60
        if ($r -and $r.html) {
            $r.html | Out-File -FilePath $lessonFile -Encoding UTF8
            Write-Host "  HTML: saved ($([int]((Get-Item $lessonFile).Length/1024))KB)" -ForegroundColor Green
        } elseif ($r) {
            $r | ConvertTo-Json | Out-File "$OUT\lessons\L${num}_response.json" -Encoding UTF8
            Write-Host "  HTML: worker responded - check L${num}_response.json" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  HTML: $($_.Exception.Message)" -ForegroundColor Red
        $body | Out-File "$OUT\lessons\L${num}_request.json" -Encoding UTF8
    }

    # 2. Generate audio
    $audioBody = @{
        lessonNumber = $l.num
        voice        = $l.voice
        level        = "A2"
        title        = $l.title
    } | ConvertTo-Json

    $audioFile = "$OUT\audio\HKO_A2_L${num}_audio.mp3"
    try {
        $bytes = Invoke-WebRequest -Uri "$MEDIA_WORKER/audio" -Method POST `
                 -ContentType "application/json" -Body $audioBody -TimeoutSec 90 -UseBasicParsing
        if ($bytes.Content.Length -gt 1000) {
            [System.IO.File]::WriteAllBytes($audioFile, $bytes.Content)
            Write-Host "  Audio: saved ($([int]($bytes.Content.Length/1024))KB)" -ForegroundColor Green
        } else {
            $bytes.Content | Out-File "$OUT\audio\L${num}_audio_response.txt" -Encoding UTF8
            Write-Host "  Audio: worker responded - check L${num}_audio_response.txt" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  Audio: $($_.Exception.Message)" -ForegroundColor Red
    }

    # 3. Generate images
    $imageBody = @{
        lessonNumber = $l.num
        title        = $l.title
        level        = "A2"
    } | ConvertTo-Json

    $imageFile = "$OUT\images\HKO_A2_L${num}_scene.png"
    try {
        $bytes = Invoke-WebRequest -Uri "$MEDIA_WORKER/image" -Method POST `
                 -ContentType "application/json" -Body $imageBody -TimeoutSec 120 -UseBasicParsing
        if ($bytes.Content.Length -gt 5000) {
            [System.IO.File]::WriteAllBytes($imageFile, $bytes.Content)
            Write-Host "  Image: saved ($([int]($bytes.Content.Length/1024))KB)" -ForegroundColor Green
        } else {
            $bytes.Content | Out-File "$OUT\images\L${num}_image_response.txt" -Encoding UTF8
            Write-Host "  Image: worker responded - check L${num}_image_response.txt" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  Image: $($_.Exception.Message)" -ForegroundColor Red
    }

    $results += "L$num - $($l.title)"
    Start-Sleep -Seconds 2
}

# ── PACKAGE AS SCORM ─────────────────────────────────────────
Write-Host "`n[SCORM] Packaging lessons..." -ForegroundColor Yellow

# Check if Python is available for SCORM packaging
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $pythonCmd = $cmd
        break
    }
}

if ($pythonCmd) {
    # Copy build_scorm.py if it exists on Desktop
    $scormScript = "C:\Users\hkome\Desktop\build_scorm.py"
    if (-not (Test-Path $scormScript)) {
        Write-Host "  build_scorm.py not found at Desktop - copy it from Claude output" -ForegroundColor Yellow
    } else {
        & $pythonCmd $scormScript
        Write-Host "  SCORM packages built" -ForegroundColor Green
    }
} else {
    Write-Host "  Python not found - SCORM zips already available from Claude" -ForegroundColor Yellow
}

# ── SUMMARY ──────────────────────────────────────────────────
Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host " GENERATION COMPLETE" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Output folder: $OUT"
Write-Host ""
$results | ForEach-Object { Write-Host "  $_" }
Write-Host ""
Write-Host " Lessons:  $OUT\lessons\"
Write-Host " Audio:    $OUT\audio\"
Write-Host " Images:   $OUT\images\"
Write-Host " SCORM:    $OUT\scorm\"
Write-Host ""
Write-Host " Upload the SCORM zips to Moodle." -ForegroundColor Green

# ── SHOW WHAT THE WORKERS ACTUALLY ACCEPT ────────────────────
Write-Host "`n[DEBUG] Worker endpoint discovery..." -ForegroundColor Yellow
Write-Host "  Hitting /routes on each worker to see available endpoints:"

foreach ($url in @($CONTENT_WORKER, $MEDIA_WORKER)) {
    foreach ($path in @("/", "/routes", "/health", "/status", "/api", "/generate", "/audio", "/image", "/lesson")) {
        try {
            $r = Invoke-WebRequest -Uri "$url$path" -Method GET -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
            Write-Host "  $url$path => HTTP $($r.StatusCode): $($r.Content.Substring(0, [Math]::Min(120, $r.Content.Length)))" -ForegroundColor Green
        } catch {
            $code = $_.Exception.Response.StatusCode.value__
            if ($code -and $code -ne 404) {
                Write-Host "  $url$path => HTTP $code" -ForegroundColor Yellow
            }
        }
    }
}
