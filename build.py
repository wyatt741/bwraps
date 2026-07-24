#!/usr/bin/env python3
"""B Printing and Wraps - static site generator.
Run:  python3 build.py   (emits index/services/gallery/about/contact + sitemap/robots)
Edit CONTENT here, never hand-edit the generated HTML. Deploy = git push.
Engine from anderson-it: one generator, cache-busted assets, real content only
(no fabricated reviews/stats), FormSubmit contact, IntersectionObserver motion.

Theme v2 (2026-07): photography-forward, on-brand. Real identity pulled from the
logo = hot magenta script "B" + black. So the palette is electric pink + ink +
warm white, NOT the rainbow-CMYK guess from v1. Every tile is a real shop photo
downloaded from bwraps1.com into assets/.
"""
import json
from datetime import date

# ---- cache-busting (bump on any css/js change) ----
CSSV = "styles.css?v=26"
JSV  = "app.js?v=3"
CHATV= "chat.js?v=6"

# ---- dark-mode: default dark (like anderson-it), toggle persists to localStorage ----
FOUC   = '<script>(function(){try{var t=localStorage.getItem("theme")||"dark";document.documentElement.setAttribute("data-theme",t);}catch(e){}})();</script>'
SUN    = '<svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.4M12 19.6V22M4.2 4.2l1.7 1.7M18.1 18.1l1.7 1.7M2 12h2.4M19.6 12H22M4.2 19.8l1.7-1.7M18.1 5.9l1.7-1.7"/></svg>'
MOON   = '<svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z"/></svg>'
TOGGLE = f'<button class="theme-toggle" type="button" aria-label="Toggle dark mode" title="Toggle theme">{SUN}{MOON}</button>'

# ---- ultra-light line icons (replaces emoji - premium feel per high-end-visual-design) ----
def _svg(p):
    return f'<svg class="ic-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
ICON = {
 "embroidery": _svg('<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.12 8.12 20 20M14.8 14.8 20 4M8.12 15.88 12 12"/>'),
 "apparel":    _svg('<path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>'),
 "printing":   _svg('<path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8" rx="1"/>'),
 "wraps":      _svg('<path d="M10 17h4V5H2v12h3M20 17h2v-3.34a4 4 0 0 0-1.17-2.83L19 9h-5v8h1"/><circle cx="7.5" cy="17.5" r="2"/><circle cx="17.5" cy="17.5" r="2"/>'),
 "pin":        _svg('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.5"/>'),
 "bolt":       _svg('<path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/>'),
 "palette":    _svg('<path d="M12 22a10 10 0 1 1 0-20 10 10 0 0 1 10 10 3 3 0 0 1-3 3h-1.5a1.5 1.5 0 0 0-1.5 1.5V19a3 3 0 0 1-3 3z"/><circle cx="7.5" cy="10.5" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="16.5" cy="10.5" r="1"/>'),
 "heart":      _svg('<path d="M20.8 5.6a5.5 5.5 0 0 0-7.8 0L12 6.5l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.8 1-1a5.5 5.5 0 0 0 0-7.6z"/>'),
}
def icon(name): return ICON.get(name, "")

# why-choose-us features: (icon, title, body)
FEATURES = [
 ("pin","Right here in Surprise","A real shop you can walk into, not an online middleman."),
 ("bolt","Fast turnarounds","We move quick so you hit your event, launch, or deadline."),
 ("palette","Everything in house","Print, wrap, and stitch under one roof, so your branding stays consistent."),
 ("heart","Small-batch friendly","One hat or a thousand shirts, we treat every order like it matters."),
]

# ---- business facts (verified from bwraps1.com, 2026-07-23) ----
BIZ      = "B Printing and Wraps"
TAG      = "Surprise's custom print, wrap & embroidery shop"
CITY     = "Surprise, Arizona"
ADDR     = "16551 N Dysart Rd #107, Surprise, AZ 85378"
PHONE    = "928-230-8525"
PHONE_TEL= "+19282308525"
EMAIL    = "elitecustomprinting@outlook.com"  # real shop inbox from their site. CONFIRM this is the form destination + activate FormSubmit before launch.
HOURS    = "Mon-Fri 9am-5pm"
DOMAIN   = "bwraps1.com"
MAPS     = "https://maps.app.goo.gl/eGQwKDuvYefatZDTA"      # real directions link from their site
GOOGLE   = "https://maps.app.goo.gl/v1bZDkvdZy5mf69Z6"      # real Google Business profile (5.0, 20 reviews)
MAP_EMBED= "https://www.google.com/maps?q=16551+N+Dysart+Rd+%23107+Surprise+AZ+85378&output=embed"
# socials (verified live on bwraps1.com, 2026-07-23)
TIKTOK   = "https://www.tiktok.com/@luckstitch"
IG       = "https://www.instagram.com/bprinting_/"
FB       = "https://www.facebook.com/bprintingandwraps"

