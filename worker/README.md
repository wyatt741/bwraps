# B Printing and Wraps chat Worker — deploy guide

The tiny backend that holds the Anthropic API key and powers the AI half of the chat
widget. The static site (GitHub Pages) can't hold a secret, so this runs free on
Cloudflare Workers. One-time setup, ~10 minutes.

**Hybrid:** free-text questions go to this Worker's AI (`/chat`, Claude Haiku, trained on
the shop's services). The quote **wizard** stays deterministic on the client and only
POSTs its answers to `/lead` — no AI ever touches pricing or leads.

## What you need
- A free **Cloudflare** account (you have one).
- An **Anthropic API key** with credits (console.anthropic.com → API Keys). Make a *separate*
  key just for this bot so it can be capped and rotated on its own.
- Node.js (fnm is set up on this machine).

## Steps
```bash
cd worker
npx wrangler login              # opens a browser, approve
npx wrangler secret put ANTHROPIC_API_KEY   # paste the key when prompted; it never goes in any file
npx wrangler deploy
```
`deploy` prints a URL like `https://bwraps-chat.<your-subdomain>.workers.dev`. Copy it.

## Wire it to the site
1. Open `../chat.js`, set `WORKER_URL` to that URL (no trailing slash).
2. In `../build.py`, bump `CHATV`: `chat.js?v=1` → `chat.js?v=2`.
3. `python3 build.py` then `git push origin main`.
4. Until `WORKER_URL` is set, the widget still works as a **demo** (canned keyword answers +
   the wizard). Setting it flips free-text to real AI. Nothing breaks in between.

## Recommended safety (do these)
- **Anthropic Console → set a monthly spend limit + billing alert.** Hard backstop: even if
  the endpoint is abused, the bill can't exceed your number. With the dedicated key, this only
  caps the bot. ~2 cents per conversation at Haiku pricing.
- **Optional per-IP rate limiting:** `npx wrangler kv namespace create RATE_KV`, paste the id
  into `wrangler.toml` (uncomment the block), `npx wrangler deploy`.

## Notes
- Model is `claude-haiku-4-5` (change `MODEL` in `worker.js` to switch).
- `ALLOWED` in `worker.js` lists origins allowed to call it: `bwraps1.com`, `www.bwraps1.com`,
  and `wyatt741.github.io` (the Pages demo). Update if the domain changes.
- `/lead` posts to the same FormSubmit inbox (`elitecustomprinting@outlook.com`) as the contact
  form. That inbox's FormSubmit activation must be confirmed by the owner for leads to arrive.
- The output filter (`BLOCK` regex) drops any reply with a specific price or "guarantee" and
  swaps in a "get a free quote" deflection — an FTC-safe backstop even if the model is jailbroken.
