# HKO ESL Generator 2030
Session ocean-wren-3745 · Sun, 15 Mar 2026 19:27:26 GMT
Build Standard 2030.1 · Health 24/100 · Status RUNNING

---

## Architecture

```
Tauri Desktop App / esl-ui
hko-esl-assembler.html  ──POST──▶  brein            (orchestrator / API gateway)
                                     ├──queue──▶  lesson-planner   (LLM plan + activity design)
                                     ├──queue──▶  image-gen        (Flux → GitHub)
                                     ├──queue──▶  audio-gen        (TTS → GitHub)
                                     ├──queue──▶  assembler        (HTML → GitHub)
                                     ├──queue──▶  visual-check     (image QA + lesson density check)
                                     ├──queue──▶  video-gen        (PPT storyboard → video → GitHub)
                                     └──HTTP──▶   asset-manager    (signed GitHub URLs)

esl-ui       ──serves──▶  Generator UI (single HTML page served from worker)
hko-oracle   ──HTTP──▶    Lesson data API (list / search / get / delete)
d1-template  ──HTTP──▶    D1 schema manager (setup / migrate / seed / reset)
```

**Asset storage: GitHub repository (not R2)**
All generated images, audio, HTML lessons, and videos are committed to GitHub via the Contents API.
asset-manager serves signed redirect URLs pointing to `raw.githubusercontent.com`.

---

## Workers — Complete Reference

| Worker | Function | URL | Auth |
|--------|----------|-----|------|
| **brein** | Orchestrator & API gateway — routes all client requests, manages job lifecycle | https://brein.mrhkruger.workers.dev | BREIN_API_KEY |
| **lesson-planner** | LLM lesson plan generator — Llama 3.3 70b + KV cache + activity design decisions | https://lesson-planner.mrhkruger.workers.dev | API_SECRET |
| **image-gen** | Flux 1 Schnell image generation → commits PNG to GitHub | https://image-gen.mrhkruger.workers.dev | API_SECRET |
| **audio-gen** | Deepgram aura-2-en TTS → MP3 → commits to GitHub | https://audio-gen.mrhkruger.workers.dev | API_SECRET |
| **assembler** | Assembles full lesson HTML from plan + asset URLs → commits to GitHub | https://assembler.mrhkruger.workers.dev | API_SECRET |
| **visual-check** | QA pass — image quality + lesson density check, flags sparse lessons for enrichment | https://visual-check.mrhkruger.workers.dev | API_SECRET |
| **video-gen** | PPT storyboard builder → exports video → commits to GitHub | https://video-gen.mrhkruger.workers.dev | API_SECRET |
| **asset-manager** | Signed redirect URLs for all GitHub-hosted assets | https://asset-manager.mrhkruger.workers.dev | R2_SIGN_SECRET |
| **esl-ui** | Generator UI — single HTML page served from worker | https://esl-ui.mrhkruger.workers.dev | optional |
| **hko-oracle** | Lesson data API — list, search, get, update, delete from D1 | https://hko-oracle.mrhkruger.workers.dev | API_SECRET |
| **d1-template** | D1 schema manager — migrations, seed, status, reset | https://d1-template.mrhkruger.workers.dev | API_SECRET (required) |

---

## GitHub Setup

### Repositories

| Repo | Purpose | URL |
|------|---------|-----|
| `hko-esl-repo` | All generated lesson assets — HTML, images, audio, video, quizzes | github.com/BTHKO/hko-esl-repo |
| `HKO_ESL_GENERATOR` | Tauri app source + all worker source code | github.com/BTHKO/HKO_ESL_GENERATOR |

### hko-esl-repo — Folder Structure

