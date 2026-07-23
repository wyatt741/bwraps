# B Printing and Wraps — Creative Brief / Master Prompt

_The single structuring doc for this site. Read first. Updated as decisions land._

## The business (from bwraps1.com, 2026-07-23)
- **Name:** B Printing and Wraps
- **Location:** Surprise, Arizona (Phoenix West Valley)
- **Phone:** 928-230-8525
- **What they do:** a full-service print + wrap + embroidery shop.
- **Services observed on the current site:**
  - Vehicle / wall / vending-machine wraps
  - **Embroidery** (their featured service — custom hats, apparel, monogram towels & robes). Playful tagline: "the stitchin' is bitchin'."
  - Custom apparel — screen print, DTF (direct-to-film), heat press
  - DTF printing / wholesale gang sheets
  - General printing / signage
- **Audience:** local businesses (restaurants, gyms, auto shops, real estate, schools, food trucks, non-profits) + individuals wanting custom gear.
- **Existing assets on old site:** "Wall of Fame" (local client directory), testimonials, TikTok, contact form (name/phone/email/file upload/message).
- **Voice:** bold, playful, community-minded, a little cheeky.

## The master prompt (what we're building)
> Build a fast, modern, mobile-first marketing site for **B Printing and Wraps**, a print/wrap/embroidery shop in Surprise, AZ. The site's #1 job is to turn visitors into **quote requests**. It should show off their work with a strong visual gallery, make the range of services obvious, carry their playful local voice, and be dead simple to contact. Bold and colorful to match a print shop's energy — this is not a corporate SaaS site.

## Architecture (reuse what works from anderson-it)
- **Single Python generator `build.py`** emits every page. Edit content in build.py, never hand-edit HTML. Deploy = `git push`.
- `styles.css` + `app.js`, cache-busted `?v=N`.
- **No fabrication** — real reviews/testimonials only, real photos of their work, no invented stats or client logos without permission.
- **Concise voice, no em dashes.**
- Contact form via FormSubmit.co (like anderson-it) to their email; keep the 928 number + file upload for artwork.
- Motion layer (reveals, hovers) under `prefers-reduced-motion`.
- Real licensed stock only where their own photos are missing (with a plan to swap in real work).

## Open decisions (filled in by the grilling round)
- Primary goal: _TBD_
- Visual vibe / theme: _TBD_
- Lead services to feature: _TBD_
- Brand assets available (logo, photos, colors): _TBD_
- Contact email for the form: _TBD_
- Deploy target (demo subdomain vs replacing bwraps1.com): _TBD_

## Page plan (draft — adjust after answers)
1. **Home** — hero + what-they-do + gallery teaser + why-them + testimonials + contact CTA
2. **Services** — wraps / embroidery / apparel & DTF / printing (each with detail)
3. **Gallery / Portfolio** — the proof, grouped by type
4. **About** — the shop, the local story, Wall of Fame
5. **Contact** — form (with artwork upload) + phone + map/area

## Status
Discovery done. Awaiting owner answers to the grilling round, then build a **demo** for the friend to review (not live to their domain until approved).
