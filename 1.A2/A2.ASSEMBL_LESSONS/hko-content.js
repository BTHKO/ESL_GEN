// hko-content.js
// Deploy: npx wrangler deploy hko-content.js --name hko-content --compatibility-date 2025-01-01
// Bindings needed: Workers AI (name: AI), KV (name: KV, id: e51e71b8efc34ecc8be226593c2afbc4)

const LESSONS = {
  1:  { title: "I Started in HR Five Years Ago",         grammar: "Past Simple — Regular Verbs",          voice: "maria",    num: "01" },
  2:  { title: "I Didn't Expect So Many Applications",   grammar: "Past Simple — Negative Forms",         voice: "carlos",   num: "02" },
  3:  { title: "We Received 50 Applications",            grammar: "Past Simple + Quantities",             voice: "patricia", num: "03" },
  4:  { title: "The Interview Went Well",                grammar: "Past Simple — Irregular Verbs",        voice: "carlos",   num: "04" },
  5:  { title: "I'm Going to Review the CVs Tomorrow",   grammar: "Future with Going To",                 voice: "maria",    num: "05" },
  6:  { title: "I'll Send You the Job Description",      grammar: "Future with Will",                     voice: "patricia", num: "06" },
  7:  { title: "What Will Happen Next?",                 grammar: "Future Questions — Will",              voice: "carlos",   num: "07" },
  8:  { title: "This Candidate Is Better Than That One", grammar: "Comparatives",                         voice: "patricia", num: "08" },
  9:  { title: "She's the Most Qualified Candidate",     grammar: "Superlatives",                         voice: "maria",    num: "09" },
  10: { title: "Our Process Is Faster Now",              grammar: "Comparative & Superlative Adverbs",    voice: "carlos",   num: "10" },
  11: { title: "Have You Worked Here Long?",             grammar: "Present Perfect — For & Since",        voice: "maria",    num: "11" },
  12: { title: "We've Just Hired Three People",          grammar: "Present Perfect — Just, Already, Yet", voice: "carlos",   num: "12" },
};

const AUDIO_SCRIPTS = {
  1: `My name is María. I work in HR. I started five years ago. I studied psychology at university. I finished in 2018. I wanted to work with people. I applied for many jobs. I got an interview at MineSafe. The interview went well. They called me the next day. I started as an HR assistant. Two years later, I moved to the recruitment team. I learned a lot. Last year, I changed roles again. I became an HR Coordinator. I love my job.`,
  2: `Last month I had a difficult week. My name is Carlos. I work in recruitment. On Monday I posted a new job. I expected about 30 applications. By Tuesday I received 150. I didn't expect so many. Many candidates didn't have the right skills. About 100 didn't meet our needs. On Thursday I sent 15 invitations. Five candidates didn't reply. Two candidates didn't come to the interviews. They didn't call. They didn't email. I didn't hire anyone that week.`,
  3: `Good morning. My name is Patricia. Last month we received 150 applications. We had three open positions. My team read all 150 CVs. We selected 30 candidates. We sent them an online test. 25 candidates completed the test. We invited 15 candidates to a first interview. Then we selected six for a second interview. In the end, we hired three people. This was a very good month for our team.`,
  4: `I had an important interview last year. My name is Carlos. I saw the job online. I felt excited right away. I went to their website and applied the same day. Two weeks later they called me. I went on a Tuesday morning. The interview took one hour. The manager asked good questions. I gave clear answers. Three days later they called again. I went to a second interview. The manager said I got the job. I was very happy. I started the next Monday.`,
  5: `Hi, I'm María. I have a lot of work this week. Today is Monday. I'm going to review 50 CVs. I'm going to make a short list by noon. Then I'm going to send emails to the best candidates. Tomorrow I'm going to call five people. I'm going to ask about their work history. On Wednesday I'm going to set up the interviews. On Thursday and Friday I'm going to run the interviews. It's a busy week. But I have a clear plan.`,
  6: `Hi Patricia. It's María. I'm calling about the new role. I'll send you the job description today. You'll have it before lunch. Yes, I'll add the salary range to the document. I'll also send you the team structure. I'll explain everything by email. I'll set up a call for next week. We'll talk through all the details. I'll post the role on Friday. I'll send you the link right away.`,
  7: `Hi Carlos. I have some questions about our process. Will you post the job this week? Yes. I'll post it on Monday. About 80 people will apply. How long will the review take? It will take about three days. Then I'll make a short list. Will you do phone calls first? Yes. I'll call the best candidates. Each call will take 20 minutes. How many people will you interview? I'll interview ten people. When will we make a decision? We'll decide by the end of the month.`,
  8: `Hello. My name is Patricia. I need to choose between two candidates. The first candidate is Ana. She has five years of work experience. She speaks two languages. Her interview score was 85 out of 100. The second candidate is Luis. He has three years of experience. His score was 78 out of 100. Ana is more experienced than Luis. She is also a better communicator. Her score is higher than his score. Ana is a better match for this role.`,
  9: `Good afternoon. My name is María. We interviewed six people for this role. Her name is Sofia. She has the most experience on our list. She worked in HR for eight years. She is also the most qualified candidate. Her interview was the best of the six. She gave the clearest answers. Her test score was the highest. She scored 94 out of 100. I recommend Sofia for this role. She is the strongest candidate we have seen this year.`,
  10: `Hi Carlos. I have some good news about our team. Our process is faster now. We used to take four weeks. Now we take two weeks. We review CVs more quickly now. We also schedule interviews more efficiently. We respond to candidates more promptly now. Before, we waited five days. Now we reply in two days. Our new hires are performing more strongly than before. This is the best result we've had in three years.`,
  11: `Hi! I'm María. Welcome to the team. Have you worked in HR before? Yes, I have. I've worked in HR for four years. Have you used our software system? No, I haven't. It's new to me. But I've used similar tools. Have you met the team yet? I've met two people so far. Carlos and Patricia. They seem very friendly. Have you had lunch yet? No, I haven't. I've been in meetings all morning. Let's go together. I'll introduce you to more people.`,
  12: `Hi everyone. I'm Carlos. I have some updates from this week. We've just hired three new people. They start next Monday. I've already sent them their contracts. They've already signed and returned them. I've also just posted two more jobs. I've already written the job descriptions. I've already shared them with the managers. Have you reviewed the new hire profiles yet? I haven't scheduled the welcome meeting yet. I'll do that today. It's been a great week. Well done to the team!`,
};