```
hko-esl-repo/
│
├── _GLOBAL_STANDARDS_RULES/                                   ← READ FIRST — every generation
│   ├── ESL_BUILDER_MASTERBRIEF_TEMPLATEANDRULE_STANDARDS.md   ← canonical rules — all workers
│   ├── HKO_UNIFIED_LESSON_TEMPLATE_V2.html                    ← assembler base template
│   ├── HTML5_EDITING_GUIDE.md
│   ├── COMPLETE_ASSESSMENT_BANK_A1_C2.md
│   ├── REPLICATION_GUIDE.md
│   ├── TEMPLATE_1_Grammar_Presentation_Format.md
│   ├── TEMPLATE_2_Vocabulary_Glossary_Format.md
│   ├── TEMPLATE_3_4_5_COURSE_STRUCTURES.md
│   ├── SENCE COURSES CDO 2026.md
│   ├── PROJECT_SUMMARY_COMPLETE.md
│   ├── README.md
│   └── GRAMMAR VOCAB BOX.html
│
├── 1.A2/
│   ├── A2_COMPLETE_COURSE_12_LESSONS.md     ← level-specific lesson content + characters
│   ├── A2_ASSET_LIST.html
│   ├── A2 COMPLETED LESSONS/                ← approved final lessons
│   ├── A2_LESSONS_TO_REDO/                  ← generated / working lessons
│   │   ├── L##_v2.html
│   │   ├── L##_quiz.html
│   │   ├── L##_quiz.gift.txt
│   │   ├── UNIT6_quiz.html
│   │   └── FINAL_quiz.html
│   ├── A2_AUDIOS/                           ← L##_audio.mp3, L##_dialogue.mp3
│   ├── A2_IIMAGES/                          ← L##_img1.png … L##_img5.png
│   └── A2_VIDEOS/                           ← L##_storyboard.pptx, L##_video.mp4
│
├── 2. B1/    ← identical structure
├── 3. C1/
└── 4.A1/
```

### GitHub Token — Required Scopes
```
repo (full)   — read/write files via Contents API
```

### GitHub Contents API Write Pattern
```javascript
const existing = await fetch(
  `https://api.github.com/repos/BTHKO/hko-esl-repo/contents/${path}`,
  { headers: { 'Authorization': `Bearer ${env.GITHUB_TOKEN}` } }
).then(r => r.ok ? r.json() : null);

await fetch(
  `https://api.github.com/repos/BTHKO/hko-esl-repo/contents/${path}`,
  {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${env.GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: `[auto] ${path}`,
      content: btoa(fileContent),
      sha: existing?.sha || undefined,
    }),
  }
);
```

### Asset Naming Convention

| Asset | Path in repo | Notes |
|-------|-------------|-------|
| Lesson HTML | `{level}/LESSONS_TO_REDO/L##_v2.html` | Assembled by assembler |
| Quiz HTML | `{level}/LESSONS_TO_REDO/L##_quiz.html` | |
| GIFT quiz | `{level}/LESSONS_TO_REDO/L##_quiz.gift.txt` | Moodle import |
| Image 1–5 | `{level}/IMAGES/L##_img1.png … L##_img5.png` | lesson-planner decides count (3–5) |
| Activity image | `{level}/IMAGES/L##_act_S#_img.png` | Image used inside a specific activity |
| Audio main | `{level}/AUDIOS/L##_audio.mp3` | Monologue or combined dialogue |
| Dialogue audio | `{level}/AUDIOS/L##_dialogue_A.mp3`, `_B.mp3` | Rendered per speaker, combined in audio-gen |
| PPT storyboard | `{level}/VIDEOS/L##_storyboard.pptx` | Input to video-gen |
| Lesson video | `{level}/VIDEOS/L##_video.mp4` | Grammar storyboard video |

Raw asset URL:
```
https://raw.githubusercontent.com/BTHKO/hko-esl-repo/main/{level}/IMAGES/L01_img1.png
```

---

## brein — Global Lesson Generation Rules

These rules apply to every lesson at every CEFR level and every topic domain.
They are not specific to any course, character set, or subject matter.
Level-specific content (characters, topics, vocabulary lists) lives in the level content file.

### Mandatory Pre-flight: Read Global Standards First

No generation begins without loading these four files in order:

```
Step 1 → _GLOBAL_STANDARDS_RULES/ESL_BUILDER_MASTERBRIEF_TEMPLATEANDRULE_STANDARDS.md
Step 2 → _GLOBAL_STANDARDS_RULES/TEMPLATE_1_Grammar_Presentation_Format.md
Step 3 → _GLOBAL_STANDARDS_RULES/TEMPLATE_2_Vocabulary_Glossary_Format.md
Step 4 → {level_folder}/{LEVEL}_COMPLETE_COURSE_12_LESSONS.md
```

