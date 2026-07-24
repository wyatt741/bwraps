/* B Printing and Wraps chat assistant — HYBRID:
   - free-text questions -> AI (Cloudflare Worker /chat, Claude Haiku, trained on the shop)
   - quote WIZARD -> deterministic (no AI); packages answers and POSTs to the Worker /lead
   Until WORKER_URL is set, it runs as a client-side DEMO (canned keyword answers + the wizard),
   so nothing breaks before the Worker is deployed. See worker/README.md to deploy + wire up. */
(function () {
  // ==== set this to your deployed Worker URL (no trailing slash) to turn on real AI ====
  var WORKER_URL = "";   // e.g. "https://bwraps-chat.yoursubdomain.workers.dev"
  // ====================================================================================

  var root = document.getElementById("cw");
  if (!root) return;
  var bubble = document.getElementById("cw-bubble"), panel = document.getElementById("cw-panel"),
      closeB = document.getElementById("cw-close"), log = document.getElementById("cw-log"),
      form = document.getElementById("cw-form"), input = document.getElementById("cw-input"),
      sendB = document.getElementById("cw-send"),
      nudge = document.getElementById("cw-nudge"), nudgeOpen = document.getElementById("cw-nudge-open"),
      nudgeX = document.getElementById("cw-nudge-x");

  var PHONE = "928-230-8525";
  var AI = !!WORKER_URL;                 // AI mode when a Worker URL is set, else demo mode
  var history = [];                      // {role, content} for the AI
  var transcript = [];                   // {role, text} full visible log -> emailed with a lead
  var mode = "chat", started = false, busy = false;
  var userTurns = 0, lastUserQ = "", offeredFollowup = false;   // drive the intent-based follow-up capture

  // ---------- helpers ----------
  function el(t, c, x) { var n = document.createElement(t); if (c) n.className = c; if (x != null) n.textContent = x; return n; }
  function scroll() { log.scrollTop = log.scrollHeight; }
  function setInput(on, ph) { input.disabled = !on; sendB.disabled = !on; input.placeholder = ph || "Type your message..."; }
  function linkify(box, text) {
    var re = /(https?:\/\/[^\s)]+)|(\d{3}-\d{3}-\d{4})/g, last = 0, m;
    while ((m = re.exec(text))) {
      if (m.index > last) box.appendChild(document.createTextNode(text.slice(last, m.index)));
      var a = document.createElement("a");
      if (m[1]) { a.href = m[1]; a.target = "_blank"; a.rel = "noopener"; a.textContent = m[1].replace(/^https?:\/\//, "").replace(/\/$/, ""); }
      else { a.href = "tel:+1" + m[2].replace(/\D/g, ""); a.textContent = m[2]; }
      box.appendChild(a); last = m.index + m[0].length;
    }
    if (last < text.length) box.appendChild(document.createTextNode(text.slice(last)));
  }
  function addMsg(role, text) { transcript.push({ role: role, text: text }); var d = el("div", "cw-msg cw-" + role); linkify(d, text); log.appendChild(d); scroll(); return d; }
  function transcriptText() { return transcript.map(function (m) { return (m.role === "user" ? "Visitor" : "Assistant") + ": " + m.text; }).join("\n"); }
  function typing() { var t = el("div", "cw-typing"); t.appendChild(el("span")); t.appendChild(el("span")); t.appendChild(el("span")); log.appendChild(t); scroll(); return t; }
  function botSay(text, then) { var t = typing(); setTimeout(function () { t.remove(); addMsg("bot", text); if (then) then(); }, 380); }
  function chips(items) {
    var wrap = el("div", "cw-chips");
    items.forEach(function (it) {
      var b = el("button", "cw-chip" + (it.ghost ? " cw-chip-ghost" : ""), it.label); b.type = "button";
      b.addEventListener("click", function () { wrap.remove(); it.act(); });
      wrap.appendChild(b);
    });
    log.appendChild(wrap); scroll(); return wrap;
  }

  // ---------- proactive nudge (once per session, after a delay) ----------
  function hideNudge(dismiss) { if (!nudge) return; nudge.hidden = true; if (dismiss) { try { sessionStorage.setItem("cw-nudge", "1"); } catch (e) {} } }
  function showNudge() {
    if (!nudge || started || !panel.hidden) return;
    try { if (sessionStorage.getItem("cw-nudge")) return; } catch (e) {}
    nudge.hidden = false;
  }
  if (nudge) {
    nudgeOpen.addEventListener("click", function () { hideNudge(true); open(); });
    nudgeX.addEventListener("click", function () { hideNudge(true); });
    setTimeout(showNudge, 20000);
  }

  // ---------- open / close ----------
  function open() {
    hideNudge(true);
    panel.hidden = false; bubble.setAttribute("aria-expanded", "true"); root.classList.add("cw--open");
    if (!started) { started = true; showMenu(); }
    setTimeout(function () { (input.disabled ? bubble : input).focus(); }, 60);
  }
  function close() { panel.hidden = true; bubble.setAttribute("aria-expanded", "false"); root.classList.remove("cw--open"); bubble.focus(); }
  bubble.addEventListener("click", function () { panel.hidden ? open() : close(); });
  closeB.addEventListener("click", close);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) close(); });

  // ---------- opening menu ----------
  function showMenu() {
    mode = "chat";
    addMsg("bot", "Hey! I'm the B Printing assistant. Ask me anything, or pick one:");
    chips([
      { label: "Get a quote", act: startWizard },
      { label: "Our services", act: function () { userMsg("What do you offer?"); route("what do you offer"); } },
      { label: "Hours & location", act: function () { userMsg("Where are you and when are you open?"); route("hours and location"); } }
    ]);
    setInput(true, "Or type your question...");
  }
  function userMsg(t) { addMsg("user", t); }

  // ---------- free-text: AI when configured, else canned ----------
  function route(text) {
    userTurns++; lastUserQ = text;
    if (AI) return sendChat(text);
    var res = answer(text);
    if (typeof res === "function") res(); else botSay(res, function () { maybeOfferFollowup(text); });
  }
  function sendChat(text) {
    history.push({ role: "user", content: text });
    busy = true; setInput(false, "..."); var t = typing();
    fetch(WORKER_URL + "/chat", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ messages: history }) })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        t.remove();
        var reply = (d && d.reply) ? d.reply : ("Sorry, I had trouble there. Call or text " + PHONE + ".");
        history.push({ role: "assistant", content: reply });
        addMsg("bot", reply);
      })
      .catch(function () { t.remove(); addMsg("bot", "Sorry, I couldn't connect. Please call or text " + PHONE + "."); })
      .finally(function () { busy = false; setInput(true, "Ask anything else..."); input.focus(); maybeOfferFollowup(text); });
  }

  // ---------- intent-based follow-up capture: offer once, after intent or a couple of turns ----------
  function maybeOfferFollowup(text) {
    if (offeredFollowup || mode !== "chat") return;
    var q = (text || "").toLowerCase();
    var intent = ["price", "cost", "how much", "pricing", "quote", "turnaround", "how long", "how fast",
                  "when can", "deadline", "rush", "estimate", "lead time"].some(function (w) { return q.indexOf(w) !== -1; });
    if (!(intent || userTurns >= 2)) return;
    offeredFollowup = true;
    setTimeout(offerFollowup, 700);
  }
  function offerFollowup() {
    if (mode !== "chat") return;
    botSay("Want the shop to follow up with you directly? I can pass along your question and our chat so Shar and the team can help.", function () {
      chips([
        { label: "Yes, please", act: startFollowup },
        { label: "No thanks", ghost: true, act: function () { botSay("No problem! Ask me anything else, or reach the shop anytime at " + PHONE + "."); } }
      ]);
    });
  }

  // ---------- canned fallback answers (demo mode only) ----------
  var ANSWERS = {
    services: "We do it all in house: embroidery (hats, polos, towels), custom apparel & DTF, printing & signs (banners, stickers, large format), and vehicle, trailer & wall wraps. Want a quote on any of it?",
    hours: "We're at 16551 N Dysart Rd #107, Surprise, AZ 85378. Open Mon-Fri 9am-5pm, closed weekends. Call or text " + PHONE + ".",
    price: "Pricing depends on the product, quantity, and artwork, so the fastest way is a quick quote. Want me to grab a few details? Or call/text " + PHONE + ".",
    contact: "Easiest ways to reach us: call or text " + PHONE + ", or the quote form on the site. Want me to start a quote here?",
    fallback: "Good question, the team can get you a precise answer. Want me to start a quick quote, or call/text " + PHONE + "."
  };
  function answer(text) {
    var q = text.toLowerCase(), has = function (a) { return a.some(function (w) { return q.indexOf(w) !== -1; }); };
    if (has(["quote", "estimate", "order", "get started"])) return startWizard;
    if (has(["price", "cost", "how much", "pricing", "$"])) return ANSWERS.price;
    if (has(["hour", "open", "where", "location", "address", "directions"])) return ANSWERS.hours;
    if (has(["embroider", "hat", "apparel", "dtf", "shirt", "print", "banner", "sticker", "sign", "wrap", "vehicle", "service", "offer"])) return ANSWERS.services;
    if (has(["contact", "call", "text", "phone", "email", "reach"])) return ANSWERS.contact;
    return ANSWERS.fallback;
  }

  // ---------- quote wizard (deterministic; never AI) ----------
  var STEPS = [
    { key: "service", q: "Let's build your quote! What do you need?", opts: ["Embroidery", "Apparel & DTF", "Printing & Signs", "Wraps", "Not sure yet"] },
    { key: "size",    q: "Roughly how many pieces (or how big a job)?", opts: ["Just 1-5", "6-24", "25-100", "100+ / not sure"] },
    { key: "details", q: "Tell me a bit about the project, colors, sizes, deadline, or skip.", text: true, optional: true },
    { key: "name",    q: "Now let's grab your contact info. What's your name?", text: true },
    { key: "email",   q: "Best email for your quote?", text: true, email: true },
    { key: "phone",   q: "A phone number in case we need it? Optional, type or skip.", text: true, optional: true }
  ];
  var answers = {}, step = 0, skipWrap = null;
  function startWizard() { mode = "wizard"; answers = {}; step = 0; addMsg("user", "I'd like a quote"); botSay(STEPS[0].q, renderStep); }
  function runStep() { if (step >= STEPS.length) return submitQuote(); botSay(STEPS[step].q, renderStep); }
  function renderStep() {
    var s = STEPS[step];
    if (s.opts) {
      setInput(false, "Pick an option above");
      chips(s.opts.map(function (o) { return { label: o, act: function () { addMsg("user", o); answers[s.key] = o; step++; runStep(); } }; }));
    } else {
      setInput(true, s.optional ? "Type, or click Skip" : "Type your answer...");
      skipWrap = s.optional ? chips([{ label: "Skip", ghost: true, act: function () { skipWrap = null; answers[s.key] = ""; step++; runStep(); } }]) : null;
      input.focus();
    }
  }
  function wizardText(text) {
    var s = STEPS[step];
    if (s.email && !/.+@.+\..+/.test(text)) { addMsg("bot", "Hmm, that doesn't look like an email. Mind trying again?"); input.focus(); return; }
    if (skipWrap) { skipWrap.remove(); skipWrap = null; }
    addMsg("user", text); answers[s.key] = text; step++; runStep();
  }
  function submitQuote() {
    mode = "chat";
    if (!AI) {   // demo mode: no backend to send to
      botSay("Perfect, that's everything, thanks " + (answers.name || "") + "!", function () {
        botSay("In the live site this sends straight to the shop. For now, call or text " + PHONE + " and mention your " + (answers.service || "project") + " and we'll get you a quote fast.", function () { setInput(true, "Ask anything else..."); });
      });
      return;
    }
    setInput(false, "Sending..."); var t = typing();
    var payload = Object.assign({}, answers, { source: "AI chat widget quote wizard", transcript: transcriptText() });
    fetch(WORKER_URL + "/lead", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        t.remove();
        if (d && d.ok) addMsg("bot", "Perfect, that's everything, thanks " + (answers.name || "") + "! We'll put together a quote and get back to you soon. Need it faster? Call or text " + PHONE + ".");
        else addMsg("bot", "I couldn't send that just now. Please call or text " + PHONE + " and we'll sort your quote.");
      })
      .catch(function () { t.remove(); addMsg("bot", "I couldn't connect to send that. Please call or text " + PHONE + "."); })
      .finally(function () { setInput(true, "Ask anything else..."); });
  }

  // ---------- follow-up capture (from free-text chat; name + email/phone -> emailed to owner with transcript) ----------
  var FUP_STEPS = [
    { key: "name", q: "Awesome. What's your name?", text: true },
    { key: "contact", q: "And the best way to reach you, an email or phone number?", text: true, contact: true }
  ];
  var fanswers = {}, fstep = 0;
  function startFollowup() { mode = "followup"; fanswers = {}; fstep = 0; addMsg("user", "Yes, please follow up"); botSay(FUP_STEPS[0].q, renderFStep); }
  function runFStep() { if (fstep >= FUP_STEPS.length) return submitFollowup(); botSay(FUP_STEPS[fstep].q, renderFStep); }
  function renderFStep() { setInput(true, FUP_STEPS[fstep].contact ? "Email or phone..." : "Type your answer..."); input.focus(); }
  function followupText(text) {
    var s = FUP_STEPS[fstep];
    if (s.contact) {
      var hasEmail = /.+@.+\..+/.test(text), hasPhone = text.replace(/\D/g, "").length >= 7;
      if (!hasEmail && !hasPhone) { addMsg("bot", "Hmm, that doesn't look like an email or phone number. Mind trying again?"); input.focus(); return; }
    }
    addMsg("user", text); fanswers[s.key] = text; fstep++; runFStep();
  }
  function submitFollowup() {
    mode = "chat";
    var contact = fanswers.contact || "", isEmail = /.+@.+\..+/.test(contact);
    if (!AI) {   // demo mode: no backend to send to
      botSay("Perfect, thanks " + (fanswers.name || "") + "! On the live site this goes straight to the shop along with our chat, so they can follow up. For now, call or text " + PHONE + ".", function () { setInput(true, "Ask anything else..."); });
      return;
    }
    setInput(false, "Sending..."); var t = typing();
    var payload = { name: fanswers.name || "", email: isEmail ? contact : "", phone: isEmail ? "" : contact,
      details: lastUserQ || "(asked in chat)", source: "AI chat widget follow-up request", transcript: transcriptText() };
    fetch(WORKER_URL + "/lead", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        t.remove();
        if (d && d.ok) addMsg("bot", "Perfect, thanks " + (fanswers.name || "") + "! I've passed this to the shop and they'll reach out. Need it faster? Call or text " + PHONE + ".");
        else addMsg("bot", "I couldn't send that just now. Please call or text " + PHONE + ".");
      })
      .catch(function () { t.remove(); addMsg("bot", "I couldn't connect to send that. Please call or text " + PHONE + "."); })
      .finally(function () { setInput(true, "Ask anything else..."); });
  }

  // ---------- input routing ----------
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var text = input.value.trim(); if (!text || busy) return; input.value = "";
    if (mode === "wizard" && STEPS[step] && STEPS[step].text) { wizardText(text); return; }
    if (mode === "followup" && FUP_STEPS[fstep] && FUP_STEPS[fstep].text) { followupText(text); return; }
    mode = "chat"; userMsg(text); route(text);
  });
})();
