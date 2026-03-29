// hko-media.js
// Deploy: npx wrangler deploy hko-media.js --name hko-media --compatibility-date 2025-01-01
// Bindings needed: Workers AI (name: AI), KV (name: KV, id: e51e71b8efc34ecc8be226593c2afbc4)

const SCRIPTS = {
  1:  `My name is María. I work in HR. I started five years ago. I studied psychology at university. I finished in 2018. I wanted to work with people. I applied for many jobs. I got an interview at MineSafe. The interview went well. They called me the next day. I started as an HR assistant. Two years later, I moved to the recruitment team. I learned a lot. Last year, I changed roles again. I became an HR Coordinator. I love my job.`,
  2:  `Last month I had a difficult week. My name is Carlos. I work in recruitment. On Monday I posted a new job. I expected about 30 applications. By Tuesday I received 150. I didn't expect so many. Many candidates didn't have the right skills. About 100 didn't meet our needs. I didn't hire anyone that week.`,
  3:  `Good morning. My name is Patricia. Last month we received 150 applications. We had three open positions. My team read all 150 CVs. We selected 30 candidates. In the end, we hired three people. This was a very good month for our team.`,
  4:  `I had an important interview last year. My name is Carlos. I saw the job online. I felt excited right away. I applied the same day. Two weeks later they called me. The interview took one hour. I gave clear answers. The manager said I got the job. I was very happy.`,
  5:  `Hi, I'm María. Today is Monday. I'm going to review 50 CVs. I'm going to make a short list by noon. Then I'm going to send emails to the best candidates. Tomorrow I'm going to call five people. On Wednesday I'm going to set up the interviews. It's a busy week. But I have a clear plan.`,
  6:  `Hi Patricia. It's María. I'll send you the job description today. Yes, I'll add the salary range to the document. I'll also send you the team structure. I'll explain everything by email. I'll set up a call for next week. We'll talk through all the details. I'll post the role on Friday.`,
  7:  `Will you post the job this week? Yes. I'll post it on Monday. How long will the review take? It will take about three days. Will you do phone calls first? Yes. I'll call the best candidates. How many people will you interview? I'll interview ten people. When will we make a decision? We'll decide by the end of the month.`,
  8:  `Hello. My name is Patricia. I need to choose between two candidates. Ana has five years of experience. Her interview score was 85. Luis has three years of experience. His score was 78. Ana is more experienced than Luis. She is also a better communicator. Ana is a better match for this role.`,
  9:  `Good afternoon. My name is María. We interviewed six people. Her name is Sofia. She has the most experience. She worked in HR for eight years. Her interview was the best of the six. Her test score was the highest. She scored 94 out of 100. I recommend Sofia for this role.`,
  10: `Our process is faster now. We used to take four weeks. Now we take two weeks. We review CVs more quickly now. We also schedule interviews more efficiently. We respond to candidates more promptly now. Our new hires are performing more strongly than before.`,
  11: `Hi! I'm María. Welcome to the team. Have you worked in HR before? Yes, I have. I've worked in HR for four years. Have you used our software system? No, I haven't. Have you met the team yet? I've met two people so far. Carlos and Patricia. They seem very friendly.`,
  12: `Hi everyone. I'm Carlos. We've just hired three new people. They start next Monday. I've already sent them their contracts. They've already signed and returned them. I've also just posted two more jobs. I've already written the job descriptions. It's been a great week. Well done to the team!`,
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cors = { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: { ...cors, "Access-Control-Allow-Methods": "GET,POST", "Access-Control-Allow-Headers": "Content-Type" } });
    }

    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ status: "ok", worker: "hko-media" }), { headers: cors });
    }

    // GET /audio?n=1 — generate TTS audio for lesson n
    if (url.pathname === "/audio" && request.method === "GET") {
      const n = parseInt(url.searchParams.get("n")) || 1;
      const script = SCRIPTS[n];
      if (!script) return new Response("Not found", { status: 404 });

      // Check KV cache first
      const cached = await env.KV.get(`audio:a2:${n.toString().padStart(2,"0")}`, "arrayBuffer");
      if (cached) {
        return new Response(cached, { headers: { "Content-Type": "audio/mpeg", "Cache-Control": "public, max-age=86400", "Access-Control-Allow-Origin": "*" } });
      }

      // Generate with Workers AI TTS
      try {
        const resp = await env.AI.run("@cf/myshell-ai/melotts", {
          prompt: script,
          language: "en"
        });

        // Cache in KV
        const buf = await resp.arrayBuffer ? resp.arrayBuffer() : resp;
        await env.KV.put(`audio:a2:${n.toString().padStart(2,"0")}`, buf, { expirationTtl: 86400 * 30 });

        return new Response(buf, { headers: { "Content-Type": "audio/mpeg", "Cache-Control": "public, max-age=86400", "Access-Control-Allow-Origin": "*" } });
      } catch (e) {
        // Fallback: return script as JSON so browser TTS can use it
        return new Response(JSON.stringify({ fallback: true, script, error: e.message }), { headers: cors });
      }
    }

    // POST /audio — generate audio from custom text
    if (url.pathname === "/audio" && request.method === "POST") {
      const body = await request.json().catch(() => ({}));
      const text = body.text || SCRIPTS[body.lessonNumber || 1];

      try {
        const resp = await env.AI.run("@cf/myshell-ai/melotts", {
          prompt: text,
          language: "en"
        });
        const buf = await resp.arrayBuffer ? resp.arrayBuffer() : resp;
        return new Response(buf, { headers: { "Content-Type": "audio/mpeg", "Access-Control-Allow-Origin": "*" } });
      } catch (e) {
        return new Response(JSON.stringify({ fallback: true, script: text, error: e.message }), { headers: cors });
      }
    }

    // GET /image?n=1 — generate image for lesson n using Workers AI
    if (url.pathname === "/image" && request.method === "GET") {
      const n = parseInt(url.searchParams.get("n")) || 1;

      // Check KV cache
      const cached = await env.KV.get(`img:a2:${n.toString().padStart(2,"0")}`, "arrayBuffer");
      if (cached) {
        return new Response(cached, { headers: { "Content-Type": "image/png", "Cache-Control": "public, max-age=86400", "Access-Control-Allow-Origin": "*" } });
      }

      const prompts = {
        1:  "Latin American woman HR professional at modern Santiago office desk, reviewing documents, professional photography, warm lighting",
        2:  "Latin American male HR recruiter surprised at laptop screen, piles of CVs on desk, modern office, professional photography",
        3:  "Latin American woman presenting recruitment statistics at whiteboard, modern conference room, professional photography",
        4:  "Professional interview scene, Latin American man in interview, modern Santiago office, confident posture, professional photography",
        5:  "Latin American woman HR professional with weekly planner and sticky notes, organized desk, morning office light, professional photography",
        6:  "Latin American woman on phone call at modern office desk, taking notes, professional photography",
        7:  "Two HR professionals in discussion, modern Santiago office, professional photography, natural lighting",
        8:  "Latin American woman holding two CV folders side by side comparing them, modern office desk, professional photography",
        9:  "Latin American woman presenting to colleagues at boardroom, candidate profile on screen, professional photography",
        10: "Before and after comparison chart on office screen, two HR professionals looking at results, professional photography",
        11: "Two professionals in office break room with coffee cups, welcoming new employee, professional photography",
        12: "Latin American man presenting to small team, welcome packs on table, celebratory atmosphere, professional photography",
      };

      try {
        const resp = await env.AI.run("@cf/black-forest-labs/flux-1-schnell", {
          prompt: prompts[n] || prompts[1],
          num_steps: 8
        });

        const buf = resp instanceof ArrayBuffer ? resp : await resp.arrayBuffer();
        await env.KV.put(`img:a2:${n.toString().padStart(2,"0")}`, buf, { expirationTtl: 86400 * 30 });
        return new Response(buf, { headers: { "Content-Type": "image/png", "Cache-Control": "public, max-age=86400", "Access-Control-Allow-Origin": "*" } });
      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: cors });
      }
    }

    return new Response(JSON.stringify({
      worker: "hko-media",
      endpoints: [
        "GET  /health",
        "GET  /audio?n=1   (lessons 1-12, cached)",
        "POST /audio       {text: '...', lessonNumber: 1}",
        "GET  /image?n=1   (lessons 1-12, cached, Flux AI)"
      ]
    }), { headers: cors });
  }
};
