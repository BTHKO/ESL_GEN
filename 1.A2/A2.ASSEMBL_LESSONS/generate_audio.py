"""
HKO A2 Audio Generator - ElevenLabs Direct API
Generates all story + pronunciation audio for 12 lessons
Run: python generate_audio.py
Output: ./audio/ folder with all MP3 files
"""

import os, json, requests, time

# ── CONFIG ── paste your key here ──────────────────────────────
ELEVEN_API_KEY = "YOUR_ELEVENLABS_API_KEY_HERE"
# ───────────────────────────────────────────────────────────────

BASE_URL = "https://api.elevenlabs.io/v1"
OUT_DIR  = "audio"
os.makedirs(OUT_DIR, exist_ok=True)

# Voice profiles (ElevenLabs voice IDs - update if needed)
VOICES = {
    "maria":    {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella",   "stability": 0.55, "similarity": 0.75, "style": 0.20, "speed": 0.88},
    "carlos":   {"id": "pNInz6obpgDQGcFmaJgB", "name": "Adam",    "stability": 0.60, "similarity": 0.72, "style": 0.15, "speed": 0.88},
    "patricia": {"id": "ThT5KcBeYPX3keUQqHPh", "name": "Dorothy", "stability": 0.58, "similarity": 0.74, "style": 0.18, "speed": 0.88},
}

# All 12 lesson audio scripts (from A2_ASSET_LIST)
LESSONS = {
    "L01": {
        "voice": "maria",
        "filename": "GEN_A2_L01_AUD_STORY_V1.mp3",
        "script": """My name is María. I work in HR. I started five years ago.
I studied psychology at university. I finished in 2018. I wanted to work with people. I applied for many jobs. I got an interview at MineSafe.
The interview went well. They called me the next day. I started as an HR assistant. My tasks were simple. I scheduled interviews. I answered employee questions. I filed documents.
Two years later, I moved to the recruitment team. I learned a lot. I interviewed many candidates. I liked this work very much.
Last year, I changed roles again. I became an HR Coordinator. I now manage a small team. I love my job. I am happy with my career."""
    },
    "L02": {
        "voice": "carlos",
        "filename": "GEN_A2_L02_AUD_STORY_V1.mp3",
        "script": """Last month I had a difficult week. My name is Carlos. I work in recruitment.
On Monday I posted a new job. I expected about 30 applications. By Tuesday I received 150. I didn't expect so many.
I started reading CVs on Wednesday. Many candidates didn't have the right skills. About 100 didn't meet our needs. I didn't call them.
On Thursday I sent 15 invitations. Five candidates didn't reply. I waited two days. They didn't answer my emails.
On Friday I set up the interviews. But two candidates didn't come. They didn't call. They didn't email. I was sad.
I didn't hire anyone that week. The process took three more weeks. This is normal in our work."""
    },
    "L03": {
        "voice": "patricia",
        "filename": "GEN_A2_L03_AUD_STORY_V1.mp3",
        "script": """Good morning. My name is Patricia. I am going to share our results.
Last month we received 150 applications. We had three open positions. My team read all 150 CVs. We finished in four days.
We selected 30 candidates. They met our needs. We sent them an online test. 25 candidates completed the test. Five candidates scored too low. We didn't move them forward.
We invited 15 candidates to a first interview. We interviewed all 15. Then we selected six for a second interview.
In the end, we hired three people. One for each open role. All three said yes to our offer. This was a very good month for our team."""
    },
    "L04": {
        "voice": "carlos",
        "filename": "GEN_A2_L04_AUD_STORY_V1.mp3",
        "script": """I had an important interview last year. My name is Carlos. I want to tell you about it.
I saw the job online. I felt excited right away. I went to their website. I read about the company. I applied the same day.
Two weeks later they called me. They invited me to an interview. I went on a Tuesday morning. The interview took one hour.
The manager asked good questions. I gave clear answers. I used examples from my past work. She showed me the office at the end.
Three days later they called again. I went to a second interview. At the end the manager said I got the job. I was very happy. I started the next Monday."""
    },
    "L05": {
        "voice": "maria",
        "filename": "GEN_A2_L05_AUD_STORY_V1.mp3",
        "script": """Hi, I'm María. I have a lot of work this week. I'm going to tell you my plan.
Today is Monday. I'm going to review 50 CVs. I'm going to make a short list by noon. Then I'm going to send emails to the best candidates.
Tomorrow I'm going to call five people. I'm going to ask about their work history. I'm going to take notes during each call.
On Wednesday I'm going to set up the interviews. I'm going to book the meeting rooms. I'm going to send the interview times by email.
On Thursday and Friday I'm going to run the interviews. I'm going to write my notes after each one. It's a busy week. But I have a clear plan."""
    },
    "L06": {
        "voice": "patricia",
        "filename": "GEN_A2_L06_AUD_STORY_V1.mp3",
        "script": """Hi Patricia. It's María. I'm calling about the new role.
Hi María. Yes, I have some questions.
I'll answer them now. I'll send you the job description today. You'll have it before lunch.
Great. Will you include the salary range?
Yes, I'll add it to the document. I'll also send you the team structure.
What about the interview process?
I'll explain everything by email. I'll set up a call for next week. We'll talk through all the details.
Perfect. One more thing. When will you post the role?
I'll post it on Friday. I'll send you the link right away.
Thank you, María.
No problem. Talk soon."""
    },
    "L07": {
        "voice": "carlos",
        "filename": "GEN_A2_L07_AUD_STORY_V1.mp3",
        "script": """Hi Carlos. I have some questions about our process.
Of course. What do you want to know?
Will you post the job this week?
Yes. I'll post it on Monday. About 80 people will apply.
How long will the review take?
It will take about three days. Then I'll make a short list.
Will you do phone calls first?
Yes. I'll call the best candidates. Each call will take 20 minutes.
How many people will you interview?
I'll interview ten people. The interviews will happen next week.
When will we make a decision?
We'll decide by the end of the month. I'll send you an update every week.
Thank you, Carlos."""
    },
    "L08": {
        "voice": "patricia",
        "filename": "GEN_A2_L08_AUD_STORY_V1.mp3",
        "script": """Hello. My name is Patricia. I need to choose between two candidates.
The first candidate is Ana. She has five years of work experience. She speaks two languages. Her interview score was 85 out of 100.
The second candidate is Luis. He has three years of work experience. He speaks one language. His interview score was 78 out of 100.
Ana is more experienced than Luis. She is also a better communicator. Her score is higher than his score.
Luis is younger than Ana. He is also less expensive for the company. But his score is lower than Ana's.
The role needs strong communication skills. It also needs experience. Ana is a better match for this role. I'm going to recommend Ana to the manager."""
    },
    "L09": {
        "voice": "maria",
        "filename": "GEN_A2_L09_AUD_STORY_V1.mp3",
        "script": """Good afternoon. My name is María. I am going to present our final candidate.
We interviewed six people for this role. All six were strong candidates. But one stood out from the rest.
Her name is Sofia. She has the most experience on our list. She worked in HR for eight years. She is also the most qualified candidate. She has two HR certifications.
Her interview was the best of the six. She gave the clearest answers. She prepared the most carefully. She asked the most relevant questions at the end.
Her test score was the highest. She scored 94 out of 100. No other candidate scored above 85.
I recommend Sofia for this role. She is the strongest candidate we have seen this year. I am confident she is the right choice."""
    },
    "L10": {
        "voice": "carlos",
        "filename": "GEN_A2_L10_AUD_STORY_V1.mp3",
        "script": """Hi Carlos. I have some good news about our team.
Tell me!
Our process is faster now. We used to take four weeks. Now we take two weeks.
That's great. How did we do it?
We review CVs more quickly now. We also schedule interviews more efficiently.
What else is better?
We respond to candidates more promptly now. Before, we waited five days. Now we reply in two days.
And the quality?
Our new hires are performing more strongly than before. The last group adapted most quickly to the team.
This is the best result we've had in three years.
I agree. The team worked very hard to improve."""
    },
    "L11": {
        "voice": "maria",
        "filename": "GEN_A2_L11_AUD_STORY_V1.mp3",
        "script": """Hi! I'm María. Welcome to the team.
Thank you. I'm David. I just started today.
Have you worked in HR before?
Yes, I have. I've worked in HR for four years.
Have you used our software system?
No, I haven't. It's new to me. But I've used similar tools.
Have you met the team yet?
I've met two people so far. Carlos and Patricia. They seem very friendly.
Have you had lunch yet?
No, I haven't. I've been in meetings all morning.
Let's go together. I'll introduce you to more people.
That sounds great. Thank you, María."""
    },
    "L12": {
        "voice": "carlos",
        "filename": "GEN_A2_L12_AUD_STORY_V1.mp3",
        "script": """Hi everyone. I'm Carlos. I have some updates from this week.
It has been a busy week for recruitment. I'm happy to share the results.
We've just hired three new people. They start next Monday. I've already sent them their contracts. They've already signed and returned them.
I've also just posted two more jobs. One is for an HR Assistant. The other is for a Recruiter. I've already written the job descriptions. I've already shared them with the managers.
Have you reviewed the new hire profiles yet? I've sent them to the whole team. Please read them before Monday.
I haven't scheduled the welcome meeting yet. I'll do that today. I'll send the calendar invite this afternoon.
It's been a great week. Well done to the team!"""
    },
}

def generate_audio(text, voice_key, filename):
    voice = VOICES[voice_key]
    url = f"{BASE_URL}/text-to-speech/{voice['id']}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability":        voice["stability"],
            "similarity_boost": voice["similarity"],
            "style":            voice["style"],
            "use_speaker_boost": True
        }
    }
    # Add speed if supported
    try:
        payload["voice_settings"]["speed"] = voice["speed"]
    except:
        pass

    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path):
        print(f"  SKIP (exists): {filename}")
        return True

    print(f"  Generating: {filename} [{voice_key}]...")
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    if r.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(r.content)
        size = len(r.content) // 1024
        print(f"  OK: {filename} ({size}KB)")
        return True
    else:
        print(f"  ERROR {r.status_code}: {r.text[:200]}")
        return False