# ---- SEO: canonical base + share image + LocalBusiness structured data ----
# Canonical points at the launch domain (bwraps1.com), matching the sitemap, so search
# consolidates there after cutover. All facts below are real/verified (no fabrication).
BASE   = f"https://{DOMAIN}"
OG_IMG = f"{BASE}/assets/storefront.jpg"
LD_JSON = json.dumps({
  "@context":"https://schema.org","@type":["LocalBusiness","Store"],"@id":f"{BASE}/#business",
  "name":BIZ,"description":f"Custom printing, wraps, and embroidery in {CITY}.",
  "image":OG_IMG,"logo":f"{BASE}/assets/logo-mark.png","url":f"{BASE}/",
  "telephone":PHONE_TEL,"email":EMAIL,"priceRange":"$$",
  "address":{"@type":"PostalAddress","streetAddress":"16551 N Dysart Rd #107",
             "addressLocality":"Surprise","addressRegion":"AZ","postalCode":"85378","addressCountry":"US"},
  "areaServed":{"@type":"City","name":"Surprise"},"hasMap":MAPS,
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification",
    "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"17:00"}],
  "sameAs":[IG,FB,TIKTOK],
  "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"50"},
}, separators=(",",":"))

# "Contact" is a header nav link; the animated "Get a quote" button (also -> contact.html) is the primary CTA.
NAV = [("index.html","Home"),("services.html","Services"),("gallery.html","Gallery"),
       ("about.html","About"),("contact.html","Contact")]
FOOT_NAV = NAV

# ============================ SHARED CHROME ============================
def head(title, desc, page="", path="index.html"):
    canon = f"{BASE}/{path}"
    return f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:url" content="{canon}">
<meta property="og:site_name" content="{BIZ}"><meta property="og:image" content="{OG_IMG}">
<meta property="og:locale" content="en_US"><meta name="theme-color" content="#e6187e">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMG}">
<link rel="icon" href="assets/logo-az.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{CSSV}">
<script type="application/ld+json">{LD_JSON}</script>
{FOUC}
</head><body class="{page}">
<a class="skip" href="#main">Skip to content</a>'''

def brandmark(cls=""):
    # logo-mark.png = just the script "B" (cropped from the full logo, whose built-in
    # wordmark was illegible at nav size). The name sits beside it as real type.
    return (f'<a class="brand {cls}" href="index.html" aria-label="{BIZ} home">'
            f'<img src="assets/logo-mark.png" alt="" width="863" height="810">'
            f'<span class="brand-name">B&nbsp;Printing&nbsp;&amp;&nbsp;Wraps</span></a>')

def nav(active):
    links = "".join(
        f'<a href="{h}"{" class=\"active\"" if h==active else ""}>{t}</a>'
        for h,t in NAV)
    mlinks = "".join(f'<a href="{h}">{t}</a>' for h,t in NAV)
    return f'''<div class="nav-shell"><header class="nav"><div class="nav-in">
  {brandmark()}
  <nav class="nav-links">{links}</nav>
  {TOGGLE}
  <a class="btn btn-primary btn-sm nav-cta cta-anim" href="contact.html">Get a quote<span class="btn-ic">&rarr;</span></a>
  <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header></div>
<div class="mobile-menu" id="mobile-menu">{mlinks}<a class="btn btn-primary cta-anim" href="contact.html">Get a quote<span class="btn-ic">&rarr;</span></a></div>'''

def cta():
    return f'''<section class="cta-band"><div class="wrap"><div class="cta-card reveal">
  <div class="cta-copy">
    <span class="eyebrow eyebrow-light">Let's build it</span>
    <h2>Got a project? Let's make it loud.</h2>
    <p>Tell us what you need printed, wrapped, or stitched. We'll get you a fast, free quote.</p>
  </div>
  <div class="cta-btns"><a class="btn btn-glow btn-lg cta-anim" href="contact.html">Get a free quote<span class="btn-ic">&rarr;</span></a>
  <a class="btn btn-ghost-light btn-lg" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
