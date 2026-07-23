#!/usr/bin/env python3
"""B Printing and Wraps - static site generator.
Run:  py build.py    (emits index/services/gallery/about/contact + sitemap/robots)
Edit CONTENT here, never hand-edit the generated HTML. Deploy = git push.
Learned from the anderson-it engine: one generator, cache-busted assets, real
content only (no fabricated reviews/stats), FormSubmit contact, motion layer.
"""
import html

# ---- cache-busting (bump on any css/js change) ----
CSSV = "styles.css?v=1"
JSV  = "app.js?v=1"

# ---- business facts (from bwraps1.com, 2026-07-23) ----
BIZ      = "B Printing and Wraps"
TAG      = "Surprise's creative print, wrap & embroidery shop"
CITY     = "Surprise, Arizona"
PHONE    = "928-230-8525"
PHONE_TEL= "+19282308525"
EMAIL    = "hello@bwraps1.com"   # PLACEHOLDER - owner to confirm the real inbox for the form
DOMAIN   = "bwraps1.com"
TIKTOK   = "https://www.tiktok.com/@bwraps1"  # PLACEHOLDER handle - confirm

NAV = [("index.html","Home"),("services.html","Services"),("gallery.html","Gallery"),
       ("about.html","About"),("contact.html","Contact")]

# ============================ SHARED CHROME ============================
def head(title, desc, page=""):
    return f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{CSSV}">
</head><body class="{page}">'''

def nav(active):
    links = "".join(
        f'<a href="{h}"{" class=\"active\"" if h==active else ""}>{t}</a>'
        for h,t in NAV)
    mlinks = "".join(f'<a href="{h}">{t}</a>' for h,t in NAV)
    return f'''<header class="nav"><div class="wrap nav-in">
  <a class="brand" href="index.html"><span class="brand-b">B</span><span class="brand-t">Printing&nbsp;&amp;&nbsp;Wraps</span></a>
  <nav class="nav-links">{links}<a class="btn btn-primary" href="contact.html">Get a quote</a></nav>
  <button class="burger" aria-label="Menu"><span></span><span></span><span></span></button>
</div>
<div class="mobile-menu" id="mobile-menu">{mlinks}<a class="btn btn-primary" href="contact.html">Get a quote</a></div>
</header>'''

def cta():
    return f'''<section class="cta-band"><div class="wrap cta-in">
  <h2>Got a project? Let's make it loud.</h2>
  <p>Tell us what you need printed, wrapped, or stitched. We'll get you a quote fast.</p>
  <div class="cta-btns"><a class="btn btn-primary btn-lg" href="contact.html">Get a free quote</a>
  <a class="btn btn-ghost btn-lg" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
</div></section>'''

def footer():
    cols = "".join(f'<a href="{h}">{t}</a>' for h,t in NAV)
    return f'''<footer><div class="wrap foot-grid">
  <div class="foot-brand">
    <a class="brand" href="index.html"><span class="brand-b">B</span><span class="brand-t">Printing&nbsp;&amp;&nbsp;Wraps</span></a>
    <p>Custom printing, wraps, and embroidery in {CITY}. Local, fast, and a little bit loud.</p>
  </div>
  <div class="foot-col"><h5>Explore</h5>{cols}</div>
  <div class="foot-col"><h5>Contact</h5>
    <a href="tel:{PHONE_TEL}">{PHONE}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <a href="{TIKTOK}" target="_blank" rel="noopener">TikTok</a>
    <span class="foot-note">Surprise, Arizona</span>
  </div>
