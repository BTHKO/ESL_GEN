"""
HKO A2 SCORM Builder
Generates 12 complete SCORM lessons + 2 quizzes
Uses real images from GitHub, local audio files
Run: python build_scorm.py
Output: ./scorm_output/ folder with 14 .zip files ready for Moodle
"""

import os, json, zipfile, shutil

# ── CONFIG ──────────────────────────────────────────────────────
GITHUB_RAW = "https://raw.githubusercontent.com/BTHKO/ESL_GEN/main"
AUDIO_DIR  = "audio"   # local folder where generate_audio.py saved files
OUT_DIR    = "scorm_output"
# ────────────────────────────────────────────────────────────────

os.makedirs(OUT_DIR, exist_ok=True)

# Image map: lesson → {slot: github_url}
IMAGES = {
    "L01": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L01_PPT_HERO_01_V1.png",
        "scene":   f"{GITHUB_RAW}/GEN_A2_L01_IMG_SCENE_01_V2.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L01_IMG_MATCH_01_V2.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L01_IMG_LABEL_01_V1.png",
    },
    "L02": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L02_IMG_SCENE_01_V2.png",
        "scene":   f"{GITHUB_RAW}/GEN_A2_L02_IMG_SCENE_01_V2.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L02_IMG_MATCH_01_V2.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L02_IMG_MATCH_01_V2.png",
    },
    "L03": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L03_IMG_SCENE_01_V1.png",
        "scene":   f"{GITHUB_RAW}/GEN_A2_L03_IMG_SCENE_01_V1.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L03_IMG_MATCH_01_V1.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L03_IMG_MATCH_01_V1.png",
    },
    "L04": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L04_IMG_SCENE_0.png",
        "scene":   f"{GITHUB_RAW}/GEN_A2_L04_IMG_SCENE_0.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L04_IMG_MATCH_01_V1.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L04_IMG_MATCH_01_V1.png",
    },
    "L05": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L05_IMG_SCENE_01_V1.png",
        "scene":   f"{GITHUB_RAW}/GEN_A2_L05_IMG_SCENE_01_V1.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L05_IMG_SCENE_01_V1.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L05_IMG_SCENE_01_V1.png",
    },
    "L06": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L06_IMG_SCENE_01_V1.png",
        "scene":   f"{GITHUB_RAW}/GEN_A2_L06_IMG_SCENE_01_V1.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L06_IMG_SCENE_01_V1.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L06_IMG_SCENE_01_V1.png",
    },
    "L07": {
        "hero":    f"{GITHUB_RAW}/EN_A2_L07_IMG_SCENE_01_V1.png",
        "scene":   f"{GITHUB_RAW}/EN_A2_L07_IMG_SCENE_01_V1.png",
        "vocab":   f"{GITHUB_RAW}/EN_A2_L07_IMG_SCENE_01_V1.png",
        "grammar": f"{GITHUB_RAW}/EN_A2_L07_IMG_SCENE_01_V1.png",
    },
    "L08": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L08_IMG_SCENE_01_V1.png",
        "scene":   f"{GITHUB_RAW}/GEN_A2_L08_IMG_SCENE_01_V1.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L08_IMG_SCENE_01_V1.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L08_IMG_SCENE_01_V1.png",
    },
    # L09-L12: reuse closest thematic images until new ones are generated
    "L09": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L08_IMG_SCENE_01_V1.png",
        "scene":   f"{GITHUB_RAW}/GEN_A2_L03_IMG_SCENE_01_V1.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L03_IMG_MATCH_01_V1.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L04_IMG_MATCH_01_V1.png",
    },
    "L10": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L02_IMG_SCENE_01_V2.png",
        "scene":   f"{GITHUB_RAW}/GEN_A2_L05_IMG_SCENE_01_V1.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L02_IMG_MATCH_01_V2.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L04_IMG_MATCH_01_V1.png",
    },
    "L11": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L06_IMG_SCENE_01_V1.png",
        "scene":   f"{GITHUB_RAW}/EN_A2_L07_IMG_SCENE_01_V1.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L01_IMG_MATCH_01_V2.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L03_IMG_MATCH_01_V1.png",
    },
    "L12": {
        "hero":    f"{GITHUB_RAW}/GEN_A2_L01_IMG_SCENE_01_V2.png",
        "scene":   f"{GITHUB_RAW}/GEN_A2_L08_IMG_SCENE_01_V1.png",
        "vocab":   f"{GITHUB_RAW}/GEN_A2_L04_IMG_MATCH_01_V1.png",
        "grammar": f"{GITHUB_RAW}/GEN_A2_L02_IMG_MATCH_01_V2.png",
    },
}

LESSON_META = {
    "L01": {"title": "I Started in HR Five Years Ago",       "grammar": "Past Simple — Regular Verbs",           "char": "María López",    "num": "01"},
    "L02": {"title": "I Didn't Expect So Many Applications", "grammar": "Past Simple — Negative Forms",          "char": "Carlos Ramírez", "num": "02"},
    "L03": {"title": "We Received 50 Applications",          "grammar": "Past Simple + Quantities",              "char": "Patricia Fuentes","num": "03"},
    "L04": {"title": "The Interview Went Well",              "grammar": "Past Simple — Irregular Verbs",         "char": "Carlos Ramírez", "num": "04"},
    "L05": {"title": "I'm Going to Review the CVs Tomorrow", "grammar": "Future with Going To",                  "char": "María López",    "num": "05"},
    "L06": {"title": "I'll Send You the Job Description",    "grammar": "Future with Will — Offers & Promises",  "char": "Patricia Fuentes","num": "06"},
    "L07": {"title": "What Will Happen Next?",              "grammar": "Future Questions — Will",               "char": "Carlos Ramírez", "num": "07"},
    "L08": {"title": "This Candidate Is Better Than That One","grammar": "Comparatives",                        "char": "Patricia Fuentes","num": "08"},
    "L09": {"title": "She's the Most Qualified Candidate",  "grammar": "Superlatives",                          "char": "María López",    "num": "09"},
    "L10": {"title": "Our Process Is Faster Now",           "grammar": "Comparative & Superlative Adverbs",     "char": "Carlos Ramírez", "num": "10"},
    "L11": {"title": "Have You Worked Here Long?",          "grammar": "Present Perfect — For & Since",         "char": "María López",    "num": "11"},
    "L12": {"title": "We've Just Hired Three People",        "grammar": "Present Perfect — Just, Already, Yet",  "char": "Carlos Ramírez", "num": "12"},
}

def make_imsmanifest(lesson_id, title, has_audio):
    audio_resource = ""
    if has_audio:
        audio_resource = f'<file href="audio/{lesson_id.lower()}_audio.mp3"/>'
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="HKO_A2_{lesson_id}" version="1.1"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2
    imscp_rootv1p1p2.xsd
    http://www.adlnet.org/xsd/adlcp_rootv1p2
    adlcp_rootv1p2.xsd">

  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
    <adlcp:location>metadata.xml</adlcp:location>
  </metadata>

  <organizations default="HKO_A2_{lesson_id}_ORG">
    <organization identifier="HKO_A2_{lesson_id}_ORG">
      <title>A2 HR English — {lesson_id}: {title}</title>
      <item identifier="ITEM_{lesson_id}" identifierref="RES_{lesson_id}">
        <title>{title}</title>
        <adlcp:masteryscore>60</adlcp:masteryscore>
      </item>
    </organization>
  </organizations>

  <resources>
    <resource identifier="RES_{lesson_id}" type="webcontent"
      adlcp:scormtype="sco" href="lesson.html">
      <file href="lesson.html"/>
      {audio_resource}
    </resource>
  </resources>

