# HKO ESL Content Library

This folder contains all ESL lesson content organized by CEFR level.

## Structure

```
content-library/
  A1/
    lessons/      ← Lesson markdown files (lesson-01.md, lesson-02.md, ...)
    assessments/  ← Quiz and test files
  A2/
    lessons/
    assessments/
  B1/
    lessons/      ← HR English focus (Lesson 1–12 complete)
    assessments/
  B2/
    lessons/
    assessments/
  C1/
    lessons/      ← Advanced Business English
    assessments/
  C2/
    lessons/
    assessments/
  shared/
    templates/    ← Reusable block templates (grammar, vocab, etc.)
```

## Naming Convention

```
lesson-01-topic-name.md
assessment-01-vocabulary.md
template-grammar-present-simple.md
```

## File Format (lesson markdown)

```markdown
---
level: B1
lesson: 3
topic: Job Interviews
grammar: Past Simple for Experience
vocab: [candidate, qualification, reference]
---

# Lesson 3: Job Interviews

## Vocabulary
...

## Grammar Focus
...

## Activities
...
```

## How Content Gets Into the App

1. Files in this folder are **source content** — stored in GitHub
2. When a lesson is generated via the API, the AI creates lesson HTML
3. Generated lessons are stored in Cloudflare R2 (`hko-generated` bucket)
4. The local UI reads from both GitHub (templates) and R2 (generated)

## Uploading Bulk Content

To sync this folder to Cloudflare R2:
```powershell
node scripts/sync-content-to-r2.js
```