</div>
<div class="legal wrap"><span>&copy; 2026 {BIZ}. All rights reserved.</span></div>
</footer>
<script src="{JSV}"></script></body></html>'''

# ============================ CONTENT DATA ============================
# services: (id, kicker-emoji, title, blurb, [bullets])
SERVICES = [
 ("embroidery","🧵","Embroidery",
  "Hats, apparel, monogram towels & robes. As they say around here, the stitchin' is bitchin'.",
  ["Custom hats & beanies","Company polos & workwear","Monogram towels & robes","Sports team & spirit wear"]),
 ("apparel","👕","Custom Apparel & DTF",
  "Screen print, direct-to-film, and heat press. Turn your crew into walking billboards.",
  ["Screen printing","Direct-to-film (DTF) transfers","Wholesale gang sheets","Heat-press & one-offs"]),
 ("printing","🖨️","Printing & Signs",
  "Banners, signage, stickers, business collateral. If it can be printed, we print it.",
  ["Banners & yard signs","Stickers & decals","Business cards & flyers","Posters & large format"]),
 ("wraps","🚗","Vehicle & Wall Wraps",
  "Vehicles, walls, and vending machines turned into rolling (and standing) billboards.",
  ["Full & partial vehicle wraps","Wall & window graphics","Vending machine wraps","Fleet branding"]),
]

# gallery placeholder tiles: (category, label). Real photos swap in later.
GALLERY = [
 ("embroidery","Embroidered caps"),("wraps","Box truck wrap"),("apparel","DTF tees"),
 ("printing","Event banner"),("embroidery","Monogram robes"),("apparel","Screen-print run"),
 ("wraps","Wall mural wrap"),("printing","Die-cut stickers"),("wraps","Vending wrap"),
 ("apparel","Team hoodies"),("printing","Yard signs"),("embroidery","Company polos"),
]
GCATS = [("all","Everything"),("embroidery","Embroidery"),("apparel","Apparel & DTF"),
         ("printing","Printing"),("wraps","Wraps")]

# testimonials: SAMPLE layout only - replace with the shop's REAL reviews before launch.
TESTIMONIALS = [
 ("Sample review","Local business owner","We'll drop your real customer reviews in here. This card just shows the layout and styling."),
 ("Sample review","Repeat customer","Pull 2-3 of your best testimonials from the current site or Google and we'll feature them."),
 ("Sample review","Team apparel client","Real names, real quotes. No made-up reviews - that's the rule."),
]

def tile(cat, label, big=False):
    return f'<figure class="tile tile-{cat}{" tile-big" if big else ""}" data-cat="{cat}"><span class="tile-label">{label}</span><span class="tile-swap">photo</span></figure>'

# ============================ PAGES ============================
def home():
    svc = "".join(
        f'''<a class="svc svc-{s[0]}" href="services.html#{s[0]}">
        <span class="svc-emoji">{s[1]}</span><h3>{s[2]}</h3><p>{s[3]}</p>
        <span class="svc-more">See more &rarr;</span></a>''' for s in SERVICES)
    teaser = "".join(tile(c,l) for c,l in GALLERY[:6])
    tst = "".join(f'<blockquote class="tst reveal"><p>&ldquo;{q}&rdquo;</p><cite>{n}<span>{r}</span></cite></blockquote>'
                  for n,r,q in TESTIMONIALS)
    return head(f"{BIZ} | {TAG}", f"Custom printing, wraps, and embroidery in {CITY}. Get a fast, free quote from a local shop that does it all.","home") + nav("index.html") + f'''
<section class="hero"><div class="wrap hero-in">
  <div class="hero-copy reveal">
    <span class="eyebrow">Print &middot; Wrap &middot; Embroider</span>
    <h1>Make your brand <span class="hl hl-1">loud</span>,<br><span class="hl hl-2">local</span>, and impossible to miss.</h1>
    <p>{BIZ} is your creative print partner in {CITY}. Embroidery, custom apparel, signs, and wraps, all under one roof and out the door fast.</p>
    <div class="hero-btns"><a class="btn btn-primary btn-lg" href="contact.html">Get a free quote</a>
    <a class="btn btn-ghost btn-lg" href="gallery.html">See our work</a></div>
    <div class="hero-strip"><span>🧵 Embroidery</span><span>👕 Apparel &amp; DTF</span><span>🖨️ Printing</span><span>🚗 Wraps</span></div>
  </div>
  <div class="hero-art reveal d1">{tile("embroidery","Your work here",True)}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">What we do</span>
    <h2>One shop for everything custom</h2>
    <p>From a single embroidered cap to a full fleet wrap, we handle it in house.</p></div>
  <div class="svc-grid">{svc}</div>