</manifest>"""

def make_lesson_html(lesson_id, meta, imgs, audio_path_relative):
    num    = meta["num"]
    title  = meta["title"]
    grammar= meta["grammar"]
    char   = meta["char"]

    audio_tag = ""
    audio_btn_play = "alert('Audio not yet available — check back soon')"
    if audio_path_relative:
        audio_tag = f'<audio id="story-audio" src="{audio_path_relative}" preload="metadata"></audio>'
        audio_btn_play = "playAudio()"

    # Full self-contained lesson HTML
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>HKO A2 · Lesson {num} · {title}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Syne:wght@700;800&display=swap');
:root{{
  --ink:#0f1923;--ink2:#3d4f5c;
  --blue:#28597A;--blue-l:#e8f2f8;--blue-m:#b8d4e4;
  --green:#2E8B57;--green-l:#ebfbee;
  --amber:#c87137;--amber-l:#fff4de;
  --red:#e03131;--red-l:#fff0f0;
  --teal:#0c8599;--teal-l:#e3fafc;
  --bg:#f4f6fb;--card:#fff;
  --line:#e2e8f0;--muted:#7a8fa6;
  --r:12px;--shadow:0 2px 12px rgba(15,25,35,.08);
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--ink);font-size:15px;line-height:1.55}}

/* TOPBAR */
.topbar{{position:sticky;top:0;z-index:200;background:rgba(255,255,255,.96);backdrop-filter:blur(16px);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px;padding:8px 16px}}
.logo-box{{width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,var(--blue),var(--teal));display:grid;place-items:center;color:#fff;font-family:'Syne',sans-serif;font-weight:800;font-size:11px;flex-shrink:0}}
.lesson-id{{font-family:'Syne',sans-serif;font-size:.82rem;font-weight:700;color:var(--ink)}}
.lesson-id span{{color:var(--muted);font-weight:500}}
.topbar-right{{margin-left:auto;display:flex;align-items:center;gap:8px}}
.xp-badge{{background:var(--amber-l);border:1px solid #ffd480;color:var(--amber);font-size:.75rem;font-weight:700;padding:4px 10px;border-radius:99px}}
.prog-wrap{{display:flex;align-items:center;gap:6px;font-size:.72rem;color:var(--muted);font-weight:700}}
.prog-bar{{width:80px;height:5px;background:var(--line);border-radius:99px;overflow:hidden}}
.prog-fill{{height:100%;background:linear-gradient(90deg,var(--blue),var(--teal));border-radius:99px;transition:width .4s}}

/* SHELL */
.shell{{max-width:860px;margin:0 auto;padding:16px 14px 80px}}

/* HERO */
.hero{{border-radius:16px;overflow:hidden;margin-bottom:14px;position:relative;min-height:220px;background:linear-gradient(135deg,#0f1923 0%,#1a3a60 60%,#0c4a6e 100%);display:grid;grid-template-columns:1fr 260px}}
.hero-text{{padding:24px;position:relative;z-index:1}}
.hero-tag{{display:inline-block;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);color:rgba(255,255,255,.8);font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:3px 10px;border-radius:99px;margin-bottom:10px}}
.hero-text h1{{font-family:'Syne',sans-serif;font-size:1.45rem;font-weight:800;color:#fff;line-height:1.1;margin-bottom:6px}}
.hero-text p{{font-size:.83rem;color:rgba(255,255,255,.65)}}
.hero-stats{{display:flex;gap:10px;margin-top:14px}}
.hstat{{text-align:center;background:rgba(255,255,255,.08);border-radius:8px;padding:6px 10px}}
.hstat strong{{display:block;color:#fff;font-size:.9rem;font-family:'Syne',sans-serif}}
.hstat span{{color:rgba(255,255,255,.5);font-size:.66rem;text-transform:uppercase;letter-spacing:.06em}}
.hero-img{{overflow:hidden;position:relative}}
.hero-img img{{width:100%;height:100%;object-fit:cover;opacity:.75}}

/* STAGE */
.stage{{background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow);margin-bottom:12px;overflow:hidden;scroll-margin-top:68px}}
.stage-head{{display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid var(--line);background:linear-gradient(90deg,#fafbfe,#f4f7ff)}}
.stage-badge{{font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em;padding:3px 9px;border-radius:99px;white-space:nowrap}}
.badge-v{{background:var(--blue-l);color:var(--blue)}}
.badge-g{{background:var(--green-l);color:var(--green)}}
.stage-title{{font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:var(--ink)}}
.stage-body{{padding:14px 16px;display:grid;gap:12px}}

/* LAYOUT */
.cols2{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}

/* IMAGE */
.img-block{{background:#f0f3f8;border-radius:10px;overflow:hidden;position:relative}}
.img-block img{{width:100%;height:100%;object-fit:cover;display:block;min-height:160px;border-radius:10px}}

/* INSTRUCTION */
.instr{{font-size:.83rem;color:var(--ink2);font-weight:500}}
.es{{font-size:.77rem;color:var(--muted);font-style:italic;margin-top:2px}}
.instr-box{{background:var(--blue-l);border-left:3px solid var(--blue);border-radius:0 8px 8px 0;padding:8px 12px}}

/* CHOICES */
.choices{{display:grid;gap:7px}}
.choice{{padding:9px 13px;border-radius:9px;border:1.5px solid var(--line);background:#fafbfc;font-size:.85rem;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:8px}}
.choice:hover{{border-color:var(--blue);background:var(--blue-l)}}
.choice .mark{{width:18px;height:18px;border-radius:50%;border:2px solid var(--line);flex-shrink:0}}
.choice.correct{{background:var(--green-l);border-color:#7cc090;color:var(--green)}}
.choice.wrong{{background:var(--red-l);border-color:#f4b8b8;color:var(--red)}}

/* MATCH */
.match-wrap{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.match-col{{display:grid;gap:6px}}
.match-item{{padding:9px 12px;border-radius:9px;border:1.5px solid var(--line);background:#fafbfc;font-size:.82rem;cursor:pointer;transition:all .15s;text-align:center}}
.match-item:hover{{border-color:var(--blue);background:var(--blue-l)}}
.match-item.selected{{border-color:var(--blue);background:var(--blue-l);color:var(--blue);font-weight:700}}
.match-item.matched{{background:var(--green-l);border-color:#7cc090;color:var(--green);cursor:default}}
.match-item.wrong-flash{{background:var(--red-l);border-color:#f4b8b8;animation:shake .3s}}
@keyframes shake{{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-4px)}}75%{{transform:translateX(4px)}}}}

/* FILL BLANK */
.fill-row{{display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:.87rem;padding:10px 12px;background:#f7f9fc;border-radius:9px;border:1px solid var(--line)}}
.fill-input{{border:none;border-bottom:2px solid var(--blue);background:transparent;color:var(--blue);font-weight:700;font-size:.87rem;font-family:inherit;outline:none;min-width:80px;text-align:center;padding:0 4px}}
.fill-pill{{padding:6px 12px;border-radius:99px;background:var(--blue-l);border:1.5px solid var(--blue-m);color:var(--blue);font-size:.8rem;font-weight:700;cursor:pointer;transition:all .15s}}
.fill-pill:hover{{background:var(--blue);color:#fff}}

/* TILES */
.tile-zone{{min-height:44px;padding:8px;border:2px dashed var(--line);border-radius:9px;display:flex;flex-wrap:wrap;gap:6px;background:#fafbfc}}
.tile{{padding:7px 12px;border-radius:8px;background:var(--blue-l);border:1.5px solid var(--blue-m);color:var(--blue);font-weight:700;font-size:.8rem;cursor:grab;user-select:none}}

/* AUDIO */
.audio-btn{{display:inline-flex;align-items:center;gap:7px;padding:8px 14px;border-radius:9px;background:var(--amber-l);border:1.5px solid #ffd480;color:var(--amber);font-weight:700;font-size:.8rem;cursor:pointer;transition:all .15s}}
.audio-wave{{display:flex;align-items:center;gap:2px;height:16px}}
.audio-wave span{{width:3px;background:var(--amber);border-radius:99px;animation:wave 1s ease-in-out infinite}}
.audio-wave span:nth-child(1){{height:6px}}
.audio-wave span:nth-child(2){{height:12px;animation-delay:.1s}}
.audio-wave span:nth-child(3){{height:16px;animation-delay:.2s}}
.audio-wave span:nth-child(4){{height:10px;animation-delay:.3s}}
.audio-wave span:nth-child(5){{height:6px;animation-delay:.4s}}
@keyframes wave{{0%,100%{{transform:scaleY(1)}}50%{{transform:scaleY(1.5)}}}}

/* GRAMMAR BOX */
.gram-box{{background:#fff;border:1.5px solid var(--line);border-radius:10px;overflow:hidden}}
.gram-box-head{{background:linear-gradient(90deg,var(--green-l),#f8fdf8);padding:10px 14px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:8px}}
.gram-box-head h4{{font-family:'Syne',sans-serif;font-size:.9rem;font-weight:800;color:var(--green)}}
.gram-use{{font-size:.75rem;color:#4a7c59;background:#d3f9d8;border-radius:5px;padding:2px 8px;font-weight:700}}
.gram-body{{padding:12px 14px;display:grid;gap:8px}}
.gram-table{{width:100%;border-collapse:collapse;font-size:.8rem}}
.gram-table th{{background:var(--green-l);color:var(--green);padding:6px 10px;text-align:left;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em}}
.gram-table td{{padding:7px 10px;border-bottom:1px solid #f0f4f0;vertical-align:top}}
.gram-table tr:last-child td{{border:none}}
.gram-table .t{{color:var(--blue);font-weight:700}}
.gram-err{{background:var(--red-l);border-radius:8px;padding:8px 12px;font-size:.8rem}}
.gram-err .x{{color:var(--red);text-decoration:line-through}}
.gram-err .ok{{color:var(--green);font-weight:700}}

/* VOCAB CARD */
.vc{{background:#fff;border:1.5px solid var(--line);border-radius:10px;overflow:hidden}}
.vc-head{{background:linear-gradient(90deg,#1c3a5e,#0c8599);padding:8px 12px}}
.vc-word{{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:#fff}}
.vc-ipa{{font-size:.75rem;color:rgba(255,255,255,.6);font-style:italic}}
.vc-body{{padding:10px 12px;display:grid;gap:5px;font-size:.8rem}}
.vc-def{{color:var(--ink2)}}
.vc-es{{color:var(--muted);font-style:italic}}
.vc-ex{{border-left:3px solid var(--amber);padding-left:8px;color:var(--ink2);font-style:italic}}

/* WRITE */
.write-task{{background:#fafbfe;border:1.5px solid var(--line);border-radius:10px;padding:12px}}
.write-context{{background:var(--amber-l);border-left:3px solid var(--amber);border-radius:0 8px 8px 0;padding:8px 12px;font-size:.8rem;color:#6b4c00;margin-bottom:10px}}
.write-context strong{{display:block;color:var(--amber);font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px}}
textarea.write-area{{width:100%;border:1.5px solid var(--line);border-radius:9px;padding:10px;font-family:inherit;font-size:.85rem;line-height:1.6;resize:none;background:#fff;color:var(--ink);min-height:110px}}
textarea.write-area:focus{{outline:none;border-color:var(--blue)}}
details.suggested{{margin-top:8px;border:1px dashed var(--line);border-radius:9px;padding:8px 12px;background:#fafcfe}}
details.suggested summary{{cursor:pointer;font-size:.78rem;font-weight:700;color:var(--amber)}}
details.suggested .sug-body{{padding-top:8px;font-size:.82rem;line-height:1.7;color:var(--ink2)}}

/* FEEDBACK */
.fb{{padding:8px 12px;border-radius:9px;font-size:.82rem;font-weight:600;display:none;align-items:center;gap:7px}}
.fb.ok{{background:var(--green-l);border:1px solid #7cc090;color:#2a7a40;display:flex}}
.fb.err{{background:var(--red-l);border:1px solid #f4b8b8;color:var(--red);display:flex}}
.fb.hint{{background:var(--amber-l);border:1px solid #ffd480;color:#7a5500;display:flex}}

/* BUTTONS */
.btn{{border:none;border-radius:9px;padding:8px 14px;font-family:inherit;font-size:.8rem;font-weight:700;cursor:pointer;transition:all .15s;display:inline-flex;align-items:center;gap:6px}}
.btn.primary{{background:var(--blue);color:#fff}}
.btn.primary:hover{{background:#1e4a6a}}
.btn.green{{background:var(--green);color:#fff}}
.btn.ghost{{background:#fff;color:var(--ink);border:1.5px solid var(--line)}}
.btn.ghost:hover{{border-color:var(--blue);color:var(--blue)}}
.btn.amber{{background:var(--amber);color:#fff}}
.btn.sm{{padding:5px 10px;font-size:.75rem}}
.controls{{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;padding-top:10px;border-top:1px solid var(--line);margin-top:4px}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}

/* BADGE */
.badge{{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:99px;font-size:.78rem;font-weight:700;border:1.5px dashed var(--line);color:var(--muted);transition:all .3s}}
.badge.earned{{background:var(--amber-l);border-color:var(--amber);color:var(--amber);animation:pop .4s ease}}
@keyframes pop{{0%{{transform:scale(.8)}}60%{{transform:scale(1.1)}}100%{{transform:scale(1)}}}}
.badge-row{{display:flex;gap:8px;flex-wrap:wrap}}

/* SECTION BREAK */
.section-break{{display:flex;align-items:center;gap:10px;margin:18px 0 12px}}
.section-break h2{{font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:var(--green);white-space:nowrap}}
.section-break hr{{flex:1;border:none;border-top:2px solid var(--green-l)}}

/* QUIZ */
.quiz-card{{background:var(--card);border:1.5px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow);padding:16px;margin-bottom:12px}}
.quiz-q{{font-size:.88rem;font-weight:700;color:var(--ink);margin-bottom:10px}}
.score-box{{background:linear-gradient(135deg,var(--blue-l),var(--teal-l));border:1px solid var(--blue-m);border-radius:10px;padding:12px;text-align:center}}
.score-num{{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:var(--blue)}}

/* CAN DO */
.cando-list{{list-style:none;display:grid;gap:7px}}
.cando-item{{display:flex;align-items:center;gap:9px;padding:8px 11px;border-radius:9px;border:1.5px solid var(--line);background:#fafbfd;font-size:.84rem;cursor:pointer;transition:all .15s}}
.cando-item input{{accent-color:var(--teal);width:16px;height:16px;flex-shrink:0}}
.cando-item.checked{{background:var(--green-l);border-color:#7cc090}}

/* VOCAB GRID */
.vocab-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.vg-item{{background:#f7f9fc;border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:.8rem}}
.vg-item strong{{color:var(--blue);display:block;font-weight:700}}
.vg-item span{{color:var(--muted);font-style:italic}}

/* TRANSCRIPT */
.transcript{{background:#f7f9fc;border:1.5px dashed var(--line);border-radius:10px;padding:12px;font-size:.83rem;line-height:1.9}}
.t-speaker{{font-weight:800;color:var(--blue)}}
.t-target{{color:var(--amber);font-weight:700;background:var(--amber-l);padding:0 3px;border-radius:3px}}

/* STAGE NAV */
.stage-nav{{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:12px 14px;margin-bottom:14px}}
.stage-nav-row{{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}}
.snav-btn{{display:flex;align-items:center;gap:4px;padding:5px 10px;border-radius:7px;font-size:.72rem;font-weight:700;cursor:pointer;border:1px solid var(--line);background:#f7f9fc;color:var(--muted);transition:all .15s;white-space:nowrap}}
.snav-btn.v{{color:var(--blue);border-color:var(--blue-m);background:var(--blue-l)}}
.snav-btn.g{{color:var(--green);border-color:#b2d9bc;background:var(--green-l)}}
.snav-btn.done::after{{content:' ✓';opacity:.7}}
.snav-label{{font-size:.7rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:4px}}

/* MEM GAME */
.mem-board{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}
.mem-card{{aspect-ratio:1;border-radius:10px;border:2px solid var(--line);background:linear-gradient(135deg,var(--blue),var(--teal));cursor:pointer;position:relative;transform-style:preserve-3d;transition:transform .35s}}
.mem-card.flipped,.mem-card.matched{{transform:rotateY(180deg)}}
.mem-card-front,.mem-card-back{{position:absolute;inset:0;border-radius:8px;display:grid;place-items:center;backface-visibility:hidden;font-size:.82rem;font-weight:700;padding:6px;text-align:center}}
.mem-card-front{{color:rgba(255,255,255,.4);font-size:1.4rem}}
.mem-card-back{{background:#fff;color:var(--blue);transform:rotateY(180deg)}}
.mem-card.matched .mem-card-back{{background:var(--green-l);color:var(--green)}}

@media(max-width:600px){{
  .cols2,.match-wrap,.vocab-grid{{grid-template-columns:1fr}}
  .hero{{grid-template-columns:1fr}}.hero-img{{display:none}}
  .mem-board{{grid-template-columns:repeat(4,1fr)}}
}}
</style>
</head>
<body>
{audio_tag}

<div class="topbar">
  <div class="logo-box">HKO</div>
  <div><div class="lesson-id">A2 · Lesson {num} <span>· {title}</span></div></div>
  <div class="topbar-right">
    <div class="xp-badge">⚡ <span id="xp">0</span> XP</div>
    <div class="prog-wrap">
      <div class="prog-bar"><div class="prog-fill" id="prog" style="width:0%"></div></div>
      <span id="prog-txt">0%</span>
    </div>
  </div>
</div>

<div class="shell">

<div class="hero">
  <div class="hero-text">
    <div class="hero-tag">A2 · HR English · {grammar}</div>
    <h1>"{title}"</h1>
    <p>Learn to talk about HR work using {grammar.lower()}.</p>
    <div class="hero-stats">
      <div class="hstat"><strong>14</strong><span>Stages</span></div>
      <div class="hstat"><strong>500</strong><span>XP</span></div>
      <div class="hstat"><strong>~4h</strong><span>Total</span></div>
    </div>
  </div>
  <div class="hero-img"><img src="{imgs['hero']}" alt="HR professionals at work" onerror="this.parentNode.style.background='linear-gradient(135deg,#1a3a60,#0c4a6e)'"></div>
</div>

<!-- CAN DO -->
<div style="background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:14px;margin-bottom:14px;display:flex;gap:14px;align-items:flex-start">
  <div style="width:32px;height:32px;background:var(--blue-l);border-radius:8px;display:grid;place-items:center;font-size:1rem;flex-shrink:0">🎯</div>
  <div>
    <div style="font-family:'Syne',sans-serif;font-size:.82rem;font-weight:800;color:var(--blue);margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em">By the end of this lesson you can…</div>
    <ul style="list-style:none;display:grid;gap:4px">
      <li style="font-size:.83rem;color:var(--ink2);display:flex;gap:6px"><span style="color:var(--green);font-weight:800">✓</span> Use {grammar.lower()} in professional HR contexts</li>
      <li style="font-size:.83rem;color:var(--ink2);display:flex;gap:6px"><span style="color:var(--green);font-weight:800">✓</span> Understand {char} talking about their work</li>
      <li style="font-size:.83rem;color:var(--ink2);display:flex;gap:6px"><span style="color:var(--green);font-weight:800">✓</span> Write a short professional message about this topic</li>
      <li style="font-size:.83rem;color:var(--ink2);display:flex;gap:6px"><span style="color:var(--green);font-weight:800">✓</span> Ask and answer questions about HR situations</li>
    </ul>
  </div>
</div>

<!-- STAGE NAV -->
<div class="stage-nav">
  <div class="snav-label">Lesson Stages</div>
  <div class="stage-nav-row">
    <button class="snav-btn v" id="nav-v1" onclick="jumpTo('v1')">👁 V1</button>
    <button class="snav-btn v" id="nav-v2" onclick="jumpTo('v2')">🔤 V2</button>
    <button class="snav-btn v" id="nav-v3" onclick="jumpTo('v3')">🎙 V3</button>
    <button class="snav-btn v" id="nav-v4" onclick="jumpTo('v4')">🎮 V4</button>
    <button class="snav-btn v" id="nav-v5" onclick="jumpTo('v5')">🧩 V5</button>
    <button class="snav-btn v" id="nav-v6" onclick="jumpTo('v6')">✏️ V6</button>
    <button class="snav-btn v" id="nav-v7" onclick="jumpTo('v7')">🎤 V7</button>
    <button class="snav-btn g" id="nav-g1" onclick="jumpTo('g1')">🔍 G1</button>
    <button class="snav-btn g" id="nav-g2" onclick="jumpTo('g2')">📖 G2</button>
    <button class="snav-btn g" id="nav-g3" onclick="jumpTo('g3')">🔀 G3</button>
    <button class="snav-btn g" id="nav-g4" onclick="jumpTo('g4')">✅ G4</button>
    <button class="snav-btn g" id="nav-g5" onclick="jumpTo('g5')">🛠 G5</button>
    <button class="snav-btn g" id="nav-g6" onclick="jumpTo('g6')">📝 G6</button>
    <button class="snav-btn g" id="nav-g7" onclick="jumpTo('g7')">📧 G7</button>
  </div>
</div>

<!-- V1 -->
<div class="stage" id="v1">
  <div class="stage-head"><span class="stage-badge badge-v">👁 Word Builder · Stage 1</span><span class="stage-title">Look at the Scene</span></div>
  <div class="stage-body">
    <div class="cols2">
      <div class="img-block"><img src="{imgs['scene']}" alt="HR scene" onerror="this.style.minHeight='160px';this.style.background='var(--blue-l)'"></div>
      <div style="display:grid;gap:8px">
        <div class="instr-box"><div class="instr">Look at the image. Answer the questions below.</div><div class="es">Mira la imagen. Responde las preguntas.</div></div>
        <div style="font-size:.82rem;font-weight:700;color:var(--ink2)">What can you see? Choose all that apply.</div>
        <div class="choices" id="v1-obs">
          <div class="choice" onclick="toggleObs(this,'correct')"><div class="mark"></div>HR professionals at work</div>
          <div class="choice" onclick="toggleObs(this,'correct')"><div class="mark"></div>A professional office environment</div>
          <div class="choice" onclick="toggleObs(this,'wrong')"><div class="mark"></div>Someone working alone at home</div>
          <div class="choice" onclick="toggleObs(this,'correct')"><div class="mark"></div>People having a work discussion</div>
        </div>
      </div>
    </div>
    <div id="v1-fb" class="fb"></div>
    <div class="controls"><span></span><button class="btn primary" onclick="completeStage('v1','v2')">Next →</button></div>
  </div>
</div>

<!-- V2 -->
<div class="stage" id="v2">
  <div class="stage-head"><span class="stage-badge badge-v">🔤 Word Builder · Stage 2</span><span class="stage-title">Meet the Words</span></div>
  <div class="stage-body">
    <div class="instr-box"><div class="instr">Match each career action to its meaning. Click a word, then its match.</div><div class="es">Une cada acción con su significado.</div></div>
    <div class="match-wrap" id="v2-match">
      <div class="match-col">
        <div class="match-item" data-pair="a" onclick="matchClick(this)">started</div>
        <div class="match-item" data-pair="b" onclick="matchClick(this)">graduated</div>
        <div class="match-item" data-pair="c" onclick="matchClick(this)">applied</div>
        <div class="match-item" data-pair="d" onclick="matchClick(this)">received</div>
        <div class="match-item" data-pair="e" onclick="matchClick(this)">changed</div>
        <div class="match-item" data-pair="f" onclick="matchClick(this)">joined</div>
      </div>
      <div class="match-col">
        <div class="match-item" data-pair="c" onclick="matchClick(this)">formally requested a job</div>
        <div class="match-item" data-pair="e" onclick="matchClick(this)">moved to something different</div>
        <div class="match-item" data-pair="a" onclick="matchClick(this)">began a role or position</div>
        <div class="match-item" data-pair="f" onclick="matchClick(this)">became part of a team</div>
        <div class="match-item" data-pair="d" onclick="matchClick(this)">got something back</div>
        <div class="match-item" data-pair="b" onclick="matchClick(this)">finished university studies</div>
      </div>
    </div>
    <div id="v2-fb" class="fb"></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('v1')">← Back</button><button class="btn primary" onclick="completeStage('v2','v3')">Next →</button></div>
  </div>
</div>

<!-- V3 -->
<div class="stage" id="v3">
  <div class="stage-head"><span class="stage-badge badge-v">🎙 Word Builder · Stage 3</span><span class="stage-title">{char}'s Story</span></div>
  <div class="stage-body">
    <div class="cols2">
      <div class="img-block"><img src="{imgs['vocab']}" alt="HR character" onerror="this.style.minHeight='160px';this.style.background='var(--blue-l)'"></div>
      <div style="display:grid;gap:8px;align-content:start">
        <div class="instr-box"><div class="instr">Listen to the story. Notice the highlighted words.</div><div class="es">Escucha. Nota las palabras destacadas.</div></div>
        <div class="audio-btn" onclick="{audio_btn_play}" id="story-btn">
          <span>🔊</span><span id="story-txt">Play Story</span>
          <div class="audio-wave"><span></span><span></span><span></span><span></span><span></span></div>
        </div>
        <button class="btn ghost sm" onclick="document.getElementById('v3-transcript').style.display=document.getElementById('v3-transcript').style.display==='none'?'block':'none'">📄 Show/Hide Script</button>
        <div id="v3-transcript" class="transcript" style="display:none">
          <p>Read the script above — the highlighted words are your target vocabulary for this lesson.</p>
        </div>
      </div>
    </div>
    <div style="font-size:.82rem;font-weight:700;color:var(--ink2)">Answer the questions. Choose the best option.</div>
    <div style="display:grid;gap:10px">
      <div>
        <div style="font-size:.82rem;color:var(--ink2);margin-bottom:5px;font-weight:600">1. What is the main topic of this lesson?</div>
        <div class="choices">
          <div class="choice" onclick="quizQ(this,0,'a')"><div class="mark"></div>HR career language ✓</div>
          <div class="choice" onclick="quizQ(this,0,'b')"><div class="mark"></div>Cooking vocabulary</div>
          <div class="choice" onclick="quizQ(this,0,'b')"><div class="mark"></div>Sports terms</div>
        </div>
      </div>
      <div>
        <div style="font-size:.82rem;color:var(--ink2);margin-bottom:5px;font-weight:600">2. Which grammar structure does this lesson focus on?</div>
        <div class="choices">
          <div class="choice" onclick="quizQ(this,1,'a')"><div class="mark"></div>{grammar} ✓</div>
          <div class="choice" onclick="quizQ(this,1,'b')"><div class="mark"></div>Present continuous</div>
          <div class="choice" onclick="quizQ(this,1,'b')"><div class="mark"></div>Passive voice</div>
        </div>
      </div>
    </div>
    <div id="v3-fb" class="fb"></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('v2')">← Back</button><button class="btn primary" onclick="completeStage('v3','v4')">Next →</button></div>
  </div>
</div>

<!-- V4 -->
<div class="stage" id="v4">
  <div class="stage-head"><span class="stage-badge badge-v">🎮 Word Builder · Stage 4</span><span class="stage-title">Memory Game</span></div>
  <div class="stage-body">
    <div class="instr-box"><div class="instr">Flip cards to find matching pairs: English word ↔ Spanish meaning.</div><div class="es">Voltea fichas para encontrar los pares correctos.</div></div>
    <div class="mem-board" id="mem-board"></div>
    <div style="display:flex;justify-content:space-between;font-size:.78rem;color:var(--muted);margin-top:4px">
      <span>Pairs: <strong id="mem-pairs">0</strong>/4</span>
      <button class="btn ghost sm" onclick="initMemory()">↩ Reset</button>
    </div>
    <div id="v4-fb" class="fb"></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('v3')">← Back</button><button class="btn primary" onclick="completeStage('v4','v5')">Next →</button></div>
  </div>
</div>

<!-- V5 -->
<div class="stage" id="v5">
  <div class="stage-head"><span class="stage-badge badge-v">🧩 Word Builder · Stage 5</span><span class="stage-title">Fill the Gaps</span></div>
  <div class="stage-body">
    <div class="instr-box"><div class="instr">Choose the correct word to complete each sentence.</div><div class="es">Elige la palabra correcta para completar cada oración.</div></div>
    <div style="display:grid;gap:9px">
      <div class="fill-row">I <input class="fill-input" id="f1" placeholder="?" style="width:90px"> from university in 2018.
        <span class="fill-pill" onclick="fillInput('f1',this,'graduated')">graduated</span>
        <span class="fill-pill" onclick="fillInput('f1',this,'started')">started</span>
      </div>
      <div class="fill-row">She <input class="fill-input" id="f2" placeholder="?" style="width:75px"> for the position last month.
        <span class="fill-pill" onclick="fillInput('f2',this,'applied')">applied</span>
        <span class="fill-pill" onclick="fillInput('f2',this,'joined')">joined</span>
      </div>
      <div class="fill-row">He <input class="fill-input" id="f3" placeholder="?" style="width:70px"> the HR team in 2021.
        <span class="fill-pill" onclick="fillInput('f3',this,'joined')">joined</span>
        <span class="fill-pill" onclick="fillInput('f3',this,'changed')">changed</span>
      </div>
    </div>
    <div class="btn-row" style="margin-top:6px">
      <button class="btn ghost sm" onclick="checkFills(['f1:graduated','f2:applied','f3:joined'],'v5-fb')">✓ Check</button>
    </div>
    <div id="v5-fb" class="fb"></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('v4')">← Back</button><button class="btn primary" onclick="completeStage('v5','v6')">Next →</button></div>
  </div>
</div>

<!-- V6 -->
<div class="stage" id="v6">
  <div class="stage-head"><span class="stage-badge badge-v">✏️ Word Builder · Stage 6</span><span class="stage-title">Build Your Sentences</span></div>
  <div class="stage-body">
    <div class="instr-box"><div class="instr">Choose the correct sentence. Spot the error in the wrong ones.</div><div class="es">Elige la oración correcta.</div></div>
    <div class="choices" id="v6-err">
      <div class="choice" onclick="pickOne(this,'v6-err','wrong')"><div class="mark"></div>She didn't <u>worked</u> in finance.</div>
      <div class="choice" onclick="pickOne(this,'v6-err','correct')"><div class="mark"></div>She didn't <strong>work</strong> in finance. ✓</div>
      <div class="choice" onclick="pickOne(this,'v6-err','wrong')"><div class="mark"></div>She don't worked in finance.</div>
    </div>
    <div style="margin-top:8px">
      <div class="choices" id="v6-err2">
        <div class="choice" onclick="pickOne(this,'v6-err2','wrong')"><div class="mark"></div>Did she worked at MineSafe?</div>
        <div class="choice" onclick="pickOne(this,'v6-err2','wrong')"><div class="mark"></div>Did she works at MineSafe?</div>
        <div class="choice" onclick="pickOne(this,'v6-err2','correct')"><div class="mark"></div>Did she <strong>work</strong> at MineSafe? ✓</div>
      </div>
    </div>
    <div id="v6-fb" class="fb"></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('v5')">← Back</button><button class="btn primary" onclick="completeStage('v6','v7')">Next →</button></div>
  </div>
</div>

<!-- V7 -->
<div class="stage" id="v7">
  <div class="stage-head"><span class="stage-badge badge-v">🎤 Word Builder · Stage 7</span><span class="stage-title">Tell Your Story</span></div>
  <div class="stage-body">
    <div class="instr-box"><div class="instr">Record yourself for 30–60 seconds. Use at least 5 lesson words.</div><div class="es">Grábate 30–60 segundos. Usa al menos 5 palabras de esta lección.</div></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px">
      <button class="btn amber" onclick="alert('Connect to Moodle audio capture for recording')">🔴 Record</button>
      <button class="btn ghost sm">⏹ Stop</button>
      <button class="btn ghost sm">▶ Play</button>
    </div>
    <details class="suggested">
      <summary>💡 Sample Answer</summary>
      <div class="sug-body">I started my career in HR five years ago. I graduated from university and applied for several jobs. I received an offer and worked as an HR assistant. Then I changed roles and joined the recruitment team.</div>
    </details>
    <div class="badge-row" style="margin-top:8px"><div class="badge" id="badge-vocab">🗂 Vocabulary Complete</div></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('v6')">← Back</button><button class="btn green" onclick="unlockBadge('badge-vocab');completeStage('v7','g1')">✅ Start Useful Language →</button></div>
  </div>
</div>

<!-- GRAMMAR SECTION -->
<div class="section-break"><h2>Useful Language</h2><hr></div>

<!-- G1 -->
<div class="stage" id="g1">
  <div class="stage-head"><span class="stage-badge badge-g">🔍 Useful Language · Stage 1</span><span class="stage-title">How Did They Say It?</span></div>
  <div class="stage-body">
    <div class="instr-box"><div class="instr">Read the sentences. What do you notice about the verbs?</div><div class="es">¿Qué notas sobre los verbos?</div></div>
    <div style="display:grid;gap:7px">
      <div style="padding:9px 13px;border-radius:9px;background:var(--blue-l);border-left:3px solid var(--blue);font-size:.88rem">I <strong style="color:var(--blue)">started</strong> five years ago.</div>
      <div style="padding:9px 13px;border-radius:9px;background:var(--blue-l);border-left:3px solid var(--blue);font-size:.88rem">She <strong style="color:var(--blue)">graduated</strong> in 2018.</div>
      <div style="padding:9px 13px;border-radius:9px;background:var(--blue-l);border-left:3px solid var(--blue);font-size:.88rem">We <strong style="color:var(--blue)">received</strong> many applications.</div>
      <div style="padding:9px 13px;border-radius:9px;background:var(--amber-l);border-left:3px solid var(--amber);font-size:.88rem">I <strong style="color:var(--red)">didn't work</strong> in finance.</div>
    </div>
    <div class="choices" id="g1-disc">
      <div class="choice" onclick="pickOne(this,'g1-disc','correct')"><div class="mark"></div>They describe finished actions in the past ✓</div>
      <div class="choice" onclick="pickOne(this,'g1-disc','wrong')"><div class="mark"></div>They describe things happening right now</div>
      <div class="choice" onclick="pickOne(this,'g1-disc','wrong')"><div class="mark"></div>They are about future plans</div>
    </div>
    <div id="g1-fb" class="fb"></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('v7')">← Back</button><button class="btn primary" onclick="completeStage('g1','g2')">Next →</button></div>
  </div>
</div>

<!-- G2 -->
<div class="stage" id="g2">
  <div class="stage-head"><span class="stage-badge badge-g">📖 Useful Language · Stage 2</span><span class="stage-title">The Language Box</span></div>
  <div class="stage-body">
    <div class="gram-box">
      <div class="gram-box-head"><h4>{grammar}</h4><span class="gram-use">We use this to describe finished HR actions</span></div>
      <div class="gram-body">
        <table class="gram-table">
          <thead><tr><th>Form</th><th>Structure</th><th>HR Example</th></tr></thead>
          <tbody>
            <tr><td>✅ +</td><td>subject + <span class="t">verb+ed</span></td><td>I <span class="t">started</span> in HR five years ago.</td></tr>
            <tr><td>❌ −</td><td>subject + <span class="t">didn't</span> + base verb</td><td>She <span class="t">didn't work</span> in payroll.</td></tr>
            <tr><td>❓ ?</td><td><span class="t">Did</span> + subject + base verb?</td><td><span class="t">Did</span> you work there long?</td></tr>
          </tbody>
        </table>
        <div class="gram-err">
          <div style="font-size:.72rem;font-weight:800;color:var(--red);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">⚠ Common Error</div>
          <div><span class="x">didn't worked</span> → <span class="ok">didn't work ✓</span></div>
        </div>
      </div>
    </div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('g1')">← Back</button><button class="btn primary" onclick="completeStage('g2','g3')">Next →</button></div>
  </div>
</div>

<!-- G3 G4 G5 G6 -->
<div class="stage" id="g3">
  <div class="stage-head"><span class="stage-badge badge-g">🔀 Useful Language · Stage 3</span><span class="stage-title">Past or Present?</span></div>
  <div class="stage-body">
    <div class="instr-box"><div class="instr">Which sentence uses the correct form? Choose carefully.</div><div class="es">¿Cuál oración usa la forma correcta?</div></div>
    <div class="choices" id="g3-q1">
      <div class="choice" onclick="pickOne(this,'g3-q1','wrong')"><div class="mark"></div>I am working last week.</div>
      <div class="choice" onclick="pickOne(this,'g3-q1','correct')"><div class="mark"></div>I worked last week. ✓</div>
      <div class="choice" onclick="pickOne(this,'g3-q1','wrong')"><div class="mark"></div>I work last week.</div>
    </div>
    <div class="choices" id="g3-q2" style="margin-top:8px">
      <div class="choice" onclick="pickOne(this,'g3-q2','wrong')"><div class="mark"></div>We didn't received any CVs.</div>
      <div class="choice" onclick="pickOne(this,'g3-q2','correct')"><div class="mark"></div>We didn't receive any CVs. ✓</div>
      <div class="choice" onclick="pickOne(this,'g3-q2','wrong')"><div class="mark"></div>We not received any CVs.</div>
    </div>
    <div id="g3-fb" class="fb"></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('g2')">← Back</button><button class="btn primary" onclick="completeStage('g3','g4')">Next →</button></div>
  </div>
</div>

<div class="stage" id="g4">
  <div class="stage-head"><span class="stage-badge badge-g">✅ Useful Language · Stage 4</span><span class="stage-title">Build the Forms</span></div>
  <div class="stage-body">
    <div class="instr-box"><div class="instr">Complete each sentence with the correct form.</div><div class="es">Completa con la forma correcta.</div></div>
    <div style="display:grid;gap:9px">
      <div class="fill-row">I <input class="fill-input" id="g4f1" placeholder="?" style="width:85px"> for five positions last year.
        <span class="fill-pill" onclick="fillInput('g4f1',this,'applied')">applied</span>
        <span class="fill-pill" onclick="fillInput('g4f1',this,'apply')">apply</span>
      </div>
      <div class="fill-row">She <input class="fill-input" id="g4f2" placeholder="?" style="width:75px"> complete the form.
        <span class="fill-pill" onclick="fillInput('g4f2',this,&quot;didn't&quot;)">didn't</span>
        <span class="fill-pill" onclick="fillInput('g4f2',this,'not')">not</span>
      </div>
      <div class="fill-row"><input class="fill-input" id="g4f3" placeholder="?" style="width:40px"> you work in mining before?
        <span class="fill-pill" onclick="fillInput('g4f3',this,'Did')">Did</span>
        <span class="fill-pill" onclick="fillInput('g4f3',this,'Do')">Do</span>
      </div>
    </div>
    <div class="btn-row" style="margin-top:6px">
      <button class="btn ghost sm" onclick="checkFills(['g4f1:applied','g4f2:didn\\'t','g4f3:Did'],'g4-fb')">✓ Check All</button>
    </div>
    <div id="g4-fb" class="fb"></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('g3')">← Back</button><button class="btn primary" onclick="completeStage('g4','g5')">Next →</button></div>
  </div>
</div>

<div class="stage" id="g5">
  <div class="stage-head"><span class="stage-badge badge-g">🛠 Useful Language · Stage 5</span><span class="stage-title">Listening Practice</span></div>
  <div class="stage-body">
    <div class="cols2">
      <div class="img-block"><img src="{imgs['grammar']}" alt="Grammar scene" onerror="this.style.minHeight='160px';this.style.background='var(--green-l)'"></div>
      <div style="display:grid;gap:7px;align-content:start">
        <div class="instr-box"><div class="instr">Listen. Focus on how questions are formed.</div><div class="es">Escucha. Observa cómo se forman las preguntas.</div></div>
        <div class="audio-btn" onclick="playTTS(['When did you graduate?','I graduated in 2018.','Where did you work after that?','I worked at MineSafe for four years.','Did you manage a team?','No, I did not. I was a coordinator.'],this)">
          <span>🔊</span><span>Play Dialogue</span>
          <div class="audio-wave"><span></span><span></span><span></span><span></span><span></span></div>
        </div>
        <div class="transcript">
          <p><span class="t-speaker">Interviewer:</span> <span class="t-target">When did</span> you graduate?</p>
          <p><span class="t-speaker">Candidate:</span> I graduated in 2018.</p>
          <p><span class="t-speaker">Interviewer:</span> <span class="t-target">Where did</span> you work after that?</p>
          <p><span class="t-speaker">Candidate:</span> I worked at MineSafe for four years.</p>
          <p><span class="t-speaker">Interviewer:</span> <span class="t-target">Did</span> you manage a team?</p>
          <p><span class="t-speaker">Candidate:</span> No, I <span class="t-target">didn't</span>.</p>
        </div>
      </div>
    </div>
    <div class="choices" id="g5-q1">
      <div class="choice" onclick="pickOne(this,'g5-q1','correct')"><div class="mark"></div>Questions use Did + subject + base verb ✓</div>
      <div class="choice" onclick="pickOne(this,'g5-q1','wrong')"><div class="mark"></div>Questions use Does + subject + -ed verb</div>
    </div>
    <div id="g5-fb" class="fb"></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('g4')">← Back</button><button class="btn primary" onclick="completeStage('g5','g6')">Next →</button></div>
  </div>
</div>

<div class="stage" id="g6">
  <div class="stage-head"><span class="stage-badge badge-g">📝 Useful Language · Stage 6</span><span class="stage-title">Build Interview Questions</span></div>
  <div class="stage-body">
    <div class="instr-box"><div class="instr">Choose the correct sentence in each pair.</div><div class="es">Elige la oración correcta en cada par.</div></div>
    <div class="choices" id="g6-q1">
      <div class="choice" onclick="pickOne(this,'g6-q1','wrong')"><div class="mark"></div>Did she worked at MineSafe?</div>
      <div class="choice" onclick="pickOne(this,'g6-q1','correct')"><div class="mark"></div>Did she work at MineSafe? ✓</div>
    </div>
    <div class="choices" id="g6-q2" style="margin-top:8px">
      <div class="choice" onclick="pickOne(this,'g6-q2','correct')"><div class="mark"></div>How long did you work there? ✓</div>
      <div class="choice" onclick="pickOne(this,'g6-q2','wrong')"><div class="mark"></div>How long did you worked there?</div>
    </div>
    <div id="g6-fb" class="fb"></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('g5')">← Back</button><button class="btn primary" onclick="completeStage('g6','g7')">Next →</button></div>
  </div>
</div>

<!-- G7 -->
<div class="stage" id="g7">
  <div class="stage-head"><span class="stage-badge badge-g">📧 Useful Language · Stage 7</span><span class="stage-title">Write a Professional Message</span></div>
  <div class="stage-body">
    <div class="write-task">
      <div class="write-context"><strong>Your Task</strong>Write a short email to your manager about a recent recruitment process. Use {grammar.lower()} throughout. Aim for 60–100 words.</div>
      <div style="font-size:.75rem;font-weight:700;color:var(--muted);margin-bottom:5px">Word bank:</div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px">
        <span class="fill-pill" style="cursor:default">received</span>
        <span class="fill-pill" style="cursor:default">reviewed</span>
        <span class="fill-pill" style="cursor:default">shortlisted</span>
        <span class="fill-pill" style="cursor:default">interviewed</span>
        <span class="fill-pill" style="cursor:default">didn't expect</span>
      </div>
      <textarea class="write-area" id="g7-text" placeholder="Hi María,&#10;&#10;I wanted to update you on the recruitment process…&#10;&#10;Best regards,&#10;[Your name]" oninput="updateCounter(this,'g7-wc')"></textarea>
      <div style="font-size:.72rem;color:var(--muted);text-align:right;margin-top:4px">Words: <span id="g7-wc">0</span> / 60–100</div>
      <div class="btn-row" style="margin-top:8px"><button class="btn ghost sm" onclick="checkWriteLen('g7-text','g7-fb',40)">✓ Check Length</button></div>
      <div id="g7-fb" class="fb"></div>
      <details class="suggested">
        <summary>💡 Suggested Answer</summary>
        <div class="sug-body">Hi María,<br><br>I wanted to update you on the recruitment process. We received 45 applications. I didn't expect so many! I reviewed them and shortlisted six candidates. The interviews went very well. Three candidates performed strongly.<br><br>Best regards,<br>Paula</div>
      </details>
    </div>
    <div class="badge-row" style="margin-top:10px"><div class="badge" id="badge-gram">📝 Language Complete</div></div>
    <div class="controls"><button class="btn ghost sm" onclick="jumpTo('g6')">← Back</button><button class="btn green" onclick="unlockBadge('badge-gram');completeStage('g7','quiz')">✅ Go to Quiz →</button></div>
  </div>
</div>

<!-- QUIZ -->
<div class="section-break" id="quiz"><h2>Lesson Quiz</h2><hr></div>
<div class="quiz-card">
  <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:var(--blue);margin-bottom:4px">📋 End-of-Lesson Check · 20 pts</div>
  <div id="quiz-prog" style="font-size:.72rem;color:var(--muted);margin-bottom:14px">Question 1 of 5</div>
  <div id="quiz-score-box" style="display:none"></div>
  <div class="q-item" id="qq1">
    <div class="quiz-q">1. Which sentence uses {grammar} correctly?</div>
    <div class="choices" id="quiz-q1">
      <div class="choice" onclick="quizPick(this,1,'b')"><div class="mark"></div>She is start in HR last year.</div>
      <div class="choice" onclick="quizPick(this,1,'a')"><div class="mark"></div>She started in HR last year. ✓</div>
      <div class="choice" onclick="quizPick(this,1,'b')"><div class="mark"></div>She has started in HR last year.</div>
    </div>
  </div>
  <div class="q-item" id="qq2" style="display:none">
    <div class="quiz-q">2. Complete: "We _____ any candidates." (negative)</div>
    <div class="choices" id="quiz-q2">
      <div class="choice" onclick="quizPick(this,2,'b')"><div class="mark"></div>didn't hired</div>
      <div class="choice" onclick="quizPick(this,2,'a')"><div class="mark"></div>didn't hire ✓</div>
      <div class="choice" onclick="quizPick(this,2,'b')"><div class="mark"></div>not hired</div>
    </div>
  </div>
  <div class="q-item" id="qq3" style="display:none">
    <div class="quiz-q">3. "Applied" means…</div>
    <div class="choices" id="quiz-q3">
      <div class="choice" onclick="quizPick(this,3,'b')"><div class="mark"></div>started a new job</div>
      <div class="choice" onclick="quizPick(this,3,'a')"><div class="mark"></div>formally requested a position ✓</div>
      <div class="choice" onclick="quizPick(this,3,'b')"><div class="mark"></div>graduated from university</div>
    </div>
  </div>
  <div class="q-item" id="qq4" style="display:none">
    <div class="quiz-q">4. Which question is correct?</div>
    <div class="choices" id="quiz-q4">
      <div class="choice" onclick="quizPick(this,4,'b')"><div class="mark"></div>Did she worked there?</div>
      <div class="choice" onclick="quizPick(this,4,'a')"><div class="mark"></div>Did she work there? ✓</div>
      <div class="choice" onclick="quizPick(this,4,'b')"><div class="mark"></div>Does she worked there?</div>
    </div>
  </div>
  <div class="q-item" id="qq5" style="display:none">
    <div class="quiz-q">5. "Joined" means…</div>
    <div class="choices" id="quiz-q5">
      <div class="choice" onclick="quizPick(this,5,'b')"><div class="mark"></div>left the company</div>
      <div class="choice" onclick="quizPick(this,5,'b')"><div class="mark"></div>started university</div>
      <div class="choice" onclick="quizPick(this,5,'a')"><div class="mark"></div>became part of a team ✓</div>
    </div>
  </div>
</div>

<!-- WRAP UP -->
<div class="section-break" id="wrapup"><h2>Lesson Wrap-Up</h2><hr></div>
<div class="stage" style="box-shadow:none">
  <div class="stage-head"><span class="stage-badge badge-g">✅ Self Check</span><span class="stage-title">What Can You Do Now?</span></div>
  <div class="stage-body">
    <ul class="cando-list">
      <li class="cando-item" onclick="this.querySelector('input').checked=!this.querySelector('input').checked;this.classList.toggle('checked')"><input type="checkbox"> I can use {grammar.lower()} in professional HR contexts.</li>
      <li class="cando-item" onclick="this.querySelector('input').checked=!this.querySelector('input').checked;this.classList.toggle('checked')"><input type="checkbox"> I can form negatives and questions correctly.</li>
      <li class="cando-item" onclick="this.querySelector('input').checked=!this.querySelector('input').checked;this.classList.toggle('checked')"><input type="checkbox"> I can write a short professional message using this grammar.</li>
      <li class="cando-item" onclick="this.querySelector('input').checked=!this.querySelector('input').checked;this.classList.toggle('checked')"><input type="checkbox"> I understand {char} talking about their work.</li>
    </ul>
    <div style="font-family:'Syne',sans-serif;font-size:.82rem;font-weight:800;color:var(--blue);margin-top:12px;margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em">Vocabulary from This Lesson</div>
    <div class="vocab-grid">
      <div class="vg-item"><strong>started</strong><span>empezar</span></div>
      <div class="vg-item"><strong>graduated</strong><span>graduarse</span></div>
      <div class="vg-item"><strong>applied</strong><span>postular</span></div>
      <div class="vg-item"><strong>received</strong><span>recibir</span></div>
      <div class="vg-item"><strong>worked</strong><span>trabajar</span></div>
      <div class="vg-item"><strong>joined</strong><span>unirse</span></div>
      <div class="vg-item"><strong>changed</strong><span>cambiar</span></div>
      <div class="vg-item"><strong>moved</strong><span>mudarse</span></div>
      <div class="vg-item"><strong>wanted</strong><span>querer</span></div>
    </div>
    <div class="badge-row" style="margin-top:10px">
      <div class="badge" id="badge-final">🏆 Lesson Complete</div>
    </div>
    <div class="btn-row" style="margin-top:8px"><button class="btn green" onclick="finishLesson()">🎉 Finish Lesson</button></div>
  </div>
</div>

</div><!-- /shell -->

<script>
const STAGES=['v1','v2','v3','v4','v5','v6','v7','g1','g2','g3','g4','g5','g6','g7'];
const done=new Set();let xp=0;let quizCurrent=1;
const quizCorrect={{1:'a',2:'a',3:'a',4:'a',5:'a'}};let quizScore=0;
let matchFirst=null;let memFlipped=[],memLock=false,memFound=0;

function addXP(n){{xp+=n;document.getElementById('xp').textContent=xp;}}
function updateProg(){{const p=Math.round(done.size/14*100);document.getElementById('prog').style.width=p+'%';document.getElementById('prog-txt').textContent=p+'%';}}
function jumpTo(id){{const el=document.getElementById(id);if(el)el.scrollIntoView({{behavior:'smooth',block:'start'}});}}
function completeStage(id,next){{if(!done.has(id)){{done.add(id);addXP(25);}}updateProg();const nb=document.getElementById('nav-'+id);if(nb)nb.classList.add('done');if(next)setTimeout(()=>jumpTo(next),300);}}
function showFB(id,type,msg){{const el=document.getElementById(id);if(!el)return;el.className='fb '+type;el.style.display='flex';el.textContent=msg;}}
function toggleObs(el,r){{el.classList.toggle('chosen');if(r==='correct')el.classList.toggle('correct',el.classList.contains('chosen'));else el.classList.toggle('wrong',el.classList.contains('chosen'));}}
function pickOne(el,gId,r){{const g=document.getElementById(gId);if(!g)return;g.querySelectorAll('.choice').forEach(c=>c.classList.remove('correct','wrong','chosen'));el.classList.add(r==='correct'?'correct':'wrong');if(r==='correct')addXP(10);}}
function quizQ(el,idx,r){{const p=el.closest('.choices');p.querySelectorAll('.choice').forEach(c=>c.classList.remove('correct','wrong'));el.classList.add(r==='a'?'correct':'wrong');if(r==='a')addXP(5);}}
function matchClick(el){{if(el.classList.contains('matched'))return;if(!matchFirst){{el.classList.add('selected');matchFirst=el;}}else{{if(matchFirst===el){{matchFirst.classList.remove('selected');matchFirst=null;return;}}if(matchFirst.dataset.pair===el.dataset.pair){{matchFirst.classList.remove('selected');matchFirst.classList.add('matched');el.classList.add('matched');addXP(15);matchFirst=null;const all=document.querySelectorAll('#v2-match .match-item');if([...all].every(i=>i.classList.contains('matched'))){{showFB('v2-fb','ok','All matched! ✓ +XP');addXP(20);}}}}else{{matchFirst.classList.add('wrong-flash');el.classList.add('wrong-flash');const a=matchFirst,b=el;matchFirst=null;setTimeout(()=>{{a.classList.remove('wrong-flash');b.classList.remove('wrong-flash');}},500);}}}}}}
function fillInput(id,pill,val){{const inp=document.getElementById(id);if(!inp)return;inp.value=val;inp.style.color='var(--blue)';}}
function checkFills(pairs,fbId){{let ok=0;pairs.forEach(p=>{{const[id,ans]=p.split(':');const inp=document.getElementById(id);if(!inp)return;const match=inp.value.trim().toLowerCase()===ans.toLowerCase();inp.style.borderBottomColor=match?'var(--green)':'var(--red)';if(match)ok++;}});if(ok===pairs.length){{showFB(fbId,'ok','All correct! ✓');addXP(20);}}else showFB(fbId,'err',ok+' of '+pairs.length+' correct.');}}
function unlockBadge(id){{const el=document.getElementById(id);if(el)el.classList.add('earned');}}
function updateCounter(ta,cntId){{const words=ta.value.trim().split(/\s+/).filter(w=>w).length;document.getElementById(cntId).textContent=words;}}
function checkWriteLen(taId,fbId,min){{const ta=document.getElementById(taId);const words=ta.value.trim().split(/\s+/).filter(w=>w).length;if(words>=min){{showFB(fbId,'ok','Good length! Check the suggested answer. ✓');addXP(25);}}else showFB(fbId,'hint','Try to write at least '+min+' words. You have '+words+' so far.');}}
function playAudio(){{const a=document.getElementById('story-audio');if(!a)return;const btn=document.getElementById('story-btn');if(a.paused){{a.play();btn.classList.add('playing');document.getElementById('story-txt').textContent='Pause';a.onended=()=>{{btn.classList.remove('playing');document.getElementById('story-txt').textContent='Play Again';}}}}else{{a.pause();btn.classList.remove('playing');document.getElementById('story-txt').textContent='Play Story';}}}}
function playTTS(lines,btn){{if('speechSynthesis' in window){{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(lines.join(' ... '));u.rate=0.85;u.lang='en-US';btn.classList.add('playing');u.onend=()=>btn.classList.remove('playing');speechSynthesis.speak(u);}}}}
const memPairs=[{{a:'started',b:'empezar'}},{{a:'applied',b:'postular'}},{{a:'joined',b:'unirse'}},{{a:'received',b:'recibir'}}];
function initMemory(){{memFlipped=[];memLock=false;memFound=0;document.getElementById('mem-pairs').textContent='0';const board=document.getElementById('mem-board');const cards=[];memPairs.forEach(({{a,b}})=>{{cards.push({{text:a,pair:a+b}});cards.push({{text:b,pair:a+b}});}});cards.sort(()=>Math.random()-.5);board.innerHTML=cards.map(c=>`<div class="mem-card" data-text="${{c.text}}" data-pair="${{c.pair}}" onclick="memFlip(this)"><div class="mem-card-front">?</div><div class="mem-card-back">${{c.text}}</div></div>`).join('');}}
function memFlip(card){{if(memLock||card.classList.contains('matched')||card.classList.contains('flipped'))return;card.classList.add('flipped');memFlipped.push(card);if(memFlipped.length===2){{memLock=true;const[a,b]=memFlipped;if(a.dataset.pair===b.dataset.pair){{a.classList.add('matched');b.classList.add('matched');a.classList.remove('flipped');b.classList.remove('flipped');memFound++;addXP(15);document.getElementById('mem-pairs').textContent=memFound;memFlipped=[];memLock=false;}}else{{setTimeout(()=>{{a.classList.remove('flipped');b.classList.remove('flipped');memFlipped=[];memLock=false;}},800);}}}}}}
initMemory();
function quizPick(el,q,opt){{const parent=el.closest('.choices');parent.querySelectorAll('.choice').forEach(c=>c.classList.remove('chosen'));el.classList.add('chosen');setTimeout(()=>{{const correct=quizCorrect[q]===opt;parent.querySelectorAll('.choice').forEach((c,i)=>{{const opts=['a','b','c'];if(quizCorrect[q]===opts[i])c.classList.add('correct');else if(c.classList.contains('chosen')&&!correct)c.classList.add('wrong');}});if(correct){{quizScore++;addXP(20);}}setTimeout(()=>{{if(quizCurrent<5){{document.getElementById('qq'+quizCurrent).style.display='none';quizCurrent++;document.getElementById('qq'+quizCurrent).style.display='';document.getElementById('quiz-prog').textContent='Question '+quizCurrent+' of 5';}}else{{document.getElementById('quiz-prog').style.display='none';const pts=quizScore*4;const sb=document.getElementById('quiz-score-box');sb.style.display='block';sb.innerHTML=`<div class="score-box"><div class="score-num">${{pts}}<span style="font-size:1rem">/20</span></div><div class="score-label">${{pts>=16?'Excellent 🏆':pts>=12?'Good job!':'Review & retry'}}</div></div>`;if(pts>=16)unlockBadge('badge-final');sb.scrollIntoView({{behavior:'smooth'}});}}}},900);}},600);}}
function finishLesson(){{unlockBadge('badge-final');alert('🎉 Lesson Complete! You earned '+xp+' XP.');}}

// SCORM 1.2
(function(){{try{{var api=null,w=window;for(var i=0;i<7;i++){{if(w.API){{api=w.API;break;}}if(!w.parent||w.parent===w)break;w=w.parent;}}if(api){{api.LMSInitialize('');window.addEventListener('beforeunload',function(){{var pct=Math.round(done.size/14*100);api.LMSSetValue('cmi.core.lesson_status',pct>=80?'passed':'incomplete');api.LMSSetValue('cmi.core.score.raw',String(xp));api.LMSSetValue('cmi.core.score.min','0');api.LMSSetValue('cmi.core.score.max','500');api.LMSCommit('');api.LMSFinish('');}});}}}}catch(e){{}}}}());
</script>
</body>
</html>"""