Step 4 is where level-specific decisions live: topic domain, characters, vocabulary themes,
cultural context, register. Steps 1–3 are universal and override anything in Step 4.

### Level Folder Routing

| Level | Folder | Content File |
|-------|--------|-------------|
| A1 | `4.A1/` | `{LEVEL}_COMPLETE_COURSE_12_LESSONS.md` |
| A2 | `1.A2/` | `{LEVEL}_COMPLETE_COURSE_12_LESSONS.md` |
| B1 | `2. B1/` | `{LEVEL}_COMPLETE_COURSE_12_LESSONS.md` |
| C1 | `3. C1/` | `{LEVEL}_COMPLETE_COURSE_12_LESSONS.md` |

---

## Lesson Structure — 14 Stages (7 Vocab + 7 Grammar)

### Stage Overview

Each lesson is split into two equal halves. Each stage contains **2–3 activities**, not one.
Stage names are fixed — never expose Stage 1, Game 1, RACD, or any metalanguage to the learner.

#### Vocabulary Half (Stages 1–7)

| Stage | Name | Primary Mode | Min Activities | Learner Output |
|-------|------|-------------|----------------|----------------|
| S1 | Word Discovery in Context | Image-based activation | 2 | MCQ or short spoken/typed response |
| S2 | Guided Word Exploration | Matching / gamified | 2–3 | Matched pairs, sorted items |
| S3 | Vocabulary in Authentic Context | Input — read + listen | 2 | Minimal — annotation, highlight |
| S4 | Listening Comprehension | Audio + dialogue | 2–3 | MCQ, True/False, sequencing |
| S5 | Active Word Practice | Controlled production | 2–3 | Dropdown, gap-fill, categorise |
| S6 | Real-World Practice | Guided production | 2 | Reorder, sentence build, image-label |
| S7 | Lesson Wrap-Up & Review | **Free writing only** | 1 writing + 1 self-check | Written text 40–60 words |

#### Grammar Half (Stages 8–14)

| Stage | Name | Primary Mode | Min Activities | Learner Output |
|-------|------|-------------|----------------|----------------|
| S8 | Language in Natural Use | Discovery / noticing | 2 | MCQ, noticing task |
| S9 | Guided Language Exploration | Pattern recognition | 2–3 | Sorted, marked correct/incorrect |
| S10 | Language Rule in Context | Input — grammar box | 2 | Minimal — highlight, match form |
| S11 | Listening Comprehension | Audio + dialogue | 2–3 | MCQ, form-focused questions |
| S12 | Structured Language Practice | Controlled production | 2–3 | Dropdown, gap-fill, error correction |
| S13 | Real-World Practice | Guided production | 2 | Reorder, build sentence, image-label |
| S14 | Lesson Wrap-Up & Review | **Free writing + recap** | 1 writing + 1 recap + can-do | Written text 40–60 words |

---

## Activity Design Rules

### 2–3 Activities Per Stage — Not One

Every stage must contain a minimum of 2 activities. lesson-planner selects activity types
based on cognitive stage position. Activities within a stage escalate in difficulty:
activity 1 = lower support, activity 2/3 = less scaffolding.

### Activity Pool — Gamified and Standard, Always Mixed and Rotated

lesson-planner selects from this pool. No two consecutive stages use the same activity type.
Gamified and standard activities are always mixed within and across stages.

**Gamified activities (interactive, scored):**
- Drag-to-match (words → definitions, sentence halves, image regions → labels)
- Tile reorder (scrambled sentence → correct order)
- Swipe cards (correct / incorrect judgment)
- Word sort / categorise (drag into bins)
- Flashcard flip (tap to reveal)
- Timed gap-fill race
- Crossword / word search (for vocab reinforcement)
- Hot spot — click the correct region on an image
- Dialogue sequencer — drag conversation turns into correct order

**Standard activities (structured, reliable):**
- Multiple choice questions (MCQ) — 3 or 4 options
- True / False / Not mentioned
- Dropdown select in sentence
- Fill in the blank (typed)
- Error detection and correction
- Short answer (1–2 sentences)
- Table completion
- Note-taking from audio