</div></section>

<section class="section band"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Recent work</span><h2>A little taste of the shop</h2></div>
  <div class="gal-grid gal-teaser">{teaser}</div>
  <div class="center"><a class="btn btn-dark btn-lg" href="gallery.html">View the full gallery &rarr;</a></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">Why B</span><h2>Local shop, big-league output</h2></div>
  <div class="feat-grid">
    <div class="feat reveal"><span class="feat-ic">📍</span><h3>Right here in Surprise</h3><p>A real local shop you can walk into, not an online middleman.</p></div>
    <div class="feat reveal"><span class="feat-ic">⚡</span><h3>Fast turnarounds</h3><p>We move quick so you hit your event, launch, or deadline.</p></div>
    <div class="feat reveal"><span class="feat-ic">🎨</span><h3>Everything in house</h3><p>Print, wrap, and stitch under one roof, so your branding stays consistent.</p></div>
    <div class="feat reveal"><span class="feat-ic">🤝</span><h3>Small-batch friendly</h3><p>One hat or a thousand shirts, we treat every order like it matters.</p></div>
  </div>
</div></section>

<section class="section band"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">Kind words</span><h2>What customers say</h2>
    <p class="sample-note">Sample layout - we'll swap in your real reviews.</p></div>
  <div class="tst-grid">{tst}</div>
</div></section>
{cta()}{footer()}'''

def services():
    secs = ""
    for i,(sid,emo,title,blurb,bullets) in enumerate(SERVICES):
        bl = "".join(f"<li>{b}</li>" for b in bullets)
        art = tile(sid, title)
        flip = " svc-row-flip" if i%2 else ""
        secs += f'''<section class="section svc-row{flip}" id="{sid}"><div class="wrap svc-row-in">
        <div class="svc-row-art reveal">{art}</div>
        <div class="svc-row-copy reveal"><span class="svc-emoji">{emo}</span><h2>{title}</h2>
        <p>{blurb}</p><ul class="ticks">{bl}</ul>
        <a class="btn btn-primary" href="contact.html">Quote this &rarr;</a></div>
      </div></section>'''
    return head(f"Services | {BIZ}", f"Embroidery, custom apparel, DTF, printing, signs, and wraps in {CITY}.","services") + nav("services.html") + f'''
<section class="page-hero"><div class="wrap reveal">
  <span class="eyebrow">Services</span><h1>Everything we make</h1>
  <p>Four lines, one shop. Mix and match to brand your whole business.</p>
</div></section>
{secs}{cta()}{footer()}'''

def gallery():
    filt = "".join(f'<button class="gfilter{" active" if c=="all" else ""}" data-cat="{c}">{t}</button>' for c,t in GCATS)
    tiles = "".join(tile(c,l) for c,l in GALLERY)
    return head(f"Gallery | {BIZ}", f"See real embroidery, apparel, printing, and wrap work from {BIZ} in {CITY}.","gallery") + nav("gallery.html") + f'''
<section class="page-hero"><div class="wrap reveal">
  <span class="eyebrow">Gallery</span><h1>See the work</h1>
  <p>A sample of what leaves the shop. Real photos drop in here.</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="gfilters reveal">{filt}</div>
  <div class="gal-grid" id="gal">{tiles}</div>
</div></section>
{cta()}{footer()}'''

def about():
    fame = "".join(f'<span class="fame-chip">{n}</span>' for n in
        ["Restaurants","Cafes","Gyms & wellness","Auto shops","Real estate","Food trucks","Schools","Non-profits"])
    return head(f"About | {BIZ}", f"{BIZ} is a local print, wrap, and embroidery shop in {CITY}. Meet the team behind the work.","about") + nav("about.html") + f'''