def build_scorm_zip(lesson_id, html_content, manifest_content, audio_src=None):
    """Creates a SCORM 1.2 zip file for one lesson"""
    zip_path = os.path.join(OUT_DIR, f"HKO_A2_{lesson_id}_SCORM.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("imsmanifest.xml", manifest_content)
        zf.writestr("lesson.html", html_content)
        # Include audio if it exists locally
        if audio_src and os.path.exists(audio_src):
            fname = os.path.basename(audio_src)
            zf.write(audio_src, f"audio/{fname.lower().replace('gen_a2_', '').replace('_aud_story_v1','_audio')}")

    size_kb = os.path.getsize(zip_path) // 1024
    print(f"  Built: {os.path.basename(zip_path)} ({size_kb}KB)")
    return zip_path


def build_midcourse_quiz():
    """Build the mid-course quiz (after L6) as standalone SCORM"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>HKO A2 — Mid-Course Progress Quiz</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Syne:wght@700;800&display=swap');
:root{--blue:#28597A;--green:#2E8B57;--amber:#c87137;--red:#e03131;--bg:#f4f6fb;--card:#fff;--line:#e2e8f0;--muted:#7a8fa6}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:#0f1923;font-size:15px;line-height:1.55}
.shell{max-width:760px;margin:0 auto;padding:24px 16px 80px}
.hero{background:linear-gradient(135deg,#0f1923,#1a3a60);border-radius:16px;padding:28px;color:#fff;margin-bottom:20px}
.hero h1{font-family:'Syne',sans-serif;font-size:1.6rem;margin-bottom:8px}
.hero p{opacity:.7;font-size:.9rem}
.hero-stats{display:flex;gap:12px;margin-top:14px}
.hstat{background:rgba(255,255,255,.1);border-radius:8px;padding:8px 14px;text-align:center}
.hstat strong{display:block;font-size:1.1rem;font-family:'Syne',sans-serif}
.hstat span{font-size:.68rem;opacity:.6;text-transform:uppercase;letter-spacing:.06em}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:12px}
.q-num{font-size:.72rem;font-weight:800;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px}
.q-text{font-size:.92rem;font-weight:700;color:#0f1923;margin-bottom:12px}
.choice{padding:10px 14px;border-radius:9px;border:1.5px solid var(--line);background:#fafbfc;font-size:.85rem;cursor:pointer;margin-bottom:7px;display:flex;align-items:center;gap:8px;transition:all .15s}
.choice:hover{border-color:var(--blue);background:#e8f2f8}
.mark{width:18px;height:18px;border-radius:50%;border:2px solid var(--line);flex-shrink:0}
.choice.correct{background:#ebfbee;border-color:#7cc090;color:var(--green)}
.choice.wrong{background:#fff0f0;border-color:#f4b8b8;color:var(--red)}
.score-display{background:linear-gradient(135deg,#e8f2f8,#e3fafc);border:1px solid #b8d4e4;border-radius:12px;padding:24px;text-align:center;display:none}
.score-num{font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:var(--blue)}
.score-label{color:var(--muted);font-size:.82rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-top:4px}
.score-msg{margin-top:12px;font-size:.9rem;color:#3d4f5c}
.btn{border:none;border-radius:9px;padding:10px 18px;font-family:inherit;font-size:.85rem;font-weight:700;cursor:pointer}
.btn-primary{background:var(--blue);color:#fff}
.section-hdr{font-family:'Syne',sans-serif;font-size:.82rem;font-weight:800;color:var(--blue);text-transform:uppercase;letter-spacing:.08em;padding:8px 0 4px;border-bottom:2px solid #e8f2f8;margin-bottom:10px;margin-top:20px}
.progress-bar-wrap{background:#f0f3f8;border-radius:99px;height:8px;margin-bottom:16px;overflow:hidden}
.progress-bar-fill{height:100%;background:linear-gradient(90deg,var(--blue),var(--green));border-radius:99px;transition:width .4s}
</style>
</head>
<body>
<div class="shell">
<div class="hero">
  <h1>Mid-Course Progress Quiz</h1>
  <p>Lessons 1–6 · A2 HR English · 40 points total</p>
  <div class="hero-stats">
    <div class="hstat"><strong>20</strong><span>Questions</span></div>
    <div class="hstat"><strong>40</strong><span>Points</span></div>
    <div class="hstat"><strong>60%</strong><span>To Pass</span></div>
  </div>
</div>

<div class="progress-bar-wrap"><div class="progress-bar-fill" id="quiz-prog" style="width:0%"></div></div>
<div id="score-display" class="score-display"></div>
<div id="quiz-container"></div>
<div id="submit-row" style="text-align:center;margin-top:16px">
  <button class="btn btn-primary" onclick="submitQuiz()">Submit Quiz →</button>
</div>
</div>
<script>
const questions=[
  {sec:"Module 1 — Past Simple",q:"1. María ___ in HR five years ago.",opts:["start","started","is starting"],a:1},
  {sec:null,q:"2. She ___ from university in 2018.",opts:["graduate","graduating","graduated"],a:2},
  {sec:null,q:"3. They ___ 80 applications last week.",opts:["receive","received","are receiving"],a:1},
  {sec:null,q:"4. Which is correct?",opts:["She didn't worked in payroll.","She didn't work in payroll.","She not worked in payroll."],a:1},
  {sec:null,q:"5. ___ you work at MineSafe before?",opts:["Do","Did","Are"],a:1},
  {sec:"Module 2 — Negative & Questions",q:"6. Carlos ___ expect so many applications.",opts:["doesn't","didn't","not"],a:1},
  {sec:null,q:"7. They ___ respond to our emails.",opts:["didn't","not","wasn't"],a:0},
  {sec:null,q:"8. ___ did she work before joining MineSafe?",opts:["When","What","Which"],a:0},
  {sec:null,q:"9. How long ___ you work there?",opts:["did","do","are"],a:0},
  {sec:null,q:"10. 'Applied' means…",opts:["became part of a team","formally requested a job","finished university"],a:1},
  {sec:"Module 3 — Going To",q:"11. I ___ review the CVs tomorrow.",opts:["am going to","will going to","going to"],a:0},
  {sec:null,q:"12. She ___ call the candidates this afternoon.",opts:["is go to","is going to","are going to"],a:1},
  {sec:null,q:"13. ___ you going to post the job today?",opts:["Are","Is","Am"],a:0},
  {sec:null,q:"14. They ___ hire anyone this month. (negative)",opts:["isn't going to","aren't going to","not going to"],a:1},
  {sec:null,q:"15. 'I am going to review' shows…",opts:["a completed past action","a planned future action","a present habit"],a:1},
  {sec:"Module 4-6 — Will & Future",q:"16. I ___ send you the job description today.",opts:["will","am going to","both are correct"],a:2},
  {sec:null,q:"17. ___ you post the role on Friday?",opts:["Will","Are","Do"],a:0},
  {sec:null,q:"18. She ___ be at the interview tomorrow.",opts:["won't","isn't going","not will"],a:0},
  {sec:null,q:"19. 'I'll help you' expresses…",opts:["a past action","a future offer","a present habit"],a:1},
  {sec:null,q:"20. When ___ the results be ready?",opts:["will","are","do"],a:0},
];

let answers={};let submitted=false;

function renderQuiz(){
  const c=document.getElementById('quiz-container');
  let html='';let lastSec=null;
  questions.forEach((q,i)=>{
    if(q.sec&&q.sec!==lastSec){html+=`<div class="section-hdr">${q.sec}</div>`;lastSec=q.sec;}
    html+=`<div class="card"><div class="q-num">Question ${i+1} of ${questions.length}</div><div class="q-text">${q.q}</div>`;
    q.opts.forEach((opt,oi)=>{
      html+=`<div class="choice" id="q${i}_o${oi}" onclick="selectAnswer(${i},${oi})"><div class="mark"></div>${opt}</div>`;
    });
    html+='</div>';
  });
  c.innerHTML=html;
}

function selectAnswer(qi,oi){
  if(submitted)return;
  const q=questions[qi];
  q.opts.forEach((_,i)=>{document.getElementById('q'+qi+'_o'+i).classList.remove('chosen');});
  document.getElementById('q'+qi+'_o'+oi).classList.add('chosen','selected-ans');
  answers[qi]=oi;
  const pct=Math.round(Object.keys(answers).length/questions.length*100);
  document.getElementById('quiz-prog').style.width=pct+'%';
}

function submitQuiz(){
  if(submitted)return;
  submitted=true;
  let score=0;
  questions.forEach((q,i)=>{
    q.opts.forEach((_,oi)=>{
      const el=document.getElementById('q'+i+'_o'+oi);
      if(oi===q.a){el.classList.add('correct');}
      else if(answers[i]===oi&&oi!==q.a){el.classList.add('wrong');}
    });
    if(answers[i]===q.a)score++;
  });
  const pts=score*2;
  const pct=Math.round(score/questions.length*100);
  const sd=document.getElementById('score-display');
  sd.style.display='block';
  sd.innerHTML=`<div class="score-num">${pts}<span style="font-size:1.2rem">/40</span></div><div class="score-label">${pct}% — ${pct>=60?'PASSED ✓':'Not yet passed'}</div><div class="score-msg">${score} of ${questions.length} correct.<br>${pct>=80?'Excellent work! You are ready for Module 2.':pct>=60?'Good job! Review the questions you missed.':'Review Lessons 1–6 and try again.'}</div>`;
  sd.scrollIntoView({behavior:'smooth'});
  document.getElementById('submit-row').style.display='none';
  // SCORM
  try{var api=null,w=window;for(var i=0;i<7;i++){if(w.API){api=w.API;break;}if(!w.parent||w.parent===w)break;w=w.parent;}if(api){api.LMSInitialize('');api.LMSSetValue('cmi.core.lesson_status',pct>=60?'passed':'failed');api.LMSSetValue('cmi.core.score.raw',String(pts));api.LMSSetValue('cmi.core.score.min','0');api.LMSSetValue('cmi.core.score.max','40');api.LMSCommit('');api.LMSFinish('');}}catch(e){}
}
renderQuiz();
</script>
</body>
</html>"""

    manifest = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="HKO_A2_MID_QUIZ" version="1.1"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2">
  <metadata><schema>ADL SCORM</schema><schemaversion>1.2</schemaversion></metadata>
  <organizations default="ORG_MID">
    <organization identifier="ORG_MID">
      <title>A2 HR English — Mid-Course Progress Quiz (Lessons 1-6)</title>
      <item identifier="ITEM_MID" identifierref="RES_MID">
        <title>Mid-Course Quiz · 40 Points</title>
        <adlcp:masteryscore>60</adlcp:masteryscore>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES_MID" type="webcontent" adlcp:scormtype="sco" href="lesson.html">
      <file href="lesson.html"/>
    </resource>
  </resources>
</manifest>"""

    zip_path = os.path.join(OUT_DIR, "HKO_A2_MID_QUIZ_SCORM.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("imsmanifest.xml", manifest)
        zf.writestr("lesson.html", html)
    print(f"  Built: {os.path.basename(zip_path)}")
    return zip_path


def build_final_quiz():
    """Build the final course quiz as standalone SCORM"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>HKO A2 — Final Course Assessment</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Syne:wght@700;800&display=swap');
:root{--blue:#28597A;--green:#2E8B57;--amber:#c87137;--red:#e03131;--bg:#f4f6fb;--card:#fff;--line:#e2e8f0;--muted:#7a8fa6}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:#0f1923;font-size:15px;line-height:1.55}
.shell{max-width:760px;margin:0 auto;padding:24px 16px 80px}
.hero{background:linear-gradient(135deg,#0f1923,#2E8B57);border-radius:16px;padding:28px;color:#fff;margin-bottom:20px}
.hero h1{font-family:'Syne',sans-serif;font-size:1.6rem;margin-bottom:8px}
.hero p{opacity:.7;font-size:.9rem}
.hero-stats{display:flex;gap:12px;margin-top:14px}
.hstat{background:rgba(255,255,255,.1);border-radius:8px;padding:8px 14px;text-align:center}
.hstat strong{display:block;font-size:1.1rem;font-family:'Syne',sans-serif}
.hstat span{font-size:.68rem;opacity:.6;text-transform:uppercase;letter-spacing:.06em}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:12px}
.q-num{font-size:.72rem;font-weight:800;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px}
.q-text{font-size:.92rem;font-weight:700;color:#0f1923;margin-bottom:12px}
.choice{padding:10px 14px;border-radius:9px;border:1.5px solid var(--line);background:#fafbfc;font-size:.85rem;cursor:pointer;margin-bottom:7px;display:flex;align-items:center;gap:8px;transition:all .15s}
.choice:hover{border-color:var(--blue);background:#e8f2f8}
.mark{width:18px;height:18px;border-radius:50%;border:2px solid var(--line);flex-shrink:0}
.choice.correct{background:#ebfbee;border-color:#7cc090;color:var(--green)}
.choice.wrong{background:#fff0f0;border-color:#f4b8b8;color:var(--red)}
.score-display{background:linear-gradient(135deg,#ebfbee,#e3fafc);border:1px solid #7cc090;border-radius:12px;padding:24px;text-align:center;display:none}
.score-num{font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:var(--green)}
.score-label{color:var(--muted);font-size:.82rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-top:4px}
.btn{border:none;border-radius:9px;padding:10px 18px;font-family:inherit;font-size:.85rem;font-weight:700;cursor:pointer}
.btn-primary{background:var(--green);color:#fff}
.section-hdr{font-family:'Syne',sans-serif;font-size:.82rem;font-weight:800;color:var(--green);text-transform:uppercase;letter-spacing:.08em;padding:8px 0 4px;border-bottom:2px solid #ebfbee;margin-bottom:10px;margin-top:20px}
.progress-bar-wrap{background:#f0f3f8;border-radius:99px;height:8px;margin-bottom:16px;overflow:hidden}
.progress-bar-fill{height:100%;background:linear-gradient(90deg,var(--blue),var(--green));border-radius:99px;transition:width .4s}
.cert-badge{background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;border-radius:12px;padding:16px;text-align:center;margin-top:16px;display:none}
.cert-badge h3{font-family:'Syne',sans-serif;font-size:1.1rem;margin-bottom:4px}
</style>
</head>
<body>
<div class="shell">
<div class="hero">
  <h1>Final Course Assessment</h1>
  <p>All 12 Lessons · A2 HR English · CEFR Certification Ready</p>
  <div class="hero-stats">
    <div class="hstat"><strong>25</strong><span>Questions</span></div>
    <div class="hstat"><strong>100</strong><span>Points</span></div>
    <div class="hstat"><strong>60%</strong><span>To Pass</span></div>
  </div>
</div>
<div class="progress-bar-wrap"><div class="progress-bar-fill" id="quiz-prog" style="width:0%"></div></div>
<div id="score-display" class="score-display"></div>
<div id="cert-badge" class="cert-badge"><h3>🏆 Certificate of Completion</h3><p>A2 HR English — HKO Professional Series</p></div>
<div id="quiz-container"></div>
<div id="submit-row" style="text-align:center;margin-top:16px">
  <button class="btn btn-primary" onclick="submitQuiz()">Submit Final Assessment →</button>
</div>
</div>
<script>
const questions=[
  {sec:"Past Simple (L1-L4)",q:"1. She ___ in HR five years ago.",opts:["start","started","is starting"],a:1},
  {sec:null,q:"2. They ___ any applications last week. (negative)",opts:["didn't receive","not received","didn't received"],a:0},
  {sec:null,q:"3. ___ you work at MineSafe before?",opts:["Do","Did","Are"],a:1},
  {sec:null,q:"4. He ___ to the interview. (irregular verb)",opts:["goed","went","goes"],a:1},
  {sec:null,q:"5. The interview ___ one hour.",opts:["taked","tooken","took"],a:2},
  {sec:"Future (L5-L7)",q:"6. I ___ review the CVs tomorrow. (plan)",opts:["am going to","will going to","going to"],a:0},
  {sec:null,q:"7. I'll send you the document. 'I'll' means…",opts:["I am","I will","I have"],a:1},
  {sec:null,q:"8. ___ you post the role on Friday?",opts:["Will","Are going","Do"],a:0},
  {sec:null,q:"9. She ___ attend the meeting. (negative future)",opts:["won't","not will","isn't go to"],a:0},
  {sec:null,q:"10. When ___ the results be ready?",opts:["will","are","do"],a:0},
  {sec:"Comparatives & Superlatives (L8-L10)",q:"11. Ana is ___ experienced than Luis.",opts:["more","most","much"],a:0},
  {sec:null,q:"12. She has the ___ score of all candidates.",opts:["higher","more higher","highest"],a:2},
  {sec:null,q:"13. Our process is ___ now than before.",opts:["more fast","faster","most fast"],a:1},
  {sec:null,q:"14. This candidate is ___ than that one.",opts:["gooder","more good","better"],a:2},
  {sec:null,q:"15. We respond ___ than we did last year. (adverb)",opts:["more quickly","more quick","quicklier"],a:0},
  {sec:"Present Perfect (L11-L12)",q:"16. ___ you worked in HR before?",opts:["Did","Have","Do"],a:1},
  {sec:null,q:"17. I've worked here ___ five years.",opts:["since","for","ago"],a:1},
  {sec:null,q:"18. She has worked here ___ 2020.",opts:["for","ago","since"],a:2},
  {sec:null,q:"19. We've ___ hired three new people.",opts:["just","yet","ago"],a:0},
  {sec:null,q:"20. Have you reviewed the profiles ___?",opts:["just","already","yet"],a:2},
  {sec:"Vocabulary",q:"21. 'Applied' means…",opts:["became part of a team","formally requested a job","finished university"],a:1},
  {sec:null,q:"22. 'Shortlisted' means…",opts:["rejected all candidates","selected the best candidates for next stage","interviewed all candidates"],a:1},
  {sec:null,q:"23. 'Onboarding' means…",opts:["the process of leaving a company","the process of integrating new employees","a type of job interview"],a:1},
  {sec:null,q:"24. 'Candidate' means…",opts:["a recruiter","a hiring manager","a person applying for a job"],a:2},
  {sec:null,q:"25. 'Recruitment' means…",opts:["the process of finding and hiring employees","a type of HR report","a salary negotiation"],a:0},
];

let answers={};let submitted=false;

function renderQuiz(){
  const c=document.getElementById('quiz-container');
  let html='';let lastSec=null;
  questions.forEach((q,i)=>{
    if(q.sec&&q.sec!==lastSec){html+=`<div class="section-hdr">${q.sec}</div>`;lastSec=q.sec;}
    html+=`<div class="card"><div class="q-num">Question ${i+1} of ${questions.length}</div><div class="q-text">${q.q}</div>`;
    q.opts.forEach((opt,oi)=>{html+=`<div class="choice" id="q${i}_o${oi}" onclick="selectAnswer(${i},${oi})"><div class="mark"></div>${opt}</div>`;});
    html+='</div>';
  });
  c.innerHTML=html;
}

function selectAnswer(qi,oi){
  if(submitted)return;
  questions[qi].opts.forEach((_,i)=>{document.getElementById('q'+qi+'_o'+i).classList.remove('chosen');});
  document.getElementById('q'+qi+'_o'+oi).classList.add('chosen');
  answers[qi]=oi;
  document.getElementById('quiz-prog').style.width=Math.round(Object.keys(answers).length/questions.length*100)+'%';
}

function submitQuiz(){
  if(submitted)return;submitted=true;
  let score=0;
  questions.forEach((q,i)=>{
    q.opts.forEach((_,oi)=>{
      const el=document.getElementById('q'+i+'_o'+oi);
      if(oi===q.a)el.classList.add('correct');
      else if(answers[i]===oi&&oi!==q.a)el.classList.add('wrong');
    });
    if(answers[i]===q.a)score++;
  });
  const pts=Math.round(score/questions.length*100);
  const sd=document.getElementById('score-display');
  sd.style.display='block';
  sd.innerHTML=`<div class="score-num">${score}<span style="font-size:1.2rem">/${questions.length}</span></div><div class="score-label">${pts}% — ${pts>=60?'PASSED ✓':'Not yet passed'}</div><div style="margin-top:12px;font-size:.9rem;color:#3d4f5c">${pts>=80?'Excellent! You have demonstrated A2 HR English competency.':pts>=60?'Good work! You have passed the A2 course.':'Please review the course materials and try again.'}</div>`;
  if(pts>=60){document.getElementById('cert-badge').style.display='block';}
  sd.scrollIntoView({behavior:'smooth'});
  document.getElementById('submit-row').style.display='none';
  try{var api=null,w=window;for(var i=0;i<7;i++){if(w.API){api=w.API;break;}if(!w.parent||w.parent===w)break;w=w.parent;}if(api){api.LMSInitialize('');api.LMSSetValue('cmi.core.lesson_status',pts>=60?'passed':'failed');api.LMSSetValue('cmi.core.score.raw',String(score));api.LMSSetValue('cmi.core.score.min','0');api.LMSSetValue('cmi.core.score.max',String(questions.length));api.LMSCommit('');api.LMSFinish('');}}catch(e){}
}
renderQuiz();
</script>
</body>
</html>"""

    manifest = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="HKO_A2_FINAL_QUIZ" version="1.1"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2">
  <metadata><schema>ADL SCORM</schema><schemaversion>1.2</schemaversion></metadata>
  <organizations default="ORG_FINAL">
    <organization identifier="ORG_FINAL">
      <title>A2 HR English — Final Course Assessment · CEFR A2</title>
      <item identifier="ITEM_FINAL" identifierref="RES_FINAL">
        <title>Final Assessment · 100 Points · SENCE Certification</title>
        <adlcp:masteryscore>60</adlcp:masteryscore>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES_FINAL" type="webcontent" adlcp:scormtype="sco" href="lesson.html">
      <file href="lesson.html"/>
    </resource>
  </resources>
</manifest>"""

    zip_path = os.path.join(OUT_DIR, "HKO_A2_FINAL_QUIZ_SCORM.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("imsmanifest.xml", manifest)
        zf.writestr("lesson.html", html)
    print(f"  Built: {os.path.basename(zip_path)}")
    return zip_path


if __name__ == "__main__":
    print("=" * 60)
    print("HKO A2 SCORM Builder")
    print("=" * 60)
    print(f"Output folder: ./{OUT_DIR}/")
    print()

    built = []

    # Build 12 lessons
    for lesson_id, meta in LESSON_META.items():
        print(f"[{lesson_id}] {meta['title']}")
        imgs = IMAGES[lesson_id]

        # Check for local audio
        audio_filename = f"GEN_A2_{lesson_id}_AUD_STORY_V1.mp3"
        audio_src = os.path.join(AUDIO_DIR, audio_filename)
        has_audio = os.path.exists(audio_src)

        # For HTML: audio path is relative inside zip
        if has_audio:
            audio_rel = f"audio/{lesson_id.lower()}_audio.mp3"
        else:
            audio_rel = None

        html = make_lesson_html(lesson_id, meta, imgs, audio_rel)
        manifest = make_imsmanifest(lesson_id, meta["title"], has_audio)
        zip_path = build_scorm_zip(lesson_id, html, manifest, audio_src if has_audio else None)
        built.append(zip_path)

    print()

    # Build 2 quizzes
    print("[MID QUIZ] Mid-Course Progress Quiz (after L6)")
    built.append(build_midcourse_quiz())

    print("[FINAL QUIZ] Final Course Assessment")
    built.append(build_final_quiz())

    print()
    print("=" * 60)
    print(f"COMPLETE: {len(built)} SCORM packages built")
    print(f"Location: ./{OUT_DIR}/")
    print()
    print("Files ready to upload to Moodle:")
    for f in built:
        size = os.path.getsize(f) // 1024
        print(f"  {os.path.basename(f)} ({size}KB)")
    print()
    print("NEXT STEP for audio:")
    print("  1. Fill your ElevenLabs API key in generate_audio.py")
    print("  2. Run: python generate_audio.py")
    print("  3. Run: python build_scorm.py  (will include audio in zips)")
    print()
    print("NEXT STEP for missing images (L09-L12):")
    print("  Generate in Gemini/MidJourney and push to GitHub root")
    print("  Update IMAGES dict in this script with new filenames")
    print("  Re-run: python build_scorm.py")
