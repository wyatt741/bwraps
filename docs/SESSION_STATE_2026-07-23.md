# bwraps — Session State (2026-07-23)

**Started / Last Updated:** 2026-07-23
**Project:** C:\Users\Admin\Projects\bwraps
**Topic:** New site for B Printing and Wraps (Wyatt's friend's shop) — demo v1 built with placeholders; real assets captured, ready to wire in.

## What We Are Building / Doing
A brand-new marketing site for **B Printing and Wraps**, a print/wrap/embroidery shop in **Surprise, AZ** (West Valley). Replacing/upgrading their current site at **bwraps1.com**. Built on the SAME engine as Wyatt's `anderson-it` project: one Python `build.py` generator emits every page, `styles.css`+`app.js` cache-busted, no fabricated content, FormSubmit contact. Goal: gallery + quote-lead balanced, **bold & colorful** print-shop aesthetic, playful local voice. This is a DEMO for the friend to review before anything goes live to their domain.

## Decisions Made (from a grilling round)
- **Primary goal:** gallery + quote requests, balanced.
- **Vibe:** bold & colorful (CMYK energy) — light base, vivid pink/cyan/yellow/purple accents. NOT the dark Anderson look.
- **Lead services:** Embroidery, Apparel & DTF, Printing & Signs (wraps included but not top-billed).
- **Assets:** owner has logo + real photos → pull from their live site (below).
- **Voice:** playful, local, cheeky ("the stitchin' is bitchin'", "make your brand loud"). No em dashes.

## What WORKED (evidence)
- **Demo v1 builds + renders** — `py build.py` emits index/services/gallery/about/contact + sitemap/robots (confirmed output). Served on `http://127.0.0.1:8731`, `get_page_text` showed full hero/services/gallery rendering correctly with the Poppins/Inter fonts + colorful placeholder tiles.
- **Real content pulled from bwraps1.com** via browser JS extraction (below).

## ⭐ REAL ASSETS TO WIRE IN (exact next step) — pulled from bwraps1.com 2026-07-23
Download these into `assets/` and replace the placeholder tiles/wordmark. CDN host: `lirp.cdn-website.com/0b9bd604/dms3rep/multi/opt/`
- **Logo (primary, transparent 1920²):** `https://lirp.cdn-website.com/0b9bd604/dms3rep/multi/opt/B+PRINTING+-+WRAPS+TRANSPARENT-1920w.png`
- **Logo (AZ-flag variant 500²):** `https://lirp.cdn-website.com/0b9bd604/dms3rep/multi/opt/Arizona+flag+logo-1920w.png`
- **Work photo 1:** `https://lirp.cdn-website.com/0b9bd604/dms3rep/multi/opt/IMG_9575-1920w.jpg`
- **Work photo 2 (embroidered hats & shirts):** `https://lirp.cdn-website.com/0b9bd604/dms3rep/multi/opt/CUSTOM+EMBROIDERED+HATS+AND+SHIRTS+%281%29-1920w.jpg`
- NOTE: homepage was image-light (only these). Their **service/gallery inner pages likely have more photos** — browse bwraps1.com's other pages (or ask the owner for a photo dump) to fill the gallery. Their site is a Duda/cdn-website.com build; images sit under the same CDN path with different filenames.

### Real socials + contact (replace placeholders in build.py)
- **TikTok:** https://www.tiktok.com/@luckstitch  (NOT @bwraps1 — current build.py placeholder is wrong)
- **Instagram:** https://www.instagram.com/bprinting_/
- **Facebook:** https://www.facebook.com/bprintingandwraps
- **Google Maps:** pinned in Surprise, AZ (~33.634, -112.34)
- **Phone:** 928-230-8525 (confirmed on their site)
- **Form email:** STILL a placeholder `hello@bwraps1.com` — owner must confirm the real inbox + activate FormSubmit.
- **Real testimonials:** their site HAS a testimonials section — NOT yet captured. Pull the actual quotes before launch (current build.py has 3 SAMPLE-marked cards).

## Current State of Files
| File | Status | Notes |
|------|--------|-------|
| `build.py` | Complete (v1) | Generator: 5 pages. Placeholders for logo/photos/testimonials. TikTok handle wrong (fix to @luckstitch). |
| `styles.css` | Complete (v1) | Bold colorful theme, responsive, motion, gallery filter, colorful placeholder tiles. |
| `app.js` | Complete (v1) | Mobile menu, scroll reveals, gallery filter. |
| `assets/` | Empty | Real logo + photos go here. |
| `docs/CREATIVE_BRIEF.md` | Complete | The structuring brief / master prompt. |
| `CLAUDE.md` | Complete | Project entry. |

## What Has NOT Been Tried Yet
- Downloading + self-hosting the real images (have the URLs, haven't pulled the files).
- Wiring real logo/photos/testimonials/socials into build.py.
- Deploying to a shareable URL (GitHub Pages `wyatt741/bwraps`) so the friend can view remotely — NOT set up (no git remote yet).
- Confirming the real form inbox + FormSubmit activation.

## Commits Made This Session
- Local repo `git init`'d; first commit made this session (source + generated HTML). No remote yet.

## System / Config Changes Outside This Repo
- Added an auto-memory entry `bwraps-site` (+ MEMORY.md pointer) in `~/.claude/projects/C--Users-Admin-Projects/memory/`.
- A local `py -m http.server 8731` was started for preview (background; harmless, dies with the session).

## Blockers & Open Questions
- Real form inbox email (owner).
- More/real work photos + real testimonials (owner or deeper site scrape).
- Deploy target: shareable demo link now, or wait for owner assets first? (Wyatt to decide.)

## Environment & Setup Notes
- Build: `py build.py`. Preview: `py -m http.server 8731 --bind 127.0.0.1 --directory .` then open the Browser pane to `http://127.0.0.1:8731`.
- Same engine/conventions as `anderson-it` (see that project's CLAUDE.md).

## Exact Next Step
Download the 4 real asset URLs above into `assets/`, fix the TikTok handle to @luckstitch, add IG/FB/Maps links, and wire the real logo + photos into build.py (replace the colorful placeholder tiles + "B" wordmark). Then rebuild and re-preview. After that: pull real testimonials + get the form inbox, then deploy a shareable link.

## Resume Prompt
Next session, say **`resume bwraps`** — the resume skill reads this doc + the CREATIVE_BRIEF, then continues by wiring in the real assets listed under "REAL ASSETS TO WIRE IN."