const GITHUB_RAW = "https://raw.githubusercontent.com/BTHKO/ESL_GEN/main";
const IMAGES = {
  1:  { scene: `${GITHUB_RAW}/GEN_A2_L01_IMG_SCENE_01_V2.png`,  grammar: `${GITHUB_RAW}/GEN_A2_L01_IMG_LABEL_01_V1.png` },
  2:  { scene: `${GITHUB_RAW}/GEN_A2_L02_IMG_SCENE_01_V2.png`,  grammar: `${GITHUB_RAW}/GEN_A2_L02_IMG_MATCH_01_V2.png` },
  3:  { scene: `${GITHUB_RAW}/GEN_A2_L03_IMG_SCENE_01_V1.png`,  grammar: `${GITHUB_RAW}/GEN_A2_L03_IMG_MATCH_01_V1.png` },
  4:  { scene: `${GITHUB_RAW}/GEN_A2_L04_IMG_SCENE_0.png`,      grammar: `${GITHUB_RAW}/GEN_A2_L04_IMG_MATCH_01_V1.png` },
  5:  { scene: `${GITHUB_RAW}/GEN_A2_L05_IMG_SCENE_01_V1.png`,  grammar: `${GITHUB_RAW}/GEN_A2_L05_IMG_SCENE_01_V1.png` },
  6:  { scene: `${GITHUB_RAW}/GEN_A2_L06_IMG_SCENE_01_V1.png`,  grammar: `${GITHUB_RAW}/GEN_A2_L06_IMG_SCENE_01_V1.png` },
  7:  { scene: `${GITHUB_RAW}/EN_A2_L07_IMG_SCENE_01_V1.png`,   grammar: `${GITHUB_RAW}/EN_A2_L07_IMG_SCENE_01_V1.png` },
  8:  { scene: `${GITHUB_RAW}/GEN_A2_L08_IMG_SCENE_01_V1.png`,  grammar: `${GITHUB_RAW}/GEN_A2_L08_IMG_SCENE_01_V1.png` },
  9:  { scene: `${GITHUB_RAW}/GEN_A2_L08_IMG_SCENE_01_V1.png`,  grammar: `${GITHUB_RAW}/GEN_A2_L03_IMG_MATCH_01_V1.png` },
  10: { scene: `${GITHUB_RAW}/GEN_A2_L02_IMG_SCENE_01_V2.png`,  grammar: `${GITHUB_RAW}/GEN_A2_L04_IMG_MATCH_01_V1.png` },
  11: { scene: `${GITHUB_RAW}/GEN_A2_L06_IMG_SCENE_01_V1.png`,  grammar: `${GITHUB_RAW}/GEN_A2_L01_IMG_MATCH_01_V2.png` },
  12: { scene: `${GITHUB_RAW}/GEN_A2_L01_IMG_SCENE_01_V2.png`,  grammar: `${GITHUB_RAW}/GEN_A2_L02_IMG_MATCH_01_V2.png` },
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Content-Type": "application/json"
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: { ...cors, "Access-Control-Allow-Methods": "GET,POST", "Access-Control-Allow-Headers": "Content-Type" } });
    }

    // Health check
    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ status: "ok", workers: "hko-content" }), { headers: cors });
    }

    // Generate one lesson HTML
    if (url.pathname === "/generate" && request.method === "POST") {
      try {
        const body = await request.json();
        const n = parseInt(body.lessonNumber) || 1;
        const meta = LESSONS[n];
        if (!meta) return new Response(JSON.stringify({ error: "Invalid lesson number 1-12" }), { status: 400, headers: cors });

        const html = buildLesson(n, meta, IMAGES[n] || IMAGES[1]);
        const key = `lesson:a2:${meta.num}`;
        await env.KV.put(key, html);

        return new Response(JSON.stringify({
          success: true,
          lessonNumber: n,
          title: meta.title,
          kvKey: key,
          htmlLength: html.length
        }), { headers: cors });

      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: cors });
      }
    }

    // Generate ALL 12 lessons
    if (url.pathname === "/generate-all" && request.method === "POST") {
      const results = [];
      for (let n = 1; n <= 12; n++) {
        try {
          const meta = LESSONS[n];
          const html = buildLesson(n, meta, IMAGES[n] || IMAGES[1]);
          await env.KV.put(`lesson:a2:${meta.num}`, html);
          results.push({ lesson: n, title: meta.title, status: "ok", bytes: html.length });
        } catch (e) {
          results.push({ lesson: n, status: "error", error: e.message });
        }
      }
      return new Response(JSON.stringify({ success: true, results }), { headers: cors });
    }

    // Get stored lesson HTML
    if (url.pathname === "/lesson" && request.method === "GET") {
      const n = url.searchParams.get("n") || "1";
      const num = n.padStart(2, "0");
      const html = await env.KV.get(`lesson:a2:${num}`);
      if (!html) return new Response("Not generated yet — POST /generate first", { status: 404 });
      return new Response(html, { headers: { "Content-Type": "text/html" } });
    }

    // Get audio script for a lesson (used by hko-media)
    if (url.pathname === "/audio-script" && request.method === "GET") {
      const n = parseInt(url.searchParams.get("n")) || 1;
      const script = AUDIO_SCRIPTS[n];
      if (!script) return new Response(JSON.stringify({ error: "Not found" }), { status: 404, headers: cors });
      return new Response(JSON.stringify({ script, lesson: n, title: LESSONS[n]?.title }), { headers: cors });
    }

    return new Response(JSON.stringify({
      worker: "hko-content",
      endpoints: [
        "GET  /health",
        "POST /generate        {lessonNumber: 1-12}",
        "POST /generate-all    {}",
        "GET  /lesson?n=1",
        "GET  /audio-script?n=1"
      ]
    }), { headers: cors });
  }
};