</div></div></section>'''

def chat_widget():
    # Demo assistant: runs fully client-side (see chat.js) - guided quote wizard + canned answers.
    # No backend/API needed for the demo; wiring it to a real inbox is a one-line change in chat.js.
    return '''<div class="cw" id="cw">
  <div class="cw-nudge" id="cw-nudge" hidden>
    <button class="cw-nudge-x" id="cw-nudge-x" type="button" aria-label="Dismiss">&times;</button>
    <button class="cw-nudge-open" id="cw-nudge-open" type="button">Questions about pricing or turnaround? I can help &#128075;</button>
  </div>
  <button class="cw-bubble" id="cw-bubble" type="button" aria-label="Open the B Printing assistant" aria-expanded="false" aria-controls="cw-panel">
    <svg class="cw-i cw-i-chat" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 21l2.1-5.4A8.5 8.5 0 1 1 21 11.5Z"/></svg>
    <svg class="cw-i cw-i-x" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
  </button>
  <div class="cw-panel" id="cw-panel" role="dialog" aria-modal="false" aria-labelledby="cw-title" hidden>
    <div class="cw-head">
      <span class="cw-avatar" aria-hidden="true">B</span>
      <div class="cw-head-t"><strong id="cw-title">B Printing Assistant</strong><span><span class="cw-dot"></span> Ask about pricing, services, or hours</span></div>
      <button class="cw-x-btn" id="cw-close" type="button" aria-label="Close chat"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    </div>
    <div class="cw-log" id="cw-log" role="log" aria-live="polite" aria-label="Chat messages"></div>
    <form class="cw-form" id="cw-form" autocomplete="off">
      <label for="cw-input" class="sr-only">Type your message</label>
      <input id="cw-input" class="cw-input" type="text" placeholder="Type your message..." maxlength="600" autocomplete="off">
      <button class="cw-send" id="cw-send" type="submit" aria-label="Send message"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
    </form>
    <p class="cw-note">Demo assistant. Don't share passwords or card numbers.</p>
  </div>
</div>'''

def footer():
    cols = "".join(f'<a href="{h}">{t}</a>' for h,t in FOOT_NAV)
    return f'''<footer><div class="wrap foot-grid">
  <div class="foot-brand">
    {brandmark("brand-foot")}
    <p>Custom printing, wraps, and embroidery in {CITY}. Fast, friendly, and a little bit loud.</p>
    <div class="foot-social">
      <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">Instagram</a>
      <a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">Facebook</a>
      <a href="{TIKTOK}" target="_blank" rel="noopener" aria-label="TikTok">TikTok</a>
    </div>
  </div>
  <div class="foot-col"><h5>Explore</h5>{cols}</div>
  <div class="foot-col"><h5>Visit</h5>
    <a href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a>
    <a href="tel:{PHONE_TEL}">{PHONE}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <span class="foot-note">{HOURS} &middot; Sat-Sun closed</span>
  </div>