**Rotation rule:** lesson-planner tracks activity types used and rotates — no type appears
more than twice in the vocabulary half, and no type appears more than twice in the grammar half.
visual-check flags violations and returns a `variety_fail` status to brein.

---

## Images — 3 to 5 Per Lesson

### Quantity Decision

lesson-planner assigns an image count (3–5) based on lesson content density.
visual-check independently scores lesson richness and can escalate the count:

| Condition | Action |
|-----------|--------|
| lesson-planner assigns 3 | Default — minimum acceptable |
| lesson-planner assigns 4–5 | Rich lesson with multiple contexts |
| visual-check scores density < 60% | Returns `sparse` flag → brein requests 1 additional image |
| visual-check scores density < 40% | Returns `very_sparse` flag → brein requests 2 additional images |

### Image Slots

| Slot | Name | Stage | Purpose |
|------|------|-------|---------|
| img1 | Opening / activation | S1 | Scene-setting, context activation — learner observes and responds |
| img2 | Vocabulary in context | S3 | Illustrates 2–4 vocabulary words in a real scene |
| img3 | Activity image | S5 or S6 | Used directly inside an activity — labels, hotspots, match regions |
| img4 | Grammar scene | S8 or S10 | Illustrates the target grammar structure in use |
| img5 | Production scaffold | S13 or S14 | Optional — visual prompt for writing or guided task |

### Images Inside Activities

Images are not just decoration. From S3 onwards, lesson-planner may embed an image
directly inside an activity as the stimulus. Examples:

- **Image label activity** — workplace scene with 6 numbered elements; learner drags vocabulary words to match numbered regions
- **Hot spot MCQ** — image shown, learner clicks the correct area in response to a question
- **Describe and match** — image shown; learner matches sentences to elements visible in the image
- **Dialogue scene** — image of two characters in conversation used as context for the dialogue activity
- **Grammar spot** — image contains a caption with target grammar; learner identifies correct/incorrect form

When an image is used inside an activity, it is assigned an activity-specific slot name
(e.g. `L##_act_S5_img.png`) in addition to its numbered slot, so assembler can reference it.

### Image Quality Rules (enforced by visual-check)

- 16:9 composition — confirmed
- No accidental text overlays
- Subject not clipped at edges
- Contrast adequate for activity use (labels must be readable over the image)
- Character visual consistency maintained across all images in a lesson
- `pass` / `warn` / `regenerate` flag returned per image
- Max 2 regeneration attempts per slot before brein marks asset as `manual_review`

---

## Dialogues — Mandatory in Every Lesson

Every lesson must contain at least one dialogue. Dialogues are not optional enrichment —
they are a core input type because:
- They model authentic spoken register
- They provide grammar in natural conversational use
- They enable listening discrimination tasks (who said what, turn-taking)
- They can be used for role-play production activities at higher levels

### Dialogue Rules

**Format:** Two speakers minimum. Three speakers permitted for group scenarios.
Each speaker line ≤ 12 words (A1–A2). Up to 20 words per line (B1–C1).

**Placement:**
- S4 (Listening Comprehension — vocab half) — primary dialogue placement
- S11 (Listening Comprehension — grammar half) — grammar-focused re-use of same or new dialogue
- S6 or S13 (Guided production) — dialogue sequencer activity using the S4 dialogue

**Dialogue types by level:**

| Level | Dialogue type | Typical scenario |
|-------|--------------|-----------------|
| A1 | Simple exchange, short turns | Greeting, introductions, yes/no questions |
| A2 | Information exchange, 2 speakers | Workplace task, short request, feedback |
| B1 | Extended exchange, 2–3 speakers | Interview, negotiation opening, problem-solving |
| B2–C1 | Complex multi-turn, nuanced register | Negotiation, conflict resolution, formal presentation Q&A |

**Audio rendering:**
Each speaker rendered separately via audio-gen (Deepgram TTS, different voice profiles).
Combined with 0.4s pause between turns into a single `L##_audio.mp3`.
Speaker-labelled raw files retained as `L##_spk_A.mp3`, `L##_spk_B.mp3` for activity use.

