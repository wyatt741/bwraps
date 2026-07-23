/* B Printing and Wraps - demo chat assistant. Runs 100% client-side:
   - guided quote wizard (deterministic, packages the answers)
   - canned keyword answers for free-text questions (no AI, no backend, no cost)
   To make quotes actually send in production, POST `answers` to a FormSubmit/
   Worker endpoint in submitQuote() (one fetch) - marked below. */
(function () {
  var root = document.getElementById("cw");
  if (!root) return;

  var bubble = document.getElementById("cw-bubble");
  var panel  = document.getElementById("cw-panel");
  var closeB = document.getElementById("cw-close");
  var log    = document.getElementById("cw-log");
  var form   = document.getElementById("cw-form");
  var input  = document.getElementById("cw-input");
  var sendB  = document.getElementById("cw-send");

  var PHONE = "928-230-8525";
  var mode = "chat", started = false, busy = false;

  // ---------- helpers ----------
  function el(t, c, x) { var n = document.createElement(t); if (c) n.className = c; if (x != null) n.textContent = x; return n; }
  function scroll() { log.scrollTop = log.scrollHeight; }
  function setInput(on, ph) { input.disabled = !on; sendB.disabled = !on; input.placeholder = ph || "Type your message..."; }

  // safe linkify: URLs -> <a>, phone -> tel: (no innerHTML)
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
  function addMsg(role, text) { var d = el("div", "cw-msg cw-" + role); linkify(d, text); log.appendChild(d); scroll(); return d; }
  function typing() { var t = el("div", "cw-typing"); t.appendChild(el("span")); t.appendChild(el("span")); t.appendChild(el("span")); log.appendChild(t); scroll(); return t; }
  function botSay(text, then) { var t = typing(); setTimeout(function () { t.remove(); addMsg("bot", text); if (then) then(); }, 420); }
  function chips(items) {
    var wrap = el("div", "cw-chips");
    items.forEach(function (it) {
      var b = el("button", "cw-chip" + (it.ghost ? " cw-chip-ghost" : ""), it.label);
      b.type = "button";
      b.addEventListener("click", function () { wrap.remove(); it.act(); });
      wrap.appendChild(b);
    });
    log.appendChild(wrap); scroll(); return wrap;
  }

  // ---------- open / close ----------
  function open() {
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
    addMsg("bot", "Hey! 👋 I'm the B Printing assistant. What can I help you with?");
    chips([
      { label: "💬 Get a quote", act: startWizard },
      { label: "🧵 Our services", act: function () { addMsg("user", "What do you offer?"); botSay(ANSWERS.services); } },
      { label: "🕒 Hours & location", act: function () { addMsg("user", "Where are you?"); botSay(ANSWERS.hours); } },
    ]);
    setInput(true, "Or type your question...");
  }

  // ---------- canned answers (keyword router) ----------
  var ANSWERS = {
    services: "We do it all in house: embroidery (hats, polos, towels), custom apparel & DTF, printing & signs (banners, stickers, large format), and vehicle, trailer & wall wraps. Want a quote on any of it?",
    hours: "We're at 16551 N Dysart Rd #107, Surprise, AZ 85378. Open Mon-Fri 9am-5pm, closed weekends. Call or text " + PHONE + ".",
    embroidery: "Embroidery is our featured service, the stitchin' is bitchin'! Hats, company polos, workwear, monogram towels & robes, team spirit wear. Want a quote?",
    apparel: "Custom apparel & DTF: screen printing, direct-to-film transfers, wholesale gang sheets, and heat-press one-offs. How many pieces are you thinking?",
    printing: "Printing & signs: banners, yard signs, stickers, decals, business cards, flyers, and large format. What are you printing?",
    wraps: "Wraps are a specialty, vehicles, trailers, fleets, walls, windows, and even vending machines. What are we wrapping?",
    price: "Pricing depends on the product, quantity, and artwork, so the fastest way is a quick quote. Want me to grab a few details? Or call/text " + PHONE + ".",
    turnaround: "Turnaround depends on the job, but we move fast and can often handle rush orders, one customer needed 3 shirts done in a day and we made it happen. Want a quote?",
    contact: "Easiest ways to reach us: call or text " + PHONE + ", or use the quote form on the site. Want me to start a quote here?",
    thanks: "Anytime! Want me to start a quick quote, or is there anything else?",
    fallback: "Good question, the team can get you a precise answer. Want me to start a quick quote, or you can call/text " + PHONE + "."
  };
  function answer(text) {
    var q = text.toLowerCase();
    var has = function (arr) { return arr.some(function (w) { return q.indexOf(w) !== -1; }); };
    if (has(["quote", "estimate", "order", "get started"])) return startWizard;
    if (has(["price", "cost", "how much", "pricing", "$"])) return ANSWERS.price;
    if (has(["hour", "open", "where", "location", "address", "directions"])) return ANSWERS.hours;
    if (has(["embroider", "hat", "stitch", "polo", "towel", "monogram"])) return ANSWERS.embroidery;
    if (has(["shirt", "apparel", "dtf", "screen print", "tee", "t-shirt", "hoodie"])) return ANSWERS.apparel;
    if (has(["banner", "sign", "sticker", "decal", "flyer", "print", "card"])) return ANSWERS.printing;
    if (has(["wrap", "vehicle", "truck", "trailer", "van", "car", "window", "vending", "wall"])) return ANSWERS.wraps;
    if (has(["how long", "turnaround", "rush", "fast", "when"])) return ANSWERS.turnaround;
    if (has(["contact", "call", "text", "phone", "email", "reach"])) return ANSWERS.contact;
    if (has(["service", "offer", "do you", "what do"])) return ANSWERS.services;
    if (has(["thank", "thanks", "great", "awesome", "perfect"])) return ANSWERS.thanks;
    return ANSWERS.fallback;
  }

  // ---------- quote wizard (deterministic) ----------
  var STEPS = [
    { key: "service", q: "Let's build your quote! What do you need?", opts: ["Embroidery", "Apparel & DTF", "Printing & Signs", "Wraps", "Not sure yet"] },
    { key: "qty",     q: "Roughly how many pieces (or how big a job)?", opts: ["Just 1-5", "6-24", "25-100", "100+ / not sure"] },
    { key: "details", q: "Tell me a bit about the project, colors, sizes, deadline, or skip.", text: true, optional: true },
    { key: "name",    q: "Great. What's your name?", text: true },
    { key: "contact", q: "Best phone or email for your quote?", text: true }
  ];
  var answers = {}, step = 0, skipWrap = null;

  function startWizard() {
    mode = "wizard"; answers = {}; step = 0;
    addMsg("user", "I'd like a quote");
    botSay(STEPS[0].q, function () { renderStep(); });
  }
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
    if (skipWrap) { skipWrap.remove(); skipWrap = null; }
    addMsg("user", text); answers[STEPS[step].key] = text; step++; runStep();
  }
  function submitQuote() {
    mode = "chat";
    // PRODUCTION: send the lead, e.g.
    //   fetch("https://formsubmit.co/ajax/elitecustomprinting@outlook.com", {method:"POST",
    //     headers:{'content-type':'application/json'}, body: JSON.stringify(answers)});
    botSay("Perfect, that's everything I need, thanks " + (answers.name || "") + "! 🎉", function () {
      botSay("In the live site this sends straight to the shop. For now, call or text " + PHONE + " and mention your " + (answers.service || "project") + " and we'll get you a quote fast.", function () {
        setInput(true, "Ask anything else...");
      });
    });
  }

  // ---------- input routing ----------
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var text = input.value.trim();
    if (!text || busy) return;
    input.value = "";
    if (mode === "wizard" && STEPS[step] && STEPS[step].text) { wizardText(text); return; }
    addMsg("user", text);
    var res = answer(text);
    if (typeof res === "function") { res(); } else { botSay(res); }
  });
})();