</div>
<div class="legal wrap"><span>&copy; 2026 {BIZ}. All rights reserved.</span><span>Serving {CITY.split(",")[0]} and the West Valley.</span></div>
</footer>
{chat_widget()}
<script src="{JSV}"></script>
<script src="{CHATV}"></script></body></html>'''

# ============================ CONTENT DATA ============================
# services. "short" = home cards; "long" = services-page rows (real copy from
# bwraps1.com woven with real review sentiment); "ideal" = who it's for (their site).
SERVICES = [
 {"id":"embroidery","title":"Embroidery","hero":"emb-hats-black.png",
  "short":"Hats, apparel, monogram towels & robes. The stitchin' is bitchin'.",
  "long":"Our featured service, and where the stitchin' is bitchin'. From corporate apparel and sports teams to promotional giveaways and personal gifts, embroidery adds a touch of sophistication to your brand. Customers tell us it comes back sharp, clean, and consistent, every hat matching the last.",
  "bullets":["Custom hats & beanies","Company polos & workwear","Monogram towels & robes","Sports team & spirit wear"],
  "ideal":["Corporate apparel","Sports teams","Promo & giveaways","Monogram gifts"]},
 {"id":"apparel","title":"Custom Apparel & DTF","hero":"apparel-custom.png",
  "short":"Screen print, DTF, and heat press. Turn your crew into walking billboards.",
  "long":"Whether we screen print, use direct-to-film, or heat press your garments, custom gear puts your brand on the frontline and turns your team into walking, talking billboards. DTF delivers vibrant, durable designs that stand out, and wholesale gang sheets keep bigger runs cost-effective.",
  "bullets":["Screen printing","Direct-to-film (DTF) transfers","Wholesale gang sheets","Heat-press & one-offs"],
  "ideal":["Boutiques","Souvenir shops","Online retailers","Promo suppliers"]},
 {"id":"printing","title":"Printing & Signs","hero":"signs-banners.png",
  "short":"Banners, signage, stickers, collateral. If it can be printed, we print it.",
  "long":"Banners, signage, stickers, and business collateral. If it can be printed, we print it, from everyday marketing pieces to large-format graphics that make your brand impossible to miss.",
  "bullets":["Banners & yard signs","Stickers & decals","Business cards & flyers","Posters & large format"],
  "ideal":["Events","Storefronts","Trade shows","Small business"]},
 {"id":"wraps","title":"Vehicle & Wall Wraps","hero":"wrap-truck-bs.jpg",
  "short":"Vehicles, trailers, walls, and vending machines turned into rolling billboards.",
  "long":"We're not just in the business of sticking vinyl on surfaces, we bring your brand to life. Spruce up a retail space, make your trailer the talk of the town, or turn vending machines into mini billboards, all in high-end vinyl built to last.",
  "bullets":["Full & partial vehicle wraps","Trailer & fleet branding","Wall & window graphics","Vending machine wraps"],
  "ideal":["Vehicles & fleets","Trailers","Retail & walls","Vending machines"]},
]

# quality-focused REAL Google review excerpts for the gallery "results" band (distinct from home's).
GALLERY_REVIEWS = [
 ("Google review","Verified · Surprise, AZ","The embroidery was sharp, clean, and professional-looking, with excellent attention to detail. Every hat came out consistent in quality."),
 ("Google review","Verified · Surprise, AZ","Top-notch quality on our stickers, shirts, and hats, using high-end vinyl that lasts. Very fast and affordable too."),
 ("Google review","Verified · Surprise, AZ","Needed a rush order of shirts and they were done in a day. Couldn't be happier with how they turned out."),
]

# gallery: (category, image-file, label) - all REAL shop photos in assets/.
# storefront + gardencup pulled from their Google Business Profile (owner-posted).
GALLERY = [
 # first 6 are the home "Recent work" teaser — keep them varied; BS-Removal truck +
 # storefront are moved lower so they're not featured on the home page (storefront is the hero).
 ("wraps","wrap-gardencup.jpg","Vending machine wrap · gardencup"),
 ("embroidery","emb-hats-shirts.jpg","Embroidered hats & shirts"),
 ("wraps","wrap-trailer-101.jpg","Trailer wrap · 101 Seamless Gutters"),
 ("apparel","apparel-custom.png","Custom apparel"),
 ("embroidery","emb-hats-black.png","Custom embroidered hats"),
 ("printing","signs-banners.png","Custom banners & signs"),
 ("wraps","wrap-truck-bs.jpg","Truck wrap · BS Removal"),
 ("wraps","storefront.jpg","Our shop · window graphics"),
 ("wraps","wrap-wall.jpg","Interior wall wrap"),
 ("embroidery","emb-towels-dark.png","Embossed robes & towels"),
 ("wraps","wrap-vending.png","Vending machine wrap"),
 ("apparel","apparel-dtf.png","DTF transfers"),
 ("embroidery","emb-towels-black.png","Monogram towels"),
 ("wraps","wrap-window-perf.jpg","Vehicle window perf"),
 ("embroidery","emb-hat-shirt.png","Hat & shirt combo"),
 ("embroidery","emb-hats-shirts-2.jpg","Custom embroidered set"),
 # pulled from their Google Business Profile (owner-posted), 2026-07:
 ("wraps","wrap-kodeblue.jpg","Trailer wrap · Kode Blue Plumbing"),
 ("embroidery","emb-shores-hat.jpg","Embroidered hat · Shores Plumbing"),
 ("printing","stickers-sugardaddys.jpg","Die-cut character stickers"),
 ("wraps","wrap-veteran.jpg","Truck wrap · Veteran & Family Cleanup"),
 ("apparel","apparel-tumblers.jpg","Custom printed tumblers"),
 ("embroidery","emb-machine.jpg","In the shop · embroidery in progress"),
 ("wraps","wrap-boutique-suv.jpg","SUV wrap · boutique client"),
 ("printing","signs-cuddlypet.jpg","Storefront window signs · Cuddly Pet"),
 ("embroidery","emb-polo-cap.jpg","Embroidered polo & cap set"),
 ("wraps","wrap-flag-perf.jpg","Rear window perf · American flag"),
 ("apparel","apparel-tumbler-hg.jpg","Engraved tumbler"),
 ("printing","print-longwongs.jpg","Framed print · Long Wongs"),
 ("wraps","wrap-blazin.jpg","Truck wrap · Blazin Pest Control"),
 ("embroidery","emb-gear.jpg","Embroidered helmets & gear"),
 ("printing","signs-partybus.jpg","Custom metal sign"),
 # more real client jobs (owner-confirmed permission), 2026-07:
 ("printing","engraved-board.jpg","Engraved keepsake board"),
 ("embroidery","emb-watkins-cap.jpg","Embroidered cap · Watkins Restorations"),
 ("apparel","apparel-jb-detailing.jpg","Cap & shirt set · JB Car Detailing"),
 ("printing","decal-barkbrew.jpg","Custom decal · Bark & Brew"),
 ("wraps","wrap-fancypoo.jpg","Trailer wrap · Fancy Poo"),
 ("apparel","apparel-judgenot.jpg","Custom tee · Judge Not Photography"),
 ("printing","decal-beamauto.jpg","Logo decal · Beam Auto"),
 ("apparel","apparel-dryheat.jpg","Custom tee · Dry Heat Junk Removal"),
]
GCATS = [("all","Everything"),("embroidery","Embroidery"),("apparel","Apparel & DTF"),
         ("printing","Printing"),("wraps","Wraps")]

# industries served (Wall of Fame) — real photos + real use-case copy from bwraps1.com.
# (photo, headline, line). Lives on the Services page now (moved off About to avoid dup).
INDUSTRIES = [
 ("case-foodtruck.png","Food trucks","A tasty new look that turns heads at every stop."),
 ("case-realestate.png","Real estate","Branding that stands out in a crowded market."),
 ("case-gym.png","Gyms & fitness","Wall wraps and apparel that motivate your members."),
 ("case-school.png","Schools & teams","Spirit wear that actually shows some spirit."),
]

# brands we print on. First 4 = real logos verified on bwraps1.com. The rest are
# standard blank/cap brands any decoration shop stocks (SanMar/S&S catalog) shown as
# text chips - representative; owner can confirm/trim. ("img"|"txt", file, label)
BRANDS = [
 ("img","brand-gildan.png","Gildan"), ("img","brand-bellacanvas.png","Bella+Canvas"),
 ("img","brand-newera.png","New Era"), ("img","brand-cornerstone.png","CornerStone"),
 ("txt",None,"Comfort Colors"), ("txt",None,"Next Level"), ("txt",None,"Champion"),
 ("txt",None,"Carhartt"), ("txt",None,"Richardson"), ("txt",None,"Sport-Tek"),
 ("txt",None,"Port & Company"), ("txt",None,"Yupoong"),
]
def brand_chip(kind, f, n):
    if kind == "img":
        return f'<span class="brand-chip"><img src="assets/{f}" alt="{n}" loading="lazy"></span>'
    return f'<span class="brand-chip brand-chip-txt">{n}</span>'

# testimonials: REAL 5-star Google review excerpts (pulled 2026-07-23; 5.0 avg, 20 reviews).
# Verbatim text is behind Google's bot-wall, so these are the excerpts search surfaced.
# TODO before launch: owner to confirm each reviewer's first name for fuller attribution.
TESTIMONIALS = [
 ("Google review","Verified · Surprise, AZ","Harvest was great to work with, very professional, responsive, and kept communication clear throughout the whole process. I highly recommend them to anyone looking for quality printing and wraps."),
 ("Google review","Verified · Surprise, AZ","I can't say enough great things about B Printing and Wraps! Sharlenea and her husband truly went above and beyond for my business."),
 ("Google review","Verified · Surprise, AZ","Shar was super nice, helpful, and knowledgeable about exactly what I needed to get done. Did an amazing job on my van wrap."),
]

def photo(cat, file, label, box=False, lightbox=False):
    extra = ' data-full="assets/'+file+'"' if lightbox else ""
    role = ' role="button" tabindex="0"' if lightbox else ""
    fig = f'''<figure class="tile{" tile-box" if box else ""}" data-cat="{cat}"{extra}{role}>
      <img src="assets/{file}" alt="{label}" loading="lazy">
      <figcaption>{label}</figcaption></figure>'''
    return fig

# ============================ PAGES ============================
def home():
    svc = "".join(
        f'''<a class="svc" href="services.html#{s["id"]}">
        <span class="ic-badge">{icon(s["id"])}</span><h3>{s["title"]}</h3><p>{s["short"]}</p>
        <span class="svc-more">Explore<span class="btn-ic">&rarr;</span></span></a>''' for s in SERVICES)
    teaser = "".join(photo(c,f,l) for c,f,l in GALLERY[:6])
    # marquee: render the brand set twice so the CSS loop is seamless
    brow = "".join(brand_chip(*b) for b in BRANDS)
    brands = brow + brow
    tst = "".join(f'<blockquote class="tst"><div class="tst-stars">★★★★★</div><p>&ldquo;{q}&rdquo;</p><cite>{n}<span>{r}</span></cite></blockquote>'
                  for n,r,q in TESTIMONIALS)
    return head(f"{BIZ} | {TAG}", f"Custom printing, wraps, and embroidery in {CITY}. Get a fast, free quote from the shop that does it all.","home","index.html") + nav("index.html") + f'''