function buildLesson(n, meta, imgs) {
  const num = meta.num;
  const script = AUDIO_SCRIPTS[n] || "";
  const audioUrl = `https://hko-media.mrhkruger-content.workers.dev/audio?n=${n}`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>HKO A2 L${num} · ${meta.title}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Syne:wght@700;800&display=swap');
:root{--blue:#28597A;--green:#2E8B57;--amber:#c87137;--red:#e03131;--bg:#f4f6fb;--card:#fff;--line:#e2e8f0;--muted:#7a8fa6;--ink:#0f1923;--r:12px}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--ink);font-size:15px;line-height:1.55}
.topbar{position:sticky;top:0;z-index:200;background:rgba(255,255,255,.96);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px;padding:8px 16px}
.logo{width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,var(--blue),var(--green));display:grid;place-items:center;color:#fff;font-weight:800;font-size:11px}
.lid{font-family:'Syne',sans-serif;font-size:.82rem;font-weight:700}.lid span{color:var(--muted);font-weight:500}
.tr{margin-left:auto;display:flex;gap:8px;align-items:center}
.xp{background:#fff4de;border:1px solid #ffd480;color:var(--amber);font-size:.75rem;font-weight:700;padding:4px 10px;border-radius:99px}
.pb{display:flex;align-items:center;gap:6px;font-size:.72rem;color:var(--muted);font-weight:700}
.pbr{width:80px;height:5px;background:var(--line);border-radius:99px;overflow:hidden}
.pbf{height:100%;background:linear-gradient(90deg,var(--blue),var(--green));border-radius:99px;transition:width .4s}
.shell{max-width:860px;margin:0 auto;padding:16px 14px 80px}
.hero{border-radius:16px;overflow:hidden;margin-bottom:14px;background:linear-gradient(135deg,#0f1923,#1a3a60);display:grid;grid-template-columns:1fr 240px;min-height:200px}
.ht{padding:24px;z-index:1}.htag{display:inline-block;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);color:rgba(255,255,255,.8);font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:3px 10px;border-radius:99px;margin-bottom:10px}
.ht h1{font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:#fff;line-height:1.1;margin-bottom:6px}.ht p{font-size:.83rem;color:rgba(255,255,255,.6)}
.hstats{display:flex;gap:10px;margin-top:14px}.hst{background:rgba(255,255,255,.08);border-radius:8px;padding:6px 10px;text-align:center}
.hst strong{display:block;color:#fff;font-size:.9rem;font-family:'Syne',sans-serif}.hst span{color:rgba(255,255,255,.5);font-size:.66rem;text-transform:uppercase;letter-spacing:.06em}
.hi{overflow:hidden}.hi img{width:100%;height:100%;object-fit:cover;opacity:.75}
.stage{background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:0 2px 12px rgba(15,25,35,.08);margin-bottom:12px;overflow:hidden;scroll-margin-top:68px}
.sh{display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid var(--line);background:linear-gradient(90deg,#fafbfe,#f4f7ff)}
.sb-v{font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em;padding:3px 9px;border-radius:99px;background:#e8f2f8;color:var(--blue)}
.sb-g{font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em;padding:3px 9px;border-radius:99px;background:#ebfbee;color:var(--green)}
.st{font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:var(--ink)}
.sb{padding:14px 16px;display:grid;gap:12px}
.c2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.ib{background:#f0f3f8;border-radius:10px;overflow:hidden}.ib img{width:100%;object-fit:cover;min-height:160px;border-radius:10px;display:block}
.ib-ph{min-height:160px;display:flex;align-items:center;justify-content:center;font-size:.8rem;color:var(--muted)}
.inb{background:#e8f2f8;border-left:3px solid var(--blue);border-radius:0 8px 8px 0;padding:8px 12px}
.inb .i{font-size:.83rem;color:#3d4f5c;font-weight:500}.inb .es{font-size:.77rem;color:var(--muted);font-style:italic;margin-top:2px}
.choices{display:grid;gap:7px}
.choice{padding:9px 13px;border-radius:9px;border:1.5px solid var(--line);background:#fafbfc;font-size:.85rem;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:8px}
.choice:hover{border-color:var(--blue);background:#e8f2f8}
.mk{width:18px;height:18px;border-radius:50%;border:2px solid var(--line);flex-shrink:0}
.choice.correct{background:#ebfbee;border-color:#7cc090;color:var(--green)}.choice.wrong{background:#fff0f0;border-color:#f4b8b8;color:var(--red)}
.mw{display:grid;grid-template-columns:1fr 1fr;gap:8px}.mc{display:grid;gap:6px}
.mi{padding:9px 12px;border-radius:9px;border:1.5px solid var(--line);background:#fafbfc;font-size:.82rem;cursor:pointer;transition:all .15s;text-align:center}
.mi:hover{border-color:var(--blue);background:#e8f2f8}.mi.selected{border-color:var(--blue);background:#e8f2f8;color:var(--blue);font-weight:700}
.mi.matched{background:#ebfbee;border-color:#7cc090;color:var(--green);cursor:default}
.mi.wf{background:#fff0f0;border-color:#f4b8b8;animation:shake .3s}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-4px)}75%{transform:translateX(4px)}}
.fr{display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:.87rem;padding:10px 12px;background:#f7f9fc;border-radius:9px;border:1px solid var(--line)}
.fi{border:none;border-bottom:2px solid var(--blue);background:transparent;color:var(--blue);font-weight:700;font-size:.87rem;font-family:inherit;outline:none;min-width:80px;text-align:center;padding:0 4px}
.fp{padding:6px 12px;border-radius:99px;background:#e8f2f8;border:1.5px solid #b8d4e4;color:var(--blue);font-size:.8rem;font-weight:700;cursor:pointer;transition:all .15s}
.fp:hover{background:var(--blue);color:#fff}
.ab{display:inline-flex;align-items:center;gap:7px;padding:8px 14px;border-radius:9px;background:#fff4de;border:1.5px solid #ffd480;color:var(--amber);font-weight:700;font-size:.8rem;cursor:pointer}
.aw{display:flex;align-items:center;gap:2px;height:16px}
.aw span{width:3px;background:var(--amber);border-radius:99px;animation:wave 1s ease-in-out infinite}
.aw span:nth-child(1){height:6px}.aw span:nth-child(2){height:12px;animation-delay:.1s}.aw span:nth-child(3){height:16px;animation-delay:.2s}.aw span:nth-child(4){height:10px;animation-delay:.3s}.aw span:nth-child(5){height:6px;animation-delay:.4s}
@keyframes wave{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.5)}}
.tr2{background:#f7f9fc;border:1.5px dashed var(--line);border-radius:10px;padding:12px;font-size:.83rem;line-height:1.9}
.ts{font-weight:800;color:var(--blue)}.tt{color:var(--amber);font-weight:700;background:#fff4de;padding:0 3px;border-radius:3px}
.gb{background:#fff;border:1.5px solid var(--line);border-radius:10px;overflow:hidden}
.gbh{background:linear-gradient(90deg,#ebfbee,#f8fdf8);padding:10px 14px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:8px}
.gbh h4{font-family:'Syne',sans-serif;font-size:.9rem;font-weight:800;color:var(--green)}
.gu{font-size:.75rem;color:#4a7c59;background:#d3f9d8;border-radius:5px;padding:2px 8px;font-weight:700}
.gbb{padding:12px 14px;display:grid;gap:8px}
.gt{width:100%;border-collapse:collapse;font-size:.8rem}
.gt th{background:#ebfbee;color:var(--green);padding:6px 10px;text-align:left;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em}
.gt td{padding:7px 10px;border-bottom:1px solid #f0f4f0;vertical-align:top}.gt tr:last-child td{border:none}
.gt .t{color:var(--blue);font-weight:700}
.ge{background:#fff0f0;border-radius:8px;padding:8px 12px;font-size:.8rem}.ge .x{color:var(--red);text-decoration:line-through}.ge .ok{color:var(--green);font-weight:700}
.wt{background:#fafbfe;border:1.5px solid var(--line);border-radius:10px;padding:12px}
.wc{background:#fff4de;border-left:3px solid var(--amber);border-radius:0 8px 8px 0;padding:8px 12px;font-size:.8rem;color:#6b4c00;margin-bottom:10px}
.wc strong{display:block;color:var(--amber);font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px}
textarea.wa{width:100%;border:1.5px solid var(--line);border-radius:9px;padding:10px;font-family:inherit;font-size:.85rem;line-height:1.6;resize:none;background:#fff;color:var(--ink);min-height:110px}
textarea.wa:focus{outline:none;border-color:var(--blue)}
details.sug{margin-top:8px;border:1px dashed var(--line);border-radius:9px;padding:8px 12px;background:#fafcfe}
details.sug summary{cursor:pointer;font-size:.78rem;font-weight:700;color:var(--amber)}
details.sug .sgb{padding-top:8px;font-size:.82rem;line-height:1.7;color:#3d4f5c}
.fb{padding:8px 12px;border-radius:9px;font-size:.82rem;font-weight:600;display:none;align-items:center;gap:7px}
.fb.ok{background:#ebfbee;border:1px solid #7cc090;color:#2a7a40;display:flex}.fb.err{background:#fff0f0;border:1px solid #f4b8b8;color:var(--red);display:flex}.fb.hint{background:#fff4de;border:1px solid #ffd480;color:#7a5500;display:flex}
.btn{border:none;border-radius:9px;padding:8px 14px;font-family:inherit;font-size:.8rem;font-weight:700;cursor:pointer;transition:all .15s;display:inline-flex;align-items:center;gap:6px}
.bp{background:var(--blue);color:#fff}.bp:hover{background:#1e4a6a}.bg{background:var(--green);color:#fff}.bgh{background:#fff;color:var(--ink);border:1.5px solid var(--line)}.bgh:hover{border-color:var(--blue);color:var(--blue)}.ba{background:var(--amber);color:#fff}.sm{padding:5px 10px;font-size:.75rem}
.ctrl{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;padding-top:10px;border-top:1px solid var(--line);margin-top:4px}
.br{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.bdg{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:99px;font-size:.78rem;font-weight:700;border:1.5px dashed var(--line);color:var(--muted);transition:all .3s}
.bdg.earned{background:#fff4de;border-color:var(--amber);color:var(--amber);animation:pop .4s ease}
@keyframes pop{0%{transform:scale(.8)}60%{transform:scale(1.1)}100%{transform:scale(1)}}
.bdgr{display:flex;gap:8px;flex-wrap:wrap}
.sbk{display:flex;align-items:center;gap:10px;margin:18px 0 12px}
.sbk h2{font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:var(--green);white-space:nowrap}
.sbk hr{flex:1;border:none;border-top:2px solid #ebfbee}
.qc{background:var(--card);border:1.5px solid var(--line);border-radius:var(--r);box-shadow:0 2px 12px rgba(15,25,35,.08);padding:16px;margin-bottom:12px}
.qq{font-size:.88rem;font-weight:700;color:var(--ink);margin-bottom:10px}
.scb{background:linear-gradient(135deg,#e8f2f8,#e3fafc);border:1px solid #b8d4e4;border-radius:10px;padding:12px;text-align:center;display:none}
.scn{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:var(--blue)}
.cdl{list-style:none;display:grid;gap:7px}
.cdi{display:flex;align-items:center;gap:9px;padding:8px 11px;border-radius:9px;border:1.5px solid var(--line);background:#fafbfd;font-size:.84rem;cursor:pointer;transition:all .15s}
.cdi input{accent-color:var(--green);width:16px;height:16px;flex-shrink:0}.cdi.chk{background:#ebfbee;border-color:#7cc090}
.vg{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.vgi{background:#f7f9fc;border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:.8rem}
.vgi strong{color:var(--blue);display:block;font-weight:700}.vgi span{color:var(--muted);font-style:italic}
.mb{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.mc2{aspect-ratio:1;border-radius:10px;border:2px solid var(--line);background:linear-gradient(135deg,var(--blue),var(--green));cursor:pointer;position:relative;transform-style:preserve-3d;transition:transform .35s}
.mc2.fl,.mc2.mt{transform:rotateY(180deg)}
.mcf,.mcb{position:absolute;inset:0;border-radius:8px;display:grid;place-items:center;backface-visibility:hidden;font-size:.82rem;font-weight:700;padding:6px;text-align:center}
.mcf{color:rgba(255,255,255,.4);font-size:1.4rem}.mcb{background:#fff;color:var(--blue);transform:rotateY(180deg)}
.mc2.mt .mcb{background:#ebfbee;color:var(--green)}
.snav{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:12px 14px;margin-bottom:14px}
.snr{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.snb{display:flex;align-items:center;gap:4px;padding:5px 10px;border-radius:7px;font-size:.72rem;font-weight:700;cursor:pointer;border:1px solid var(--line);background:#f7f9fc;color:var(--muted);transition:all .15s;white-space:nowrap}
.snb.v{color:var(--blue);border-color:#b8d4e4;background:#e8f2f8}.snb.g{color:var(--green);border-color:#b2d9bc;background:#ebfbee}
.snb.dn::after{content:' ✓';opacity:.7}
@media(max-width:600px){.c2,.mw,.vg{grid-template-columns:1fr}.hero{grid-template-columns:1fr}.hi{display:none}.mb{grid-template-columns:repeat(4,1fr)}}
</style>
</head>
<body>
<div class="topbar">
  <div class="logo">HKO</div>
  <div><div class="lid">A2 · Lesson ${num} <span>· ${meta.title}</span></div></div>
  <div class="tr">
    <div class="xp">⚡ <span id="xp">0</span> XP</div>
    <div class="pb"><div class="pbr"><div class="pbf" id="prog" style="width:0%"></div></div><span id="pt">0%</span></div>
  </div>
</div>
<div class="shell">

<div class="hero">
  <div class="ht">
    <div class="htag">A2 · HR English · ${meta.grammar}</div>
    <h1>"${meta.title}"</h1>
    <p>Learn to use ${meta.grammar.toLowerCase()} in real HR situations.</p>
    <div class="hstats">
      <div class="hst"><strong>14</strong><span>Stages</span></div>
      <div class="hst"><strong>500</strong><span>XP</span></div>
      <div class="hst"><strong>~4h</strong><span>Total</span></div>
    </div>
  </div>
  <div class="hi"><img src="${imgs.scene}" alt="HR scene" onerror="this.style.background='linear-gradient(135deg,#1a3a60,#0c4a6e)';this.style.minHeight='200px'"></div>
</div>

<div style="background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:14px;margin-bottom:14px;display:flex;gap:14px">
  <div style="width:32px;height:32px;background:#e8f2f8;border-radius:8px;display:grid;place-items:center;font-size:1rem;flex-shrink:0">🎯</div>
  <div>
    <div style="font-family:'Syne',sans-serif;font-size:.82rem;font-weight:800;color:var(--blue);margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em">By the end of this lesson you can…</div>
    <ul style="list-style:none;display:grid;gap:4px">
      <li style="font-size:.83rem;color:#3d4f5c;display:flex;gap:6px"><span style="color:var(--green);font-weight:800">✓</span> Use ${meta.grammar.toLowerCase()} in HR contexts</li>
      <li style="font-size:.83rem;color:#3d4f5c;display:flex;gap:6px"><span style="color:var(--green);font-weight:800">✓</span> Understand spoken HR English at A2 level</li>
      <li style="font-size:.83rem;color:#3d4f5c;display:flex;gap:6px"><span style="color:var(--green);font-weight:800">✓</span> Write a short professional message using this grammar</li>
      <li style="font-size:.83rem;color:#3d4f5c;display:flex;gap:6px"><span style="color:var(--green);font-weight:800">✓</span> Ask and answer questions about HR situations</li>
    </ul>
  </div>
</div>

<div class="snav">
  <div style="font-size:.7rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:4px">Lesson Stages</div>
  <div class="snr">
    <button class="snb v" id="nav-v1" onclick="jt('v1')">👁 V1</button>
    <button class="snb v" id="nav-v2" onclick="jt('v2')">🔤 V2</button>
    <button class="snb v" id="nav-v3" onclick="jt('v3')">🎙 V3</button>
    <button class="snb v" id="nav-v4" onclick="jt('v4')">🎮 V4</button>
    <button class="snb v" id="nav-v5" onclick="jt('v5')">🧩 V5</button>
    <button class="snb v" id="nav-v6" onclick="jt('v6')">✏️ V6</button>
    <button class="snb v" id="nav-v7" onclick="jt('v7')">🎤 V7</button>
    <button class="snb g" id="nav-g1" onclick="jt('g1')">🔍 G1</button>
    <button class="snb g" id="nav-g2" onclick="jt('g2')">📖 G2</button>
    <button class="snb g" id="nav-g3" onclick="jt('g3')">🔀 G3</button>
    <button class="snb g" id="nav-g4" onclick="jt('g4')">✅ G4</button>
    <button class="snb g" id="nav-g5" onclick="jt('g5')">🛠 G5</button>
    <button class="snb g" id="nav-g6" onclick="jt('g6')">📝 G6</button>
    <button class="snb g" id="nav-g7" onclick="jt('g7')">📧 G7</button>
  </div>
</div>

<!-- V1 -->
<div class="stage" id="v1">
  <div class="sh"><span class="sb-v">👁 Word Builder · Stage 1</span><span class="st">Look at the Scene</span></div>
  <div class="sb">
    <div class="c2">
      <div class="ib"><img src="${imgs.scene}" alt="HR scene" onerror="this.style.minHeight='160px';this.style.background='var(--blue-l)'"></div>
      <div style="display:grid;gap:8px">
        <div class="inb"><div class="i">Look at the image. Answer the questions below.</div><div class="es">Mira la imagen. Responde las preguntas.</div></div>
        <div style="font-size:.82rem;font-weight:700;color:#3d4f5c">What can you see? Choose all that apply.</div>
        <div class="choices" id="v1c">
          <div class="choice" onclick="tog(this,'correct')"><div class="mk"></div>HR professionals at work</div>
          <div class="choice" onclick="tog(this,'correct')"><div class="mk"></div>A professional office environment</div>
          <div class="choice" onclick="tog(this,'wrong')"><div class="mk"></div>Someone working alone at home</div>
          <div class="choice" onclick="tog(this,'correct')"><div class="mk"></div>People having a work discussion</div>
        </div>
      </div>
    </div>
    <div class="ctrl"><span></span><button class="btn bp" onclick="cs('v1','v2')">Next →</button></div>
  </div>
</div>

<!-- V2 -->
<div class="stage" id="v2">
  <div class="sh"><span class="sb-v">🔤 Word Builder · Stage 2</span><span class="st">Meet the Words</span></div>
  <div class="sb">
    <div class="inb"><div class="i">Match each career action to its meaning. Click a word, then its match.</div><div class="es">Une cada acción con su significado.</div></div>
    <div class="mw" id="v2m">
      <div class="mc"><div class="mi" data-pair="a" onclick="mc(this)">started</div><div class="mi" data-pair="b" onclick="mc(this)">graduated</div><div class="mi" data-pair="c" onclick="mc(this)">applied</div><div class="mi" data-pair="d" onclick="mc(this)">received</div><div class="mi" data-pair="e" onclick="mc(this)">changed</div><div class="mi" data-pair="f" onclick="mc(this)">joined</div></div>
      <div class="mc"><div class="mi" data-pair="c" onclick="mc(this)">formally requested a job</div><div class="mi" data-pair="e" onclick="mc(this)">moved to something different</div><div class="mi" data-pair="a" onclick="mc(this)">began a role or position</div><div class="mi" data-pair="f" onclick="mc(this)">became part of a team</div><div class="mi" data-pair="d" onclick="mc(this)">got something back</div><div class="mi" data-pair="b" onclick="mc(this)">finished university studies</div></div>
    </div>
    <div id="v2fb" class="fb"></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('v1')">← Back</button><button class="btn bp" onclick="cs('v2','v3')">Next →</button></div>
  </div>
</div>

<!-- V3 -->
<div class="stage" id="v3">
  <div class="sh"><span class="sb-v">🎙 Word Builder · Stage 3</span><span class="st">Listen to the Story</span></div>
  <div class="sb">
    <div class="c2">
      <div class="ib"><img src="${imgs.scene}" alt="character" onerror="this.style.minHeight='160px';this.style.background='#e8f2f8'"></div>
      <div style="display:grid;gap:8px;align-content:start">
        <div class="inb"><div class="i">Listen. Notice the highlighted words.</div><div class="es">Escucha. Nota las palabras destacadas.</div></div>
        <div class="ab" onclick="pAudio(this)" id="abtn"><span>🔊</span><span id="atxt">Play Story</span><div class="aw"><span></span><span></span><span></span><span></span><span></span></div></div>
        <button class="btn bgh sm" onclick="var t=document.getElementById('v3t');t.style.display=t.style.display==='none'?'block':'none'">📄 Show/Hide Script</button>
        <div class="tr2" id="v3t" style="display:none">${script}</div>
      </div>
    </div>
    <div style="font-size:.82rem;font-weight:700;color:#3d4f5c">Answer the questions.</div>
    <div style="display:grid;gap:10px">
      <div><div style="font-size:.82rem;color:#3d4f5c;margin-bottom:5px;font-weight:600">1. What grammar does this lesson focus on?</div>
        <div class="choices"><div class="choice" onclick="qq(this,'a')"><div class="mk"></div>${meta.grammar} ✓</div><div class="choice" onclick="qq(this,'b')"><div class="mk"></div>Present Continuous</div><div class="choice" onclick="qq(this,'b')"><div class="mk"></div>Passive Voice</div></div></div>
      <div><div style="font-size:.82rem;color:#3d4f5c;margin-bottom:5px;font-weight:600">2. What professional context does this lesson use?</div>
        <div class="choices"><div class="choice" onclick="qq(this,'a')"><div class="mk"></div>HR and Recruitment in Chile ✓</div><div class="choice" onclick="qq(this,'b')"><div class="mk"></div>Cooking and restaurants</div><div class="choice" onclick="qq(this,'b')"><div class="mk"></div>Sports and exercise</div></div></div>
    </div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('v2')">← Back</button><button class="btn bp" onclick="cs('v3','v4')">Next →</button></div>
  </div>
</div>

<!-- V4 -->
<div class="stage" id="v4">
  <div class="sh"><span class="sb-v">🎮 Word Builder · Stage 4</span><span class="st">Memory Game</span></div>
  <div class="sb">
    <div class="inb"><div class="i">Flip cards to find matching pairs: English ↔ Spanish.</div><div class="es">Voltea fichas para encontrar los pares correctos.</div></div>
    <div class="mb" id="memb"></div>
    <div style="display:flex;justify-content:space-between;font-size:.78rem;color:var(--muted);margin-top:4px"><span>Pairs: <strong id="memp">0</strong>/4</span><button class="btn bgh sm" onclick="iMem()">↩ Reset</button></div>
    <div id="v4fb" class="fb"></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('v3')">← Back</button><button class="btn bp" onclick="cs('v4','v5')">Next →</button></div>
  </div>
</div>

<!-- V5 -->
<div class="stage" id="v5">
  <div class="sh"><span class="sb-v">🧩 Word Builder · Stage 5</span><span class="st">Fill the Gaps</span></div>
  <div class="sb">
    <div class="inb"><div class="i">Choose the correct word to complete each sentence.</div><div class="es">Elige la palabra correcta para completar cada oración.</div></div>
    <div style="display:grid;gap:9px">
      <div class="fr">I <input class="fi" id="f1" placeholder="?" style="width:90px"> from university in 2018.<span class="fp" onclick="fi('f1',this,'graduated')">graduated</span><span class="fp" onclick="fi('f1',this,'started')">started</span></div>
      <div class="fr">She <input class="fi" id="f2" placeholder="?" style="width:75px"> for the position last month.<span class="fp" onclick="fi('f2',this,'applied')">applied</span><span class="fp" onclick="fi('f2',this,'joined')">joined</span></div>
      <div class="fr">He <input class="fi" id="f3" placeholder="?" style="width:70px"> the HR team in 2021.<span class="fp" onclick="fi('f3',this,'joined')">joined</span><span class="fp" onclick="fi('f3',this,'changed')">changed</span></div>
    </div>
    <div class="br" style="margin-top:6px"><button class="btn bgh sm" onclick="cf(['f1:graduated','f2:applied','f3:joined'],'v5fb')">✓ Check</button></div>
    <div id="v5fb" class="fb"></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('v4')">← Back</button><button class="btn bp" onclick="cs('v5','v6')">Next →</button></div>
  </div>
</div>

<!-- V6 -->
<div class="stage" id="v6">
  <div class="sh"><span class="sb-v">✏️ Word Builder · Stage 6</span><span class="st">Spot the Error</span></div>
  <div class="sb">
    <div class="inb"><div class="i">Choose the correct sentence in each pair.</div><div class="es">Elige la oración correcta en cada par.</div></div>
    <div class="choices" id="v6a"><div class="choice" onclick="p1(this,'v6a','wrong')"><div class="mk"></div>She didn't <u>worked</u> in finance.</div><div class="choice" onclick="p1(this,'v6a','correct')"><div class="mk"></div>She didn't <strong>work</strong> in finance. ✓</div></div>
    <div class="choices" id="v6b" style="margin-top:8px"><div class="choice" onclick="p1(this,'v6b','wrong')"><div class="mk"></div>Did she worked at MineSafe?</div><div class="choice" onclick="p1(this,'v6b','correct')"><div class="mk"></div>Did she <strong>work</strong> at MineSafe? ✓</div></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('v5')">← Back</button><button class="btn bp" onclick="cs('v6','v7')">Next →</button></div>
  </div>
</div>

<!-- V7 -->
<div class="stage" id="v7">
  <div class="sh"><span class="sb-v">🎤 Word Builder · Stage 7</span><span class="st">Tell Your Story</span></div>
  <div class="sb">
    <div class="inb"><div class="i">Record yourself for 30–60 seconds. Use at least 5 lesson words.</div><div class="es">Grábate 30–60 segundos. Usa al menos 5 palabras de esta lección.</div></div>
    <div class="br" style="margin-bottom:8px"><button class="btn ba" onclick="alert('Connect to Moodle audio capture')">🔴 Record</button><button class="btn bgh sm">⏹ Stop</button><button class="btn bgh sm">▶ Play</button></div>
    <details class="sug"><summary>💡 Sample Answer</summary><div class="sgb">I started my career in HR five years ago. I graduated from university and applied for several jobs. I received an offer and worked as an HR assistant. Then I changed roles and joined the recruitment team.</div></details>
    <div class="bdgr" style="margin-top:8px"><div class="bdg" id="bv">🗂 Vocabulary Complete</div></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('v6')">← Back</button><button class="btn bg" onclick="ub('bv');cs('v7','g1')">✅ Start Useful Language →</button></div>
  </div>
</div>

<div class="sbk"><h2>Useful Language</h2><hr></div>

<!-- G1 -->
<div class="stage" id="g1">
  <div class="sh"><span class="sb-g">🔍 Useful Language · Stage 1</span><span class="st">How Did They Say It?</span></div>
  <div class="sb">
    <div class="inb"><div class="i">Read the sentences. What do you notice about the verbs?</div><div class="es">¿Qué notas sobre los verbos?</div></div>
    <div style="display:grid;gap:7px">
      <div style="padding:9px 13px;border-radius:9px;background:#e8f2f8;border-left:3px solid var(--blue);font-size:.88rem">I <strong style="color:var(--blue)">started</strong> five years ago.</div>
      <div style="padding:9px 13px;border-radius:9px;background:#e8f2f8;border-left:3px solid var(--blue);font-size:.88rem">She <strong style="color:var(--blue)">graduated</strong> in 2018.</div>
      <div style="padding:9px 13px;border-radius:9px;background:#e8f2f8;border-left:3px solid var(--blue);font-size:.88rem">We <strong style="color:var(--blue)">received</strong> many applications.</div>
      <div style="padding:9px 13px;border-radius:9px;background:#fff4de;border-left:3px solid var(--amber);font-size:.88rem">I <strong style="color:var(--red)">didn't work</strong> in finance.</div>
    </div>
    <div class="choices" id="g1c"><div class="choice" onclick="p1(this,'g1c','correct')"><div class="mk"></div>They describe finished actions in the past ✓</div><div class="choice" onclick="p1(this,'g1c','wrong')"><div class="mk"></div>They describe things happening right now</div><div class="choice" onclick="p1(this,'g1c','wrong')"><div class="mk"></div>They are about future plans</div></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('v7')">← Back</button><button class="btn bp" onclick="cs('g1','g2')">Next →</button></div>
  </div>
</div>

<!-- G2 -->
<div class="stage" id="g2">
  <div class="sh"><span class="sb-g">📖 Useful Language · Stage 2</span><span class="st">The Language Box</span></div>
  <div class="sb">
    <div class="gb">
      <div class="gbh"><h4>${meta.grammar}</h4><span class="gu">We use this to describe finished HR actions</span></div>
      <div class="gbb">
        <table class="gt"><thead><tr><th>Form</th><th>Structure</th><th>HR Example</th></tr></thead><tbody>
          <tr><td>✅ +</td><td>subject + <span class="t">verb+ed</span></td><td>I <span class="t">started</span> in HR five years ago.</td></tr>
          <tr><td>❌ −</td><td>subject + <span class="t">didn't</span> + base verb</td><td>She <span class="t">didn't work</span> in payroll.</td></tr>
          <tr><td>❓ ?</td><td><span class="t">Did</span> + subject + base verb?</td><td><span class="t">Did</span> you work there long?</td></tr>
        </tbody></table>
        <div class="ge"><div style="font-size:.72rem;font-weight:800;color:var(--red);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px">⚠ Common Error</div><div><span class="x">didn't worked</span> → <span class="ok">didn't work ✓</span></div></div>
      </div>
    </div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('g1')">← Back</button><button class="btn bp" onclick="cs('g2','g3')">Next →</button></div>
  </div>
</div>

<!-- G3 -->
<div class="stage" id="g3">
  <div class="sh"><span class="sb-g">🔀 Useful Language · Stage 3</span><span class="st">Correct or Not?</span></div>
  <div class="sb">
    <div class="inb"><div class="i">Which sentence uses the correct form?</div><div class="es">¿Cuál oración usa la forma correcta?</div></div>
    <div class="choices" id="g3a"><div class="choice" onclick="p1(this,'g3a','wrong')"><div class="mk"></div>I am working last week.</div><div class="choice" onclick="p1(this,'g3a','correct')"><div class="mk"></div>I worked last week. ✓</div><div class="choice" onclick="p1(this,'g3a','wrong')"><div class="mk"></div>I work last week.</div></div>
    <div class="choices" id="g3b" style="margin-top:8px"><div class="choice" onclick="p1(this,'g3b','wrong')"><div class="mk"></div>We didn't received any CVs.</div><div class="choice" onclick="p1(this,'g3b','correct')"><div class="mk"></div>We didn't receive any CVs. ✓</div><div class="choice" onclick="p1(this,'g3b','wrong')"><div class="mk"></div>We not received any CVs.</div></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('g2')">← Back</button><button class="btn bp" onclick="cs('g3','g4')">Next →</button></div>
  </div>
</div>

<!-- G4 -->
<div class="stage" id="g4">
  <div class="sh"><span class="sb-g">✅ Useful Language · Stage 4</span><span class="st">Build the Forms</span></div>
  <div class="sb">
    <div class="inb"><div class="i">Complete each sentence with the correct form.</div><div class="es">Completa con la forma correcta.</div></div>
    <div style="display:grid;gap:9px">
      <div class="fr">I <input class="fi" id="g1" placeholder="?" style="width:85px"> for five positions last year.<span class="fp" onclick="fi('g1',this,'applied')">applied</span><span class="fp" onclick="fi('g1',this,'apply')">apply</span></div>
      <div class="fr">She <input class="fi" id="g2" placeholder="?" style="width:75px"> complete the form.<span class="fp" onclick="fi('g2',this,&quot;didn't&quot;)">didn't</span><span class="fp" onclick="fi('g2',this,'not')">not</span></div>
      <div class="fr"><input class="fi" id="g3" placeholder="?" style="width:40px"> you work in mining before?<span class="fp" onclick="fi('g3',this,'Did')">Did</span><span class="fp" onclick="fi('g3',this,'Do')">Do</span></div>
    </div>
    <div class="br" style="margin-top:6px"><button class="btn bgh sm" onclick="cf([&quot;g1:applied&quot;,&quot;g2:didn't&quot;,'g3:Did'],'g4fb')">✓ Check All</button></div>
    <div id="g4fb" class="fb"></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('g3')">← Back</button><button class="btn bp" onclick="cs('g4','g5')">Next →</button></div>
  </div>
</div>

<!-- G5 -->
<div class="stage" id="g5">
  <div class="sh"><span class="sb-g">🛠 Useful Language · Stage 5</span><span class="st">Listening Practice</span></div>
  <div class="sb">
    <div class="c2">
      <div class="ib"><img src="${imgs.grammar}" alt="Grammar scene" onerror="this.style.minHeight='160px';this.style.background='#ebfbee'"></div>
      <div style="display:grid;gap:7px;align-content:start">
        <div class="inb"><div class="i">Listen. Focus on how questions are formed.</div><div class="es">Escucha. Observa cómo se forman las preguntas.</div></div>
        <div class="ab" onclick="pTTS(['When did you graduate?','I graduated in 2018.','Where did you work after that?','I worked at MineSafe for four years.','Did you manage a team?','No I did not. I was a coordinator.'],this)"><span>🔊</span><span>Play Dialogue</span><div class="aw"><span></span><span></span><span></span><span></span><span></span></div></div>
        <div class="tr2"><p><span class="ts">Interviewer:</span> <span class="tt">When did</span> you graduate?</p><p><span class="ts">Candidate:</span> I graduated in 2018.</p><p><span class="ts">Interviewer:</span> <span class="tt">Where did</span> you work after that?</p><p><span class="ts">Candidate:</span> I worked at MineSafe for four years.</p><p><span class="ts">Interviewer:</span> <span class="tt">Did</span> you manage a team?</p><p><span class="ts">Candidate:</span> No, I <span class="tt">didn't</span>.</p></div>
      </div>
    </div>
    <div class="choices" id="g5c"><div class="choice" onclick="p1(this,'g5c','correct')"><div class="mk"></div>Questions use Did + subject + base verb ✓</div><div class="choice" onclick="p1(this,'g5c','wrong')"><div class="mk"></div>Questions use Does + subject + -ed verb</div></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('g4')">← Back</button><button class="btn bp" onclick="cs('g5','g6')">Next →</button></div>
  </div>
</div>

<!-- G6 -->
<div class="stage" id="g6">
  <div class="sh"><span class="sb-g">📝 Useful Language · Stage 6</span><span class="st">Build Interview Questions</span></div>
  <div class="sb">
    <div class="inb"><div class="i">Choose the correct sentence in each pair.</div><div class="es">Elige la oración correcta en cada par.</div></div>
    <div class="choices" id="g6a"><div class="choice" onclick="p1(this,'g6a','wrong')"><div class="mk"></div>Did she worked at MineSafe?</div><div class="choice" onclick="p1(this,'g6a','correct')"><div class="mk"></div>Did she work at MineSafe? ✓</div></div>
    <div class="choices" id="g6b" style="margin-top:8px"><div class="choice" onclick="p1(this,'g6b','correct')"><div class="mk"></div>How long did you work there? ✓</div><div class="choice" onclick="p1(this,'g6b','wrong')"><div class="mk"></div>How long did you worked there?</div></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('g5')">← Back</button><button class="btn bp" onclick="cs('g6','g7')">Next →</button></div>
  </div>
</div>

<!-- G7 -->
<div class="stage" id="g7">
  <div class="sh"><span class="sb-g">📧 Useful Language · Stage 7</span><span class="st">Write a Professional Message</span></div>
  <div class="sb">
    <div class="wt">
      <div class="wc"><strong>Your Task</strong>Write a short email to your manager about a recent recruitment process. Use ${meta.grammar.toLowerCase()} throughout. Aim for 60–100 words.</div>
      <div style="font-size:.75rem;font-weight:700;color:var(--muted);margin-bottom:5px">Word bank:</div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px"><span class="fp" style="cursor:default">received</span><span class="fp" style="cursor:default">reviewed</span><span class="fp" style="cursor:default">shortlisted</span><span class="fp" style="cursor:default">interviewed</span><span class="fp" style="cursor:default">didn't expect</span></div>
      <textarea class="wa" id="g7t" placeholder="Hi María,&#10;&#10;I wanted to update you on the recruitment process…&#10;&#10;Best regards,&#10;[Your name]" oninput="wc(this,'g7wc')"></textarea>
      <div style="font-size:.72rem;color:var(--muted);text-align:right;margin-top:4px">Words: <span id="g7wc">0</span> / 60–100</div>
      <div class="br" style="margin-top:8px"><button class="btn bgh sm" onclick="cwl('g7t','g7fb',40)">✓ Check Length</button></div>
      <div id="g7fb" class="fb"></div>
      <details class="sug"><summary>💡 Suggested Answer</summary><div class="sgb">Hi María,<br><br>I wanted to update you on the recruitment process. We received 45 applications. I didn't expect so many! I reviewed them and shortlisted six candidates. The interviews went very well. Three candidates performed strongly.<br><br>Best regards,<br>Paula</div></details>
    </div>
    <div class="bdgr" style="margin-top:10px"><div class="bdg" id="bg2">📝 Language Complete</div></div>
    <div class="ctrl"><button class="btn bgh sm" onclick="jt('g6')">← Back</button><button class="btn bg" onclick="ub('bg2');cs('g7','quiz')">✅ Go to Quiz →</button></div>
  </div>
</div>

<div class="sbk" id="quiz"><h2>Lesson Quiz</h2><hr></div>
<div class="qc">
  <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:var(--blue);margin-bottom:4px">📋 End-of-Lesson Check · 20 pts</div>
  <div id="qprog" style="font-size:.72rem;color:var(--muted);margin-bottom:14px">Question 1 of 5</div>
  <div id="qscore" class="scb"></div>
  <div id="qq1"><div class="qq">1. Which sentence uses ${meta.grammar} correctly?</div><div class="choices" id="qc1"><div class="choice" onclick="qp(this,1,'b')"><div class="mk"></div>She is start in HR last year.</div><div class="choice" onclick="qp(this,1,'a')"><div class="mk"></div>She started in HR last year. ✓</div><div class="choice" onclick="qp(this,1,'b')"><div class="mk"></div>She has started in HR last year.</div></div></div>
  <div id="qq2" style="display:none"><div class="qq">2. Complete: "We _____ any candidates." (negative)</div><div class="choices" id="qc2"><div class="choice" onclick="qp(this,2,'b')"><div class="mk"></div>didn't hired</div><div class="choice" onclick="qp(this,2,'a')"><div class="mk"></div>didn't hire ✓</div><div class="choice" onclick="qp(this,2,'b')"><div class="mk"></div>not hired</div></div></div>
  <div id="qq3" style="display:none"><div class="qq">3. "Applied" means…</div><div class="choices" id="qc3"><div class="choice" onclick="qp(this,3,'b')"><div class="mk"></div>started a new job</div><div class="choice" onclick="qp(this,3,'a')"><div class="mk"></div>formally requested a position ✓</div><div class="choice" onclick="qp(this,3,'b')"><div class="mk"></div>graduated from university</div></div></div>
  <div id="qq4" style="display:none"><div class="qq">4. Which question is correct?</div><div class="choices" id="qc4"><div class="choice" onclick="qp(this,4,'b')"><div class="mk"></div>Did she worked there?</div><div class="choice" onclick="qp(this,4,'a')"><div class="mk"></div>Did she work there? ✓</div><div class="choice" onclick="qp(this,4,'b')"><div class="mk"></div>Does she worked there?</div></div></div>
  <div id="qq5" style="display:none"><div class="qq">5. "Joined" means…</div><div class="choices" id="qc5"><div class="choice" onclick="qp(this,5,'b')"><div class="mk"></div>left the company</div><div class="choice" onclick="qp(this,5,'b')"><div class="mk"></div>started university</div><div class="choice" onclick="qp(this,5,'a')"><div class="mk"></div>became part of a team ✓</div></div></div>
</div>

<div class="sbk" id="wrapup"><h2>Lesson Wrap-Up</h2><hr></div>
<div class="stage" style="box-shadow:none">
  <div class="sh"><span class="sb-g">✅ Self Check</span><span class="st">What Can You Do Now?</span></div>
  <div class="sb">
    <ul class="cdl">
      <li class="cdi" onclick="this.querySelector('input').checked=!this.querySelector('input').checked;this.classList.toggle('chk')"><input type="checkbox"> I can use ${meta.grammar.toLowerCase()} in HR contexts.</li>
      <li class="cdi" onclick="this.querySelector('input').checked=!this.querySelector('input').checked;this.classList.toggle('chk')"><input type="checkbox"> I can form negatives and questions correctly.</li>
      <li class="cdi" onclick="this.querySelector('input').checked=!this.querySelector('input').checked;this.classList.toggle('chk')"><input type="checkbox"> I can write a short professional message using this grammar.</li>
      <li class="cdi" onclick="this.querySelector('input').checked=!this.querySelector('input').checked;this.classList.toggle('chk')"><input type="checkbox"> I understand spoken HR English on this topic.</li>
    </ul>
    <div style="font-family:'Syne',sans-serif;font-size:.82rem;font-weight:800;color:var(--blue);margin-top:12px;margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em">Vocabulary from This Lesson</div>
    <div class="vg"><div class="vgi"><strong>started</strong><span>empezar</span></div><div class="vgi"><strong>graduated</strong><span>graduarse</span></div><div class="vgi"><strong>applied</strong><span>postular</span></div><div class="vgi"><strong>received</strong><span>recibir</span></div><div class="vgi"><strong>worked</strong><span>trabajar</span></div><div class="vgi"><strong>joined</strong><span>unirse</span></div><div class="vgi"><strong>changed</strong><span>cambiar</span></div><div class="vgi"><strong>moved</strong><span>mudarse</span></div><div class="vgi"><strong>wanted</strong><span>querer</span></div></div>
    <div class="bdgr" style="margin-top:10px"><div class="bdg" id="bfin">🏆 Lesson Complete</div></div>
    <div class="br" style="margin-top:8px"><button class="btn bg" onclick="fin()">🎉 Finish Lesson</button></div>
  </div>
</div>

</div>
<script>
const ST=['v1','v2','v3','v4','v5','v6','v7','g1','g2','g3','g4','g5','g6','g7'];
const dn=new Set();let xp=0;let qc=1;const qa={1:'a',2:'a',3:'a',4:'a',5:'a'};let qs=0;let mf=null;let mfl=[],mlk=false,mfd=0;
function ax(n){xp+=n;document.getElementById('xp').textContent=xp;}
function up(){const p=Math.round(dn.size/14*100);document.getElementById('prog').style.width=p+'%';document.getElementById('pt').textContent=p+'%';}
function jt(id){const e=document.getElementById(id);if(e)e.scrollIntoView({behavior:'smooth',block:'start'});}
function cs(id,nx){if(!dn.has(id)){dn.add(id);ax(25);}up();const b=document.getElementById('nav-'+id);if(b)b.classList.add('dn');if(nx)setTimeout(()=>jt(nx),300);}
function sfb(id,t,m){const e=document.getElementById(id);if(!e)return;e.className='fb '+t;e.style.display='flex';e.textContent=m;}
function tog(el,r){el.classList.toggle('chosen');if(r==='correct')el.classList.toggle('correct',el.classList.contains('chosen'));else el.classList.toggle('wrong',el.classList.contains('chosen'));}
function p1(el,g,r){const gr=document.getElementById(g);if(!gr)return;gr.querySelectorAll('.choice').forEach(c=>c.classList.remove('correct','wrong','chosen'));el.classList.add(r==='correct'?'correct':'wrong');if(r==='correct')ax(10);}
function qq(el,r){const p=el.closest('.choices');p.querySelectorAll('.choice').forEach(c=>c.classList.remove('correct','wrong'));el.classList.add(r==='a'?'correct':'wrong');if(r==='a')ax(5);}
function mc(el){if(el.classList.contains('matched'))return;if(!mf){el.classList.add('selected');mf=el;}else{if(mf===el){mf.classList.remove('selected');mf=null;return;}if(mf.dataset.pair===el.dataset.pair){mf.classList.remove('selected');mf.classList.add('matched');el.classList.add('matched');ax(15);const al=document.querySelectorAll('#v2m .mi');if([...al].every(i=>i.classList.contains('matched'))){sfb('v2fb','ok','All matched! ✓');ax(20);}mf=null;}else{mf.classList.add('wf');el.classList.add('wf');const a=mf,b=el;mf=null;setTimeout(()=>{a.classList.remove('wf');b.classList.remove('wf');},500);}}}
function fi(id,pill,val){const i=document.getElementById(id);if(!i)return;i.value=val;i.style.color='var(--blue)';}
function cf(pairs,fbId){let ok=0;pairs.forEach(p=>{const[id,ans]=p.split(':');const i=document.getElementById(id);if(!i)return;const m=i.value.trim().toLowerCase()===ans.toLowerCase();i.style.borderBottomColor=m?'var(--green)':'var(--red)';if(m)ok++;});if(ok===pairs.length){sfb(fbId,'ok','All correct! ✓');ax(20);}else sfb(fbId,'err',ok+' of '+pairs.length+' correct.');}
function ub(id){const e=document.getElementById(id);if(e)e.classList.add('earned');}
function wc(ta,cid){document.getElementById(cid).textContent=ta.value.trim().split(/\\s+/).filter(w=>w).length;}
function cwl(tid,fid,min){const ta=document.getElementById(tid);const w=ta.value.trim().split(/\\s+/).filter(w=>w).length;if(w>=min){sfb(fid,'ok','Good length! Check the suggested answer. ✓');ax(25);}else sfb(fid,'hint','Try to write at least '+min+' words. You have '+w+' so far.');}
function pAudio(btn){if('speechSynthesis' in window){speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(${JSON.stringify(script)});u.rate=0.85;u.lang='en-US';btn.classList.add('playing');document.getElementById('atxt').textContent='Playing…';u.onend=()=>{btn.classList.remove('playing');document.getElementById('atxt').textContent='Play Again';};speechSynthesis.speak(u);}}
function pTTS(lines,btn){if('speechSynthesis' in window){speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(lines.join(' ... '));u.rate=0.85;u.lang='en-US';btn.classList.add('playing');u.onend=()=>btn.classList.remove('playing');speechSynthesis.speak(u);}}
const mp=[{a:'started',b:'empezar'},{a:'applied',b:'postular'},{a:'joined',b:'unirse'},{a:'received',b:'recibir'}];
function iMem(){mfl=[];mlk=false;mfd=0;document.getElementById('memp').textContent='0';const bd=document.getElementById('memb');const cs2=[];mp.forEach(({a,b})=>{cs2.push({text:a,pair:a+b});cs2.push({text:b,pair:a+b});});cs2.sort(()=>Math.random()-.5);bd.innerHTML=cs2.map(c=>'<div class="mc2" data-text="'+c.text+'" data-pair="'+c.pair+'" onclick="mfl2(this)"><div class="mcf">?</div><div class="mcb">'+c.text+'</div></div>').join('');}
function mfl2(card){if(mlk||card.classList.contains('mt')||card.classList.contains('fl'))return;card.classList.add('fl');mfl.push(card);if(mfl.length===2){mlk=true;const[a,b]=mfl;if(a.dataset.pair===b.dataset.pair){a.classList.add('mt');b.classList.add('mt');a.classList.remove('fl');b.classList.remove('fl');mfd++;ax(15);document.getElementById('memp').textContent=mfd;mfl=[];mlk=false;if(mfd===mp.length)sfb('v4fb','ok','All pairs found! 🎉');}else setTimeout(()=>{a.classList.remove('fl');b.classList.remove('fl');mfl=[];mlk=false;},800);}}
iMem();
function qp(el,q,opt){const p=el.closest('.choices');p.querySelectorAll('.choice').forEach(c=>c.classList.remove('chosen'));el.classList.add('chosen');setTimeout(()=>{const ok=qa[q]===opt;p.querySelectorAll('.choice').forEach((c,i)=>{const o=['a','b','c'];if(qa[q]===o[i])c.classList.add('correct');else if(c.classList.contains('chosen')&&!ok)c.classList.add('wrong');});if(ok){qs++;ax(20);}setTimeout(()=>{if(qc<5){document.getElementById('qq'+qc).style.display='none';qc++;document.getElementById('qq'+qc).style.display='';document.getElementById('qprog').textContent='Question '+qc+' of 5';}else{document.getElementById('qprog').style.display='none';const pts=qs*4;const sb=document.getElementById('qscore');sb.style.display='block';sb.innerHTML='<div class="scn">'+pts+'<span style="font-size:1rem">/20</span></div><div style="color:var(--muted);font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-top:4px">'+(pts>=16?'Excellent 🏆':pts>=12?'Good job!':'Review & retry')+'</div>';if(pts>=16)ub('bfin');sb.scrollIntoView({behavior:'smooth'});}},900);},600);}
function fin(){ub('bfin');try{var api=null,w=window;for(var i=0;i<7;i++){if(w.API){api=w.API;break;}if(!w.parent||w.parent===w)break;w=w.parent;}if(api){api.LMSInitialize('');api.LMSSetValue('cmi.core.lesson_status',dn.size>=11?'passed':'incomplete');api.LMSSetValue('cmi.core.score.raw',String(xp));api.LMSSetValue('cmi.core.score.min','0');api.LMSSetValue('cmi.core.score.max','500');api.LMSCommit('');api.LMSFinish('');}}catch(e){}alert('🎉 Lesson Complete! You earned '+xp+' XP.');}
</script>
</body>
</html>`;
}