def check_api_key():
    if ELEVEN_API_KEY == "YOUR_ELEVENLABS_API_KEY_HERE":
        print("ERROR: Set your ElevenLabs API key in the script (ELEVEN_API_KEY variable)")
        return False
    r = requests.get(f"{BASE_URL}/user", headers={"xi-api-key": ELEVEN_API_KEY})
    if r.status_code == 200:
        data = r.json()
        chars = data.get("subscription", {}).get("character_count", 0)
        limit = data.get("subscription", {}).get("character_limit", 0)
        print(f"ElevenLabs OK — Characters used: {chars}/{limit}")
        return True
    else:
        print(f"ElevenLabs AUTH FAILED: {r.status_code} — check your API key")
        return False

def list_voices():
    """Helper to see available voices on your account"""
    r = requests.get(f"{BASE_URL}/voices", headers={"xi-api-key": ELEVEN_API_KEY})
    if r.status_code == 200:
        for v in r.json().get("voices", [])[:15]:
            print(f"  {v['name']:30} id={v['voice_id']}")

if __name__ == "__main__":
    print("=" * 60)
    print("HKO A2 Audio Generator")
    print("=" * 60)

    if not check_api_key():
        print("\nAvailable voices on your account:")
        list_voices()
        exit(1)

    print("\nAvailable voices on your account:")
    list_voices()

    print(f"\nGenerating {len(LESSONS)} lesson audio files...")
    ok = 0
    fail = 0
    for lesson_id, data in LESSONS.items():
        print(f"\n[{lesson_id}]")
        success = generate_audio(data["script"], data["voice"], data["filename"])
        if success:
            ok += 1
        else:
            fail += 1
        time.sleep(1)  # Rate limit safety

    print(f"\n{'='*60}")
    print(f"DONE: {ok} generated, {fail} failed")
    print(f"Audio files saved to: ./{OUT_DIR}/")
    print(f"\nNext step: run build_scorm.py to package lessons")