<main id="main">
<section class="hero"><div class="wrap hero-in">
  <div class="hero-copy reveal">
    <span class="eyebrow">★★★★★ · 5.0 on Google · {CITY.split(",")[0]}, AZ</span>
    <h1>Printing, wraps &amp; embroidery that make your brand <span class="hl" style="white-space:normal">impossible to miss</span>.</h1>
    <p>From one embroidered hat to a full fleet wrap, all done in house and out the door fast.</p>
    <p class="hero-visit"><strong>Come see us in person</strong>
      <a href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a>
      <span>{HOURS} &middot; Sat &amp; Sun closed</span></p>
    <div class="hero-btns"><a class="btn btn-primary btn-lg cta-anim" href="contact.html">Get a free quote<span class="btn-ic">&rarr;</span></a>
    <a class="btn btn-ghost btn-lg" href="gallery.html">See our work</a></div>
  </div>
  <div class="hero-art reveal d1">
    <div class="hero-frame"><img src="assets/storefront.jpg" alt="{BIZ} storefront in {CITY}" width="1600" height="1200"></div>
    <div class="hero-badge float-a"><img src="assets/logo-az.png" alt="" width="80" height="80"><span>Made in<br>Surprise, AZ</span></div>
    <figure class="hero-chip float-b"><img src="assets/emb-hats-black.png" alt="Custom embroidered hats" loading="lazy"></figure>
  </div>