**Dialogue-based activity types** (at least one per lesson):
- Listen and identify speaker (who said X?)
- Sequence the dialogue turns (dialogue sequencer drag activity)
- Fill missing turn (gap in dialogue, learner selects or writes the response)
- Role play prompt (learner takes one speaker's role in S6/S13)

---

## Video Pipeline — Grammar Storyboard Videos

Every lesson produces one grammar explanation video.
This is the visual grammar narrative: contextual scenes → speech bubbles with target language → grammar table reveal.

### Video structure (per lesson)

```
Slide 1:  Title card — lesson title, grammar point, character/context
Slides 2–6: Scene slides — contextual situation illustrating grammar in use
           Each slide: background scene image + speech bubble(s) with target language highlighted
Slide 7:  "Did you notice?" — discovery sentences from S8, target forms highlighted
Slide 8:  Grammar table — FORM / USE / EXAMPLES (from grammar box)
Slide 9:  Examples with Spanish translations
Slide 10: Common mistake — ✗ wrong → ✓ correct
End card: Summary + link to lesson
```

### Pipeline

```
lesson-planner → generates slide scripts (text, image prompts per slide)
     ↓
image-gen → generates scene images for slides 2–6
     ↓
video-gen → builds PPTX storyboard from slide scripts + images
         → exports to MP4 via LibreOffice headless + ffmpeg
         → commits L##_storyboard.pptx + L##_video.mp4 to GitHub
     ↓
visual-check → QAs video thumbnail + slide density
```

### video-gen endpoints
```
POST /build-storyboard     Slide scripts + image URLs → .pptx → commit to GitHub
POST /export-video         .pptx path → .mp4 → commit to GitHub
GET  /status/:lessonId     Storyboard + video build status
```

### Video asset naming

| Asset | Path |
|-------|------|
| PPT storyboard | `{level}/VIDEOS/L##_storyboard.pptx` |
| Exported video | `{level}/VIDEOS/L##_video.mp4` |
| Slide images | `{level}/IMAGES/L##_slide_##.png` |

---

## Critical Design Rules — Global (All Levels, All Topics)

### Cognitive escalation — strict order within each half

Recognition → Recognition with meaning → Input study → Comprehension through listening →
Controlled production → Guided production → Free production / writing.
**Never invert this sequence.**

### Writing tasks — S7 and S14 only

S6 and S13 are guided production (reorder, image-label, dialogue fill) — not writing.
The final writing task at S7 and S14 always includes:
- Word target: **40–60 words** (A1–A2) / 80–120 words (B1+)
- Model sentence as scaffold (💡)
- Sentence frame
- Word bank drawn from lesson vocabulary only

### Every stage except S3 and S10 must produce a learner output

S3 and S10 are the only pure input stages (reading vocab cards, studying grammar box).
All other stages require the learner to complete something measurable.

### Instructions — always bilingual

English bold first → Spanish italic below (faded, smaller).
Applied to every instruction block across all 14 stages.

### Grammar box — S10 — table format only

- FORM: Subject | Affirmative (+) | Negative (−) | Question (?)
- USE: ≤ 20 words plain English + Spanish translation
- EXAMPLES: 3 sentences EN + Spanish below each
- COMMON MISTAKE: ✗ wrong form → ✓ correct form + rule explanation

### Word banks — mandatory in all production stages

Present in S5, S6, S7, S12, S13, S14. Visible on same screen as task — no scrolling.
A1–A2: always include Spanish translation beside each word.
B1+: English-only word banks unless otherwise specified in level content file.

### Vocabulary — no cognates

Test every word: would a Spanish speaker recognise the meaning from form similarity?
If yes, replace it. 8 words minimum per lesson. All words must appear in lesson context.

### Audio — sentence length by level

| Level | Max words per sentence | Total script length |
|-------|------------------------|---------------------|
| A1 | 8 words | 80–100 words |
| A2 | 12 words | 120–150 words |
| B1 | 18 words | 150–200 words |
| B2–C1 | No hard limit | 200–280 words |

### Can-do statements — Spanish, measurable

Uses "podrás". One statement per skill (Escuchar / Leer / Escribir / Identificar / Hablar).
Specific and achievable at the stated CEFR level. No metalanguage.

### Banned labels — never shown to learner

Stage 1/2/3, Game 1/2, RACD, Grammar Section, Vocabulary Unit, any metalanguage.
Always replaced with context-authentic names from the approved stage name list.

---

## visual-check — Expanded Responsibilities

visual-check is not only an image QA worker. It also evaluates overall lesson density
and flags lessons that are too sparse for the assembler to proceed.

### Image QA (per image)
- Composition: subject centred, no edge clipping
- Contrast: adequate for overlay use
- No accidental text overlay
- Character visual consistency (if applicable)
- Aspect ratio: 16:9 confirmed
- Returns: `pass` / `warn` / `regenerate`

### Lesson density check (per assembled lesson)
- Activity count per stage (flags if any stage has < 2 activities)
- Image count (flags if < 3 images)
- Dialogue presence (flags if no dialogue found)
- Video presence (flags if video not yet generated)
- Activity variety (flags if same type used > 2× in one half)
- Returns density score 0–100 and a list of specific flags

### Density flags and brein responses

| Flag | Threshold | brein action |
|------|-----------|-------------|
| `sparse` | density < 60% | Request 1 additional image from image-gen |
| `very_sparse` | density < 40% | Request 2 additional images + 1 extra activity per flagged stage |
| `no_dialogue` | dialogue missing | Return lesson to lesson-planner for dialogue insertion |
| `activity_variety_fail` | same type > 2× in half | Return to lesson-planner for activity rotation |
| `no_video` | video not generated | Trigger video-gen queue |
| `image_count_low` | < 3 images | Trigger image-gen for missing slots |

---

## lesson-planner — System Prompt (sent by brein on every job)

```
You are an expert ESL curriculum developer. Your output is used across multiple
proficiency levels, topic domains, and professional contexts.

BEFORE generating anything, fetch and read in this order:
1. _GLOBAL_STANDARDS_RULES/ESL_BUILDER_MASTERBRIEF_TEMPLATEANDRULE_STANDARDS.md
2. _GLOBAL_STANDARDS_RULES/TEMPLATE_1_Grammar_Presentation_Format.md
3. _GLOBAL_STANDARDS_RULES/TEMPLATE_2_Vocabulary_Glossary_Format.md
4. {level_folder}/{LEVEL}_COMPLETE_COURSE_12_LESSONS.md

The first three files are universal law. File 4 provides level-specific context:
topic domain, characters (if defined), vocabulary themes, cultural register.

MANDATORY RULES — enforced on every output:

CONTENT:
- NO COGNATES. Test every vocabulary word for L1 transparency. Replace any that fail.
- Every lesson must have at least one dialogue (minimum 2 speakers, minimum 6 turns).
- Vocabulary: 8 words minimum. All must appear in lesson contexts, not lists only.
- Audio sentences: respect per-level word limits (A2: ≤ 12 words/sentence).
- Characters, topic, and domain come from the level content file (Step 4). If not defined,
  lesson-planner generates them appropriate to level and context.

STRUCTURE:
- 14 stages: 7 vocab + 7 grammar. Stage names are fixed — no metalanguage.
- 2–3 activities per stage. Activities within a stage escalate in difficulty.
- Gamified and standard activities must be mixed. No activity type used more than
  twice in the vocabulary half, and more than twice in the grammar half.
- Writing tasks ONLY at S7 and S14. All other stages use interactive activities.
- Every stage except S3 and S10 must produce a measurable learner output.
- Cognitive escalation is non-negotiable: recognition → input → controlled
  production → guided production → free writing. Never inverted.

IMAGES:
- Assign 3–5 images. Default is 3 unless content richness warrants more.
- Specify which images are used inside activities (label, hotspot, dialogue scene).
- Provide a detailed Flux prompt for each image slot.
- Activity images must include specific use instructions for the assembler.

DIALOGUE:
- Minimum 1 dialogue per lesson. Placed primarily in S4.
- Provide full speaker-labelled script for audio-gen.
- Provide at least 1 dialogue-based activity (sequencer, fill-the-turn, role-play).

VIDEO:
- Provide slide scripts for the grammar storyboard video (10 slides).
- Slides 2–6: scene description + speech bubble text with grammar highlighted.
- Slide 7: discovery sentences from S8 with target forms marked.
- Slide 8: grammar table content.
- Slide 9: 3 examples with translations.
- Slide 10: common mistake pair.

INSTRUCTIONS: bilingual — English bold first, Spanish italic below.
WORD BANKS: all production stages. A1–A2: Spanish translations per word.
GRAMMAR BOX: table format — FORM / USE / EXAMPLES / COMMON MISTAKE.
CAN-DO STATEMENTS: Spanish, uses "podrás", specific and measurable.

OUTPUT: valid JSON matching the lesson plan schema. No markdown fences.
```

---

## Infrastructure

| Resource | Name | ID | Notes |
|----------|------|----|-------|
| D1 Database | hko-lesson-jobs | `61839119-4b7d-4c09-8b4a-7f74c132074e` | 4 tables: jobs, lessons, assets, grammar_vocab_cache |
| KV Namespace | PROMPT_HISTORY | See CF dashboard | Prompt cache — brein + lesson-planner |
| GitHub Repo | hko-esl-repo | github.com/BTHKO/hko-esl-repo | All generated assets + lesson HTML |
| GitHub Repo | HKO_ESL_GENERATOR | github.com/BTHKO/HKO_ESL_GENERATOR | Tauri app + worker source |
| Queue | lesson-planner-queue | See dashboard | brein → lesson-planner |
| Queue | image-gen-queue | See dashboard | brein → image-gen |
| Queue | audio-gen-queue | See dashboard | brein → audio-gen |
| Queue | assembler-queue | See dashboard | brein → assembler |
| Queue | visual-check-queue | See dashboard | image-gen → visual-check + post-assembly density check |
| Queue | video-gen-queue | See dashboard | brein → video-gen (after image-gen completes) |

### D1 Schema

```sql
jobs                  — job lifecycle (id, status, progress, params_json, result_json, error)
lessons               — generated lessons (id, level, lesson_number, title, block_json, status)
assets                — all assets (id, lesson_id, type, slot, github_path, status)
grammar_vocab_cache   — reusable LLM outputs (cache_key, level, grammar, data_json, expires_at)
```

### Bindings per Worker

| Worker | AI | D1 | KV | GitHub | Queue (producer) | Queue (consumer) |
|--------|----|----|-----|--------|------------------|------------------|
| brein | — | ✓ | ✓ | — | image-gen-q, audio-gen-q, assembler-q, video-gen-q | — |
| lesson-planner | ✓ Llama 3.3 | ✓ | ✓ | ✓ reads standards | — | lesson-planner-queue |
| image-gen | ✓ Flux | ✓ | — | ✓ writes | visual-check-queue | image-gen-queue |
| audio-gen | — | ✓ | — | ✓ writes | — | audio-gen-queue |
| assembler | — | ✓ | — | ✓ writes | visual-check-queue | assembler-queue |
| visual-check | ✓ LLaVA | ✓ | — | ✓ reads | — | visual-check-queue |
| video-gen | — | ✓ | — | ✓ writes | visual-check-queue | video-gen-queue |
| asset-manager | — | — | — | ✓ signed URLs | — | — |
| esl-ui | — | — | — | — | — | — |
| hko-oracle | — | ✓ | — | — | — | — |
| d1-template | — | ✓ | — | — | — | — |

---

## Job Lifecycle — Full Flow

```
1. Client POST /generate-lesson → brein creates job (pending)
   brein fetches _GLOBAL_STANDARDS_RULES + level content file from GitHub

2. brein → lesson-planner-queue
   lesson-planner reads standards (steps 1–4) → generates full plan including:
   - 14 stages with 2–3 activities each
   - Dialogue script with speaker labels
   - 3–5 image slot assignments + Flux prompts
   - Video slide scripts (10 slides)
   (status: planning)

3. brein → image-gen-queue
   image-gen generates 3–5 images (Flux) → commits to GitHub
   image-gen → visual-check-queue → visual-check QAs each image
   if regenerate flag → image-gen retries (max 2 attempts)
   (status: generating-assets)

4. brein → audio-gen-queue  [parallel with step 3]
   audio-gen renders each speaker separately → combines → commits L##_audio.mp3
   Speaker files retained: L##_spk_A.mp3, L##_spk_B.mp3
   (status: generating-assets)

5. brein → video-gen-queue  [starts after image-gen completes]
   video-gen builds PPTX storyboard from slide scripts + scene images
   → exports MP4 → commits L##_storyboard.pptx + L##_video.mp4
   video-gen → visual-check-queue → visual-check QAs thumbnail + density
   (status: generating-video)

6. brein → assembler-queue  [starts after steps 3–5 complete]
   assembler builds HTML using HKO_UNIFIED_LESSON_TEMPLATE_V2.html
   → commits L##_v2.html to GitHub
   assembler → visual-check-queue → visual-check runs full lesson density check
   if density flags returned → brein routes back to lesson-planner / image-gen as needed
   (status: assembling)

7. brein marks job completed
   resultUrls.lessonUrl = asset-manager signed URL

8. Client polls /status/:jobId → receives lessonUrl + lesson_plan
```

---

## API Quick Reference

### Generate lesson
```http
POST https://brein.mrhkruger.workers.dev/generate-lesson
X-API-Key: <BREIN_API_KEY>
Content-Type: application/json

{
  "level": "A2",
  "lessonNumber": 1,
  "topic": "Lesson topic title",
  "grammar": "Target grammar structure",
  "vocab": [],
  "context": "Optional domain/character context — if omitted lesson-planner decides"
}
```

### Poll status
```http
GET https://brein.mrhkruger.workers.dev/status/:jobId

Response:
{
  "jobId": "...",
  "status": "completed",
  "progress": 100,
  "resultUrls": {
    "lessonUrl": "https://raw.githubusercontent.com/BTHKO/hko-esl-repo/main/...",
    "videoUrl":  "https://raw.githubusercontent.com/BTHKO/hko-esl-repo/main/..."
  },
  "lesson_plan": { ... }
}
```

### Status labels

| Label | Meaning |
|-------|---------|
| `pending` | Job queued |
| `planning` | lesson-planner running |
| `generating-assets` | image-gen + audio-gen running in parallel |
| `generating-video` | video-gen building storyboard + MP4 |
| `visual-check` | QA pass running (images or lesson density) |
| `assembling` | assembler building HTML |
| `density-review` | visual-check flagged sparse lesson — enrichment in progress |
| `completed` | All assets on GitHub, lesson + video URL ready |
| `failed` | Error — see `job.error` |

### Health (no auth)
```http
GET https://brein.mrhkruger.workers.dev/health
```

---

## Secrets — Must Set Manually

```powershell
# brein
cd workers\brein
npx wrangler secret put BREIN_API_KEY

# HMAC signing — asset-manager AND audio-gen
cd workers\asset-manager ; npx wrangler secret put R2_SIGN_SECRET
cd workers\audio-gen     ; npx wrangler secret put R2_SIGN_SECRET

# GitHub Contents API (run in each folder):
# lesson-planner, image-gen, audio-gen, assembler, visual-check, video-gen, asset-manager
npx wrangler secret put GITHUB_TOKEN

# API guard (run in each folder):
# lesson-planner, image-gen, audio-gen, assembler, visual-check, video-gen, hko-oracle, d1-template
npx wrangler secret put API_SECRET
```

---

## Desktop App — First Launch

| Field | Value |
|-------|-------|
| Worker URL | `https://brein.mrhkruger.workers.dev` |
| API Key | Value you set for `BREIN_API_KEY` |
| Assets URL | `https://raw.githubusercontent.com/BTHKO/hko-esl-repo/main` |
| Poll Interval | `4` (seconds) |

Config saved to localStorage. App auto-syncs from `/config` on each launch.

---

## Re-running

```powershell
node hko-install.js           # skips resources that already exist
node hko-install.js --force   # force-redeploys all workers

cd workers\brein
npx wrangler deploy           # single worker deploy
```

### First-time D1 setup
```http
GET https://d1-template.mrhkruger.workers.dev/setup
X-API-Key: <API_SECRET>
```

### Seed demo lesson
```http
GET https://d1-template.mrhkruger.workers.dev/seed
X-API-Key: <API_SECRET>
```

---

## Tests

```powershell
node stress-test.js   # 392 tests — expected: 392 passed / 0 failed
```

---

## Install Session

Session log: `.hko-session-ocean-wren-3745.json`
Resources pre-existing at install time: none
Health score breakdown: 24/100 points (0.8× credit for pre-existing, 0 for failures)
