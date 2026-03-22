# HTML5 MASTER LESSON TEMPLATE - EDITING GUIDE
## Complete Instructions for Customizing Your ESL Lessons

**Version:** 1.0 | **Date:** February 2026  
**Template File:** HTML5_MASTER_LESSON_TEMPLATE.html  
**Purpose:** Step-by-step guide to customize the master template for any A1-C2 lesson

---

## 📋 QUICK START CHECKLIST

Before you begin editing:
- [ ] Have your lesson plan ready (use TEMPLATE_5_Lesson_Plan)
- [ ] Have all images numbered and ready (IMG-L##-S##)
- [ ] Have grammar/vocabulary lists prepared
- [ ] Have audio files ready (if using)
- [ ] Know your CEFR level (A1/A2/B1/B2/C1/C2)
- [ ] Have Spanish translations ready (for A1-A2 levels)

---

## 🎯 SECTION 1: HEADER & META INFORMATION

### **Location:** Lines 7-12

**FIND:**
```html
<title>[LESSON TITLE] - CEFR [LEVEL] - HR English</title>
```

**REPLACE WITH:**
```html
<title>First Day at the Mining Site - CEFR A1 - HR English</title>
```

**FIND:**
```html
<h1>[LESSON TITLE - REPLACE WITH CONTEXT-AUTHENTIC NAME]</h1>
<div class="lesson-meta">
    <strong>CEFR Level:</strong> [A1/A2/B1/B2/C1/C2] |
    <strong>Module:</strong> [1-5] |
    <strong>Lesson:</strong> [01-15] |
    <strong>Context:</strong> [HR Professional Scenario]
</div>
```

**REPLACE WITH:**
```html
<h1>First Day at the Mining Site</h1>
<div class="lesson-meta">
    <strong>CEFR Level:</strong> A1 |
    <strong>Module:</strong> 1 |
    <strong>Lesson:</strong> 01 |
    <strong>Context:</strong> Introducing yourself to new team members
</div>
```

**CRITICAL RULE:** NO META-LANGUAGE in titles!  
❌ Bad: "Vocabulary Lab: Job Titles"  
✅ Good: "Meeting Your New Team"

---

## 🖼️ SECTION 2: REPLACING IMAGE PLACEHOLDERS

### **Every stage has images. Look for:**

```html
<div class="image-placeholder">
    📸 IMG-L##-S01-VOC<br>
    [INSERT IMAGE: HR professional context showing target vocabulary in use]<br>
    <em>Replace this placeholder with actual image...</em>
</div>
```

### **REPLACE WITH:**

```html
<img src="images/lesson01-stage01-vocab.jpg" alt="HR recruiter greeting candidates in office lobby">
```

### **Image Naming Convention:**

```
lesson[NN]-stage[NN]-[vocab/grammar].jpg

Examples:
lesson01-stage01-vocab.jpg
lesson01-stage08-grammar.jpg
lesson02-stage04-vocab.jpg
```

### **Alt Text Requirements:**
- Describe what's in the image
- Include HR context
- Keep under 125 characters
- Help visually impaired users understand content

**Good alt text examples:**
- "HR manager reviewing resumes at desk with laptop"
- "Two professionals shaking hands during interview"
- "Team meeting with diverse HR staff around conference table"

---

## 📝 SECTION 3: CUSTOMIZING QUESTIONS & PROMPTS

### **Stage 1 & 8: Observation Questions**

**FIND:**
```html
<div class="questions">
    <h3>❓ Observation Questions</h3>
    <ul>
        <li>[Question 1: What's happening in this scene?]</li>
        <li>[Question 2: What do you notice about specific elements?]</li>
        <li>[Question 3: Have you experienced something similar?]</li>
    </ul>
    <div class="spanish-translation">
        [A1-A2] Spanish translations:<br>
        • [Pregunta 1 en español]<br>
        • [Pregunta 2 en español]<br>
        • [Pregunta 3 en español]
    </div>
</div>
```

**REPLACE WITH:**
```html
<div class="questions">
    <h3>❓ Observation Questions</h3>
    <ul>
        <li>What's happening in this office scene?</li>
        <li>What do you notice about how people are greeting each other?</li>
        <li>Have you been in a similar situation at work?</li>
    </ul>
    <div class="spanish-translation">
        [A1-A2] Traducción al español:<br>
        • ¿Qué está pasando en esta escena de oficina?<br>
        • ¿Qué notas sobre cómo se saludan las personas?<br>
        • ¿Has estado en una situación similar en el trabajo?
    </div>
</div>
```

**Spanish Translation Guidelines:**
- **A1-A2:** ALWAYS include Spanish translations for ALL instructions, questions, and key content
- **B1-B2:** Include Spanish for key terms and complex instructions only
- **C1-C2:** English only (no Spanish needed)

---

## 📚 SECTION 4: VOCABULARY REFERENCE BOX (Stage 3)

**FIND:**
```html
<div class="reference-box">
    <h3>📖 Word Window</h3>
    <div class="item">
        <div class="term">[Word 1]</div>
        <div class="definition">[Clear definition in context]</div>
        <div class="example">Example: "[HR context sentence]"</div>
        <div class="spanish-translation">[A1-A2] ES: [Spanish translation]</div>
    </div>
```

**REPLACE WITH:**
```html
<div class="reference-box">
    <h3>📖 Word Window</h3>
    <div class="item">
        <div class="term">greet</div>
        <div class="definition">To say hello to someone in a friendly way</div>
        <div class="example">Example: "I greet my colleagues every morning with a smile."</div>
        <div class="spanish-translation">[A1-A2] ES: saludar</div>
    </div>
    <div class="item">
        <div class="term">introduce</div>
        <div class="definition">To tell someone your name or give information about yourself</div>
        <div class="example">Example: "Let me introduce myself - I'm the new HR coordinator."</div>
        <div class="spanish-translation">[A1-A2] ES: presentar(se)</div>
    </div>
    <!-- Add 6-10 more vocabulary items -->
</div>
```

**HOW MANY WORDS?**
- Minimum: 8 words
- Maximum: 12 words
- NO COGNATES (test: "Would a Spanish speaker already guess this?")

**Forbidden cognates examples:**
- ❌ doctor, hospital, telephone, important, familia, información
- ✅ Instead teach: physician, clinic, call/phone, crucial, relatives, details

---

## 🎮 SECTION 5: MATCHING GAME (Stage 2 & 9)

**FIND:**
```html
<div class="matching-game" id="matching-game-1">
    <div class="matching-column">
        <h4>Words</h4>
        <div class="match-item" data-match="1" onclick="selectMatch(this, 1)">[Word 1]</div>
        <div class="match-item" data-match="2" onclick="selectMatch(this, 1)">[Word 2]</div>
```

**REPLACE WITH:**
```html
<div class="matching-game" id="matching-game-1">
    <div class="matching-column">
        <h4>Words</h4>
        <div class="match-item" data-match="1" onclick="selectMatch(this, 1)">greet</div>
        <div class="match-item" data-match="2" onclick="selectMatch(this, 1)">introduce</div>
        <div class="match-item" data-match="3" onclick="selectMatch(this, 1)">colleague</div>
        <div class="match-item" data-match="4" onclick="selectMatch(this, 1)">position</div>
        <div class="match-item" data-match="5" onclick="selectMatch(this, 1)">department</div>
    </div>
    <div class="matching-column">
        <h4>Meanings</h4>
        <div class="match-item" data-match="3" onclick="selectMatch(this, 1)">Person you work with</div>
        <div class="match-item" data-match="1" onclick="selectMatch(this, 1)">Say hello to someone</div>
        <div class="match-item" data-match="5" onclick="selectMatch(this, 1)">Section of a company</div>
        <div class="match-item" data-match="2" onclick="selectMatch(this, 1)">Tell your name and information</div>
        <div class="match-item" data-match="4" onclick="selectMatch(this, 1)">Your job title or role</div>
    </div>
</div>
```

**CRITICAL:** The `data-match` numbers MUST correspond between columns!
- Word with data-match="1" pairs with Meaning with data-match="1"
- Mix up the ORDER in the right column so it's not too easy

---

## 🎯 SECTION 6: DRAG & DROP SENTENCE BUILDING (Stage 2 & 9)

**FIND:**
```html
<div class="word-bank" id="word-bank-1">
    <div class="draggable-word" draggable="true">[Word1]</div>
    <div class="draggable-word" draggable="true">[Word2]</div>
```

**REPLACE WITH:**
```html
<div class="word-bank" id="word-bank-1">
    <div class="draggable-word" draggable="true">My</div>
    <div class="draggable-word" draggable="true">name</div>
    <div class="draggable-word" draggable="true">is</div>
    <div class="draggable-word" draggable="true">Carlos</div>
    <div class="draggable-word" draggable="true">.</div>
</div>
```

**AND UPDATE THE CHECK BUTTON:**

**FIND:**
```html
<button class="btn-primary" onclick="checkSentence(1, '[Correct sentence]')">Check Answer</button>
```

**REPLACE WITH:**
```html
<button class="btn-primary" onclick="checkSentence(1, 'My name is Carlos .')">Check Answer</button>
```

**IMPORTANT:** The correct sentence in `checkSentence()` must EXACTLY match the order of words when correctly placed, including spaces and punctuation!

---

## 📖 SECTION 7: READING/LISTENING PASSAGES (Stage 4 & 11)

### **For LISTENING Lessons (Odd-numbered lessons: 1, 3, 5, 7, 9, 11, 13, 15)**

**FIND:**
```html
<button class="audio-button" onclick="playAudio('audio-stage4')">Play Audio</button>
<audio id="audio-stage4" src="[path/to/audio.mp3]"></audio>

<h4 style="margin-top: 20px;">Transcript:</h4>
<p style="line-height: 2; padding: 15px; background: var(--bg-light); border-radius: 5px;">
    [Audio transcript with <strong>target vocabulary</strong> in bold]
</p>
```

**REPLACE WITH:**
```html
<button class="audio-button" onclick="playAudio('audio-stage4')">Play Audio</button>
<audio id="audio-stage4" src="audio/lesson01-stage04.mp3"></audio>

<h4 style="margin-top: 20px;">Transcript:</h4>
<p style="line-height: 2; padding: 15px; background: var(--bg-light); border-radius: 5px;">
    Hello, my name is Maria and I'm the new HR <strong>coordinator</strong> for this mining site. 
    I'm here to <strong>introduce</strong> myself to the team. I'll be working in the 
    <strong>recruitment</strong> department. Nice to <strong>greet</strong> all of you today!
</p>
<div class="spanish-translation">
    [A1-A2] Traducción: Hola, mi nombre es María y soy la nueva coordinadora de RRHH 
    para este sitio minero. Estoy aquí para presentarme al equipo. Trabajaré en el 
    departamento de reclutamiento. ¡Un gusto saludarlos a todos hoy!
</div>
```

### **For READING Lessons (Even-numbered lessons: 2, 4, 6, 8, 10, 12, 14)**

**Simply comment out the audio section and uncomment the reading section**

---

## ❓ SECTION 8: MULTIPLE CHOICE QUESTIONS

**FIND:**
```html
<div class="question-container">
    <div class="question-text">1. Which word in the text means "[definition]"?</div>
    <div class="options">
        <div class="option" onclick="selectOption(this, false)">A) [Option 1]</div>
        <div class="option" onclick="selectOption(this, true)">B) [Correct Option]</div>
        <div class="option" onclick="selectOption(this, false)">C) [Option 3]</div>
        <div class="option" onclick="selectOption(this, false)">D) [Option 4]</div>
    </div>
    <div class="feedback-box" id="feedback-q1"></div>
</div>
```

**REPLACE WITH:**
```html
<div class="question-container">
    <div class="question-text">1. Which word means "to say hello to someone"?</div>
    <div class="options">
        <div class="option" onclick="selectOption(this, false)">A) introduce</div>
        <div class="option" onclick="selectOption(this, true)">B) greet</div>
        <div class="option" onclick="selectOption(this, false)">C) colleague</div>
        <div class="option" onclick="selectOption(this, false)">D) position</div>
    </div>
    <div class="feedback-box" id="feedback-q1"></div>
</div>
```

**CRITICAL:** Only ONE option should have `onclick="selectOption(this, true)"` - that's the correct answer!

---

## 💼 SECTION 9: RACD PROFESSIONAL TASK (Stage 6 & 13)

**FIND:**
```html
<div class="racd-framework">
    <h3>📝 Professional Writing Task (RACD Framework)</h3>
    <div class="racd-item">
        <span class="racd-label">R (Role):</span>
        [Your role, e.g., "HR Recruiter"]
    </div>
```

**REPLACE WITH:**
```html
<div class="racd-framework">
    <h3>📝 Professional Writing Task (RACD Framework)</h3>
    <div class="racd-item">
        <span class="racd-label">R (Role):</span>
        You are a new HR coordinator at a mining company
    </div>
    <div class="racd-item">
        <span class="racd-label">A (Audience):</span>
        Your new team members (5 people in the recruitment department)
    </div>
    <div class="racd-item">
        <span class="racd-label">C (Context):</span>
        It's your first day and you need to introduce yourself via email
    </div>
    <div class="racd-item">
        <span class="racd-label">D (Deliverable):</span>
        Write an introduction email (75-100 words) using at least 5 target vocabulary words
    </div>
```

**RACD Task Design Tips:**
- Keep it REALISTIC to HR work
- Make it SPECIFIC (not vague)
- Word count should match CEFR level:
  - A1: 50-75 words
  - A2: 75-125 words
  - B1: 125-175 words
  - B2: 175-250 words
  - C1: 250-350 words
  - C2: 350+ words

---

## 🏆 SECTION 10: SCORECARD & BADGES (Stage 7 & 14)

### **Auto-Calculated Scores (JavaScript handles this)**

The template automatically tracks:
- Game completion
- Answer accuracy
- Time spent
- Task submission

### **Badges - Configure When They're Earned**

**In the JavaScript section (bottom of file), find:**

```javascript
// Check if all matched
function checkAllMatched(gameNum) {
    // ... existing code ...
    if (items.length === correct.length) {
        showConfetti();
        playSound('victory');
        
        // ADD BADGE EARNING LOGIC HERE
        document.getElementById('badge-accuracy-champion').classList.add('earned');
    }
}
```

**Badge IDs to customize:**
- `badge-vocab-navigator`
- `badge-accuracy-champion`
- `badge-professional-communicator`
- `badge-structure-master` (for grammar stages)
- `badge-form-perfectionist` (for grammar stages)

---

## 🎨 SECTION 11: CUSTOMIZING COLORS & BRANDING

### **Location:** Lines 14-23 (CSS Variables)

**To change brand colors:**

```css
:root {
    --primary: #d2691e;      /* Main orange - change to your brand color */
    --secondary: #4a4a4a;    /* Dark gray - change to your secondary */
    --accent: #8b4513;       /* Brown accent - change to your accent */
    --success: #4caf50;      /* Keep green for success */
    --error: #f44336;        /* Keep red for errors */
}
```

**Example for different branding:**

```css
:root {
    --primary: #1976D2;      /* Blue for tech company */
    --secondary: #424242;    /* Charcoal gray */
    --accent: #FFC107;       /* Gold accent */
    --success: #4caf50;      /* Keep green */
    --error: #f44336;        /* Keep red */
}
```

---

## 📱 SECTION 12: MOBILE RESPONSIVENESS

**The template is already mobile-responsive, but test on:**
- Desktop (1920x1080)
- Laptop (1366x768)
- Tablet (768x1024)
- Phone (375x667)

**Key responsive features already included:**
- Flexible grid layouts
- Stackable columns on mobile
- Touch-friendly buttons (min 44px)
- Readable fonts (min 14px on mobile)

---

## 🔊 SECTION 13: AUDIO SETUP

### **Option 1: Upload Audio Files**

1. Record audio (native speaker, clear pronunciation)
2. Save as MP3 format
3. Place in `/audio/` folder
4. Reference in HTML:

```html
<audio id="audio-stage4" src="audio/lesson01-stage04.mp3"></audio>
```

### **Option 2: Use Web Speech API (Built-in)**

If no audio file, the template automatically uses browser text-to-speech:

```javascript
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9; // Adjust speed (0.5 = slow, 1.5 = fast)
        speechSynthesis.speak(utterance);
    }
}
```

**No additional setup needed!**

---

## 💾 SECTION 14: SAVE & DOWNLOAD FUNCTIONS

### **Auto-Save Feature (Already Configured)**

The template automatically saves student progress every 30 seconds to browser localStorage.

**What's saved:**
- Current stage
- Completed stages
- Scores
- Answers to all questions
- Production task drafts

### **Download Materials**

**FIND:**
```javascript
function downloadMaterial(type) {
    alert('📥 Downloading ' + type + '...\n\nIn production, this would trigger a PDF download.');
    // In production: window.location.href = '/downloads/' + type + '.pdf';
}
```

**REPLACE WITH:**
```javascript
function downloadMaterial(type) {
    const files = {
        'vocab-list': '/downloads/lesson01-vocab-list.pdf',
        'audio-script': '/downloads/lesson01-audio-script.pdf',
        'exercises': '/downloads/lesson01-exercises.pdf',
        'flashcards': '/downloads/lesson01-flashcards.apkg'
    };
    
    if (files[type]) {
        window.location.href = files[type];
    }
}
```

---

## ✅ FINAL TESTING CHECKLIST

Before publishing your lesson, test:

### **Functionality:**
- [ ] All 14 stages load correctly
- [ ] Navigation buttons work
- [ ] Matching game works (try incorrect matches too!)
- [ ] Drag-and-drop works on both desktop and mobile
- [ ] Multiple choice questions give correct feedback
- [ ] Audio plays (or TTS works)
- [ ] Progress bar updates
- [ ] Scores calculate correctly
- [ ] Save/load works (refresh page and check)
- [ ] Download buttons trigger downloads

### **Content:**
- [ ] No placeholder text (all [BRACKETS] replaced)
- [ ] All images load properly
- [ ] Alt text present on all images
- [ ] Spanish translations complete (A1-A2)
- [ ] NO COGNATES in vocabulary
- [ ] All HR contexts authentic and realistic
- [ ] Grammar structures match CEFR level
- [ ] Word count appropriate for level

### **Design:**
- [ ] Works on mobile (test on phone)
- [ ] Print version readable
- [ ] Colors match brand guidelines
- [ ] All text readable (contrast check)
- [ ] Buttons big enough to tap
- [ ] No horizontal scrolling

---

## 🚀 DEPLOYMENT STEPS

1. **Save your edited HTML file**
   - Name it: `lesson-[NN]-[descriptive-name].html`
   - Example: `lesson-01-first-day-mining-site.html`

2. **Upload to your LMS (Moodle)**
   - Go to your course
   - Turn editing on
   - Add activity → File
   - Upload your HTML file
   - Settings: Display "In pop-up" or "New window"

3. **Test in LMS**
   - Open as student
   - Complete one full stage
   - Refresh page (check auto-save works)
   - Submit a production task
   - Download materials

4. **Monitor Analytics**
   - Track completion rates
   - Note where students get stuck
   - Review submitted tasks
   - Adjust difficulty if needed

---

## 🆘 TROUBLESHOOTING

### **Problem:** Matching game not working

**Solution:** Check that `data-match` numbers correspond between columns

---

### **Problem:** Audio not playing

**Solution:** 
1. Check file path is correct
2. Check file format is MP3
3. Try Web Speech API fallback instead

---

### **Problem:** Progress not saving

**Solution:**
1. Check browser allows localStorage
2. Test in incognito mode (may block localStorage)
3. Check JavaScript console for errors

---

### **Problem:** Styles look broken

**Solution:**
1. Check you didn't accidentally delete CSS closing braces `}`
2. Validate HTML at validator.w3.org
3. Check browser developer console

---

## 📚 ADDITIONAL RESOURCES

**Recommended Tools:**
- **Image Editor:** Canva, Photoshop, GIMP
- **Audio Recording:** Audacity (free), Adobe Audition
- **HTML Editor:** VS Code, Sublime Text, Notepad++
- **Testing:** BrowserStack for cross-browser testing

**Useful Websites:**
- **CEFR Descriptors:** coe.int/en/web/common-european-framework-reference-languages
- **IPA Pronunciation:** tophonetics.com
- **Color Contrast Checker:** webaim.org/resources/contrastchecker
- **HTML Validator:** validator.w3.org

---

## 💡 PRO TIPS

1. **Start Small:** Edit one stage at a time, test, then move to next
2. **Duplicate & Modify:** Copy-paste stages for consistency
3. **Version Control:** Save versions (lesson01-v1.html, lesson01-v2.html)
4. **Student Feedback:** After first students complete, ask what was confusing
5. **Iterate:** No lesson is perfect first time - improve based on data

---

**END EDITING GUIDE**

Good luck creating amazing ESL lessons! 🚀