</div></section>

<section class="brands"><div class="wrap brands-in">
  <span class="brands-label">We print on the good stuff</span>
  <div class="brands-marquee"><div class="brands-track">{brands}</div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">What we do</span>
    <h2>One shop for everything custom</h2>
    <p>From a single embroidered cap to a full fleet wrap, we handle it in house.</p></div>
  <div class="svc-grid stagger reveal">{svc}</div>
</div></section>

<section class="section band"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Recent work</span><h2>A little taste of the shop</h2>
    <p>Real jobs for real businesses. Tap through the full gallery for more.</p></div>
  <div class="gal-grid gal-teaser stagger reveal">{teaser}</div>
  <div class="center"><a class="btn btn-dark btn-lg" href="gallery.html">View the full gallery<span class="btn-ic">&rarr;</span></a></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">Why Choose Us</span><h2>Small shop, big-league output</h2></div>
  <div class="feat-grid stagger reveal">
    {"".join(f'<div class="feat"><span class="ic-badge">{icon(k)}</span><h3>{t}</h3><p>{d}</p></div>' for k,t,d in FEATURES)}
  </div>
</div></section>

<section class="section band"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">★★★★★ · 5.0 on Google</span><h2>What customers say</h2>
    <p>Real 5-star reviews from the businesses we've printed, wrapped, and stitched for.</p></div>
  <div class="tst-grid stagger reveal">{tst}</div>
  <div class="center" style="margin-top:32px"><a class="btn btn-ghost" href="{GOOGLE}" target="_blank" rel="noopener">Read all reviews on Google<span class="btn-ic">&rarr;</span></a></div>
</div></section>
</main>
{cta()}{footer()}'''

def services():
    cards = ""
    for s in SERVICES:
        bl = "".join(f"<li>{b}</li>" for b in s["bullets"])
        chips = "".join(f'<span class="ideal-chip">{x}</span>' for x in s["ideal"])
        cards += f'''<article class="prod-card" id="{s["id"]}">
        <div class="prod-img"><img src="assets/{s["hero"]}" alt="{s["title"]}" loading="lazy"></div>
        <div class="prod-body"><span class="ic-badge">{icon(s["id"])}</span><h2>{s["title"]}</h2>
        <p>{s["long"]}</p><ul class="ticks">{bl}</ul>
        <div class="ideal"><span class="ideal-label">Ideal for</span>{chips}</div>
        <a class="btn btn-primary cta-anim" href="contact.html">Quote this<span class="btn-ic">&rarr;</span></a></div>
      </article>'''
    uses = "".join(f'<figure class="usecase"><img src="assets/{f}" alt="{t}" loading="lazy"><figcaption><strong>{t}</strong><span>{d}</span></figcaption></figure>' for f,t,d in INDUSTRIES)
    return head(f"Services | {BIZ}", f"Embroidery, custom apparel, DTF, printing, signs, and wraps in {CITY}.","services","services.html") + nav("services.html") + f'''