<section class="page-hero"><div class="wrap reveal">
  <span class="eyebrow">About</span><h1>Your neighbors with a print shop</h1>
</div></section>
<section class="section"><div class="wrap about-in">
  <div class="about-copy reveal">
    <p class="lead">{BIZ} started with a simple idea: give {CITY} a creative shop that can print it, wrap it, and stitch it, without sending you to three different vendors.</p>
    <p>We're a local team that treats a one-off gift with the same care as a full fleet wrap. Whether you're a food truck needing a fresh look, a gym motivating members with a wall wrap, or a team that wants spirit wear with actual spirit, we've got you.</p>
    <p>Everything happens in house, so your branding stays consistent and your timeline stays short.</p>
  </div>
  <div class="about-art reveal d1">{tile("wraps","The shop")}</div>
</div></section>
<section class="section band"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">Wall of Fame</span><h2>Proud to work with local</h2>
    <p>We serve a whole range of businesses around Surprise:</p></div>
  <div class="fame reveal">{fame}</div>
</div></section>
{cta()}{footer()}'''

def contact():
    return head(f"Contact | {BIZ}", f"Get a free quote from {BIZ} in {CITY}. Call {PHONE} or send us your project.","contact") + nav("contact.html") + f'''
<section class="page-hero"><div class="wrap reveal">
  <span class="eyebrow">Contact</span><h1>Let's get you a quote</h1>
  <p>Tell us what you need. Attach your art or logo if you've got it, and we'll take it from there.</p>
</div></section>
<section class="section"><div class="wrap contact-in">
  <form class="cform reveal" action="https://formsubmit.co/{EMAIL}" method="POST" enctype="multipart/form-data">
    <input type="hidden" name="_subject" value="New quote request from the website">
    <input type="hidden" name="_template" value="table">
    <div class="f-row"><label>Name<input name="name" required></label>
    <label>Phone<input name="phone" type="tel"></label></div>
    <label>Email<input name="email" type="email" required></label>
    <label>What do you need?
      <select name="service"><option value="">Pick one</option>
      <option>Embroidery</option><option>Custom apparel / DTF</option>
      <option>Printing / signs</option><option>Vehicle or wall wrap</option><option>Not sure yet</option></select></label>
    <label>Your art or logo (optional)<input name="attachment" type="file"></label>
    <label>Project details<textarea name="message" rows="5" placeholder="Sizes, quantities, colors, deadline..."></textarea></label>
    <button class="btn btn-primary btn-lg" type="submit">Send it &rarr;</button>
    <p class="form-fine">Prefer to talk? Call or text {PHONE}.</p>
  </form>
  <aside class="contact-side reveal d1">
    <div class="cside-card"><h3>Call or text</h3><a class="big-phone" href="tel:{PHONE_TEL}">{PHONE}</a></div>
    <div class="cside-card"><h3>Email</h3><a href="mailto:{EMAIL}">{EMAIL}</a></div>
    <div class="cside-card"><h3>Where</h3><p>{CITY}<br>Serving the West Valley</p></div>
    <div class="cside-card"><h3>Follow</h3><a href="{TIKTOK}" target="_blank" rel="noopener">TikTok &rarr;</a></div>
  </aside>
</div></section>
{footer()}'''

# ============================ BUILD ============================
PAGES = {"index.html":home,"services.html":services,"gallery.html":gallery,
         "about.html":about,"contact.html":contact}

def sitemap():
    urls = "".join(f"<url><loc>https://{DOMAIN}/{p}</loc></url>" for p in PAGES)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'

def build():
    for fn, f in PAGES.items():
        with open(fn,"w",encoding="utf-8") as fh: fh.write(f())
    with open("sitemap.xml","w",encoding="utf-8") as fh: fh.write(sitemap())
    with open("robots.txt","w",encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    print("built:", ", ".join(PAGES), "+ sitemap.xml, robots.txt")

if __name__ == "__main__":
    build()