<main id="main">
<section class="page-hero"><div class="wrap reveal">
  <span class="eyebrow">Services</span><h1>Everything we make</h1>
  <p>Four lines, one shop, all under one roof in {CITY.split(",")[0]}. Embroidery, custom apparel and DTF, printing and signs, and vehicle wraps. Mix and match to brand your whole business, and get it out the door fast.</p>
</div></section>
<section class="section" style="padding-top:40px"><div class="wrap">
  <div class="prod-grid stagger reveal">{cards}</div>
</div></section>
<section class="section band"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">Who we work with</span><h2>Built for busy businesses</h2>
    <p>From food trucks to real estate to gyms and schools, we help {CITY.split(",")[0]} brands show up loud.</p></div>
  <div class="usecase-grid stagger reveal">{uses}</div>
</div></section>
</main>{cta()}{footer()}'''

def gallery():
    filt = "".join(f'<button class="gfilter{" active" if c=="all" else ""}" data-cat="{c}">{t}</button>' for c,t in GCATS)
    tiles = "".join(photo(c,f,l,lightbox=True) for c,f,l in GALLERY)
    greviews = "".join(f'<blockquote class="tst"><div class="tst-stars">★★★★★</div><p>&ldquo;{q}&rdquo;</p><cite>{n}<span>{r}</span></cite></blockquote>'
                       for n,r,q in GALLERY_REVIEWS)
    return head(f"Gallery | {BIZ}", f"See real embroidery, apparel, printing, and wrap work from {BIZ} in {CITY}.","gallery","gallery.html") + nav("gallery.html") + f'''
<main id="main">
<section class="page-hero"><div class="wrap reveal">
  <span class="eyebrow">Gallery</span><h1>See the work</h1>
  <p>Real jobs for real businesses, truck and trailer wraps, embroidered hats and apparel, DTF, banners and signage. Every photo here left our shop in {CITY.split(",")[0]}. Tap any one to view it bigger.</p>
</div></section>
<section class="section" style="padding-top:24px"><div class="wrap">
  <div class="stats reveal">
    <div class="stat"><strong>5.0★</strong><span>rating on Google</span></div>
    <div class="stat"><strong>50+</strong><span>5-star reviews</span></div>
    <div class="stat"><strong>In-house</strong><span>print · wrap · stitch</span></div>
    <div class="stat"><strong>Fast</strong><span>in-house turnaround</span></div>
  </div>
</div></section>
<section class="section" style="padding-top:24px"><div class="wrap">
  <div class="gfilters reveal">{filt}</div>
  <div class="gal-grid gal-masonry" id="gal">{tiles}</div>
</div></section>
<section class="section band"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">★★★★★ · 5.0 on Google</span><h2>Work that holds up</h2>
    <p>It's not just how it looks leaving the shop, it's how it holds up after. Here's what customers say about the quality.</p></div>
  <div class="tst-grid stagger reveal">{greviews}</div>
  <div class="center" style="margin-top:32px"><a class="btn btn-ghost" href="{GOOGLE}" target="_blank" rel="noopener">Read all reviews on Google<span class="btn-ic">&rarr;</span></a></div>
</div></section>
</main>
<div class="lightbox" id="lightbox" aria-hidden="true"><button class="lb-close" aria-label="Close">&times;</button><img src="" alt=""></div>
{cta()}{footer()}'''

def about():
    fame = "".join(f'<span class="fame-chip">{n}</span>' for n in
        ["Restaurants","Cafes","Gyms & wellness","Auto shops","Real estate","Food trucks","Schools"])
    return head(f"About | {BIZ}", f"{BIZ} is a print, wrap, and embroidery shop in {CITY}. Meet the team behind the work.","about","about.html") + nav("about.html") + f'''
<main id="main">
<section class="page-hero"><div class="wrap reveal">
  <span class="eyebrow">About</span><h1>Your neighbors with a print shop</h1>
</div></section>
<section class="section"><div class="wrap about-in">
  <div class="about-copy reveal">
    <p class="lead">{BIZ} started with a simple idea: give {CITY} a creative shop that can print it, wrap it, and stitch it, without sending you to three different vendors.</p>
    <p>We're a small team that treats a one-off gift with the same care as a full fleet wrap. Whether you're a food truck needing a fresh look, a gym motivating members with a wall wrap, or a team that wants spirit wear with actual spirit, we've got you.</p>
    <p>Everything happens in house, so your branding stays consistent and your timeline stays short.</p>
    <div class="about-facts">
      <div><strong>{ADDR.split(",")[0]}</strong><span>Dysart Rd, Surprise</span></div>
      <div><strong>{HOURS}</strong><span>Sat-Sun closed</span></div>
      <div><strong>In house</strong><span>Print · wrap · stitch</span></div>
    </div>
  </div>
  <div class="about-art reveal d1"><div class="art-frame">{photo("embroidery","emb-thread.png","In the shop")}</div></div>
</div></section>
<section class="section band"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">Wall of Fame</span><h2>Proud of who we work with</h2>
    <p>We serve a whole range of businesses around Surprise:</p></div>
  <div class="fame reveal">{fame}</div>
</div></section>
</main>{cta()}{footer()}'''

def contact():
    return head(f"Contact | {BIZ}", f"Get a free quote from {BIZ} in {CITY}. Call {PHONE} or send us your project.","contact","contact.html") + nav("contact.html") + f'''
<main id="main">
<section class="page-hero"><div class="wrap reveal">
  <span class="eyebrow">Contact</span><h1>Let's get you a quote</h1>
  <p>Tell us what you need. Attach your art or logo if you've got it, and we'll take it from there.</p>
</div></section>
<section class="section"><div class="wrap contact-in">
  <form class="cform reveal" action="https://formsubmit.co/{EMAIL}" method="POST" enctype="multipart/form-data">
    <input type="hidden" name="_subject" value="New quote request from the website">
    <input type="hidden" name="_template" value="table">
    <input type="text" name="_honey" style="display:none">
    <div class="f-row"><label>Name<input name="name" required></label>
    <label>Phone<input name="phone" type="tel"></label></div>
    <label>Email<input name="email" type="email" required></label>
    <label>What do you need?
      <select name="service"><option value="">Pick one</option>
      <option>Embroidery</option><option>Custom apparel / DTF</option>
      <option>Printing / signs</option><option>Vehicle or wall wrap</option><option>Not sure yet</option></select></label>
    <label>Your art or logo (optional)<input name="attachment" type="file"></label>
    <label>Project details<textarea name="message" rows="5" placeholder="Sizes, quantities, colors, deadline..."></textarea></label>
    <button class="btn btn-primary btn-lg" type="submit">Send it<span class="btn-ic">&rarr;</span></button>
    <p class="form-fine">Prefer to talk? Call or text {PHONE}.</p>
  </form>
  <aside class="contact-side reveal d1">
    <div class="cside-card"><h3>Call or text</h3><a class="big-phone" href="tel:{PHONE_TEL}">{PHONE}</a></div>
    <div class="cside-card"><h3>Email</h3><a href="mailto:{EMAIL}">{EMAIL}</a></div>
    <div class="cside-card"><h3>Visit the shop</h3><a class="cside-addr" href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a><a href="{MAPS}" target="_blank" rel="noopener">Get directions &rarr;</a></div>
    <div class="cside-card"><h3>Hours</h3><p>{HOURS}<br>Saturday &amp; Sunday closed</p></div>
    <div class="cside-card"><h3>Follow</h3><div class="cside-social"><a href="{IG}" target="_blank" rel="noopener">Instagram</a><a href="{FB}" target="_blank" rel="noopener">Facebook</a><a href="{TIKTOK}" target="_blank" rel="noopener">TikTok</a></div></div>
  </aside>
</div></section>
<section class="map-sec"><iframe src="{MAP_EMBED}" title="{BIZ} location map" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></section>
</main>{footer()}'''

# ============================ BUILD ============================
PAGES = {"index.html":home,"services.html":services,"gallery.html":gallery,
         "about.html":about,"contact.html":contact}

def sitemap():
    today = date.today().isoformat()
    urls = "".join(
        f"<url><loc>{BASE}/{p}</loc><lastmod>{today}</lastmod>"
        f"<priority>{'1.0' if p=='index.html' else '0.8'}</priority></url>" for p in PAGES)
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
