# Worldbrand Classic Signs — Website

Client website for **Worldbrand Classic Signs (WCS)**, Durban, built by **Talent Learn Consult (TLC)**.
This repository on GitHub is the single source of truth for the site.

- **Preview (proposal) link:** https://dionpather-afk.github.io/worldbrand-classic-signs/
- **Future live domain:** www.worldbrandsigns.co.za (domain not yet registered/active as at 11 Nov 2026)
- **Delivery route:** TLC Website Delivery Blueprint, Route B (code-first): GitHub Pages preview → client approval + deposit → domain + Xneelo hosting → deploy → client sign-off → Dion's go-ahead → live.

## Look & feel
Black background with brushed-chrome headings and neon accents, taken from the new WCS logo:
neon pink `#ff2bd6`, neon red `#ff2d55`, lime `#c8ff2e`, yellow `#f6ff5a`.
Fonts (self-hosted, SIL Open Font License): Anton (headings), Tilt Neon (neon script), Inter (body).

## Pages (17)
Home · About · Services · 3D Fabricated Signs · Billboards · Pylon Signs · Perspex Signs · Lightboxes ·
Digital Printing · Wallpaper & Wall Branding · Vehicle Branding · Projects · Clients · Get a Quote ·
Contact · Privacy Policy (POPIA) · 404

## Content sources
- All company text is from the client's Company Profile (2024), lightly edited and typo-corrected.
- All 34 project photos are the client's own, extracted from the Company Profile.
- Contact details confirmed by Dion (11 Nov 2026): 25 Sedgemoor Pl, Woodlands, Durban, 4004 · +27 81 400 2417 · info@worldbrandsigns.co.za

## ⚠️ Demo content to replace before going live
| Item | Where | Status |
|---|---|---|
| 3 client testimonials | Home page "What clients say" (marked **Demo content**) | Placeholder — need real reviews from client |
| Facebook link | Removed for now | Need the real Facebook page URL from client, then re-add |
| Instagram / TikTok | Footer + Contact page | Verified 11 Nov 2026: @worldbrandsigns and @worldbrands1 are the client's accounts |
| Business hours | Not shown | Ask client if they want them listed |
| Client logo images | Clients page uses neon text names, not logos | Optional: client to send logos + confirm permission |

## How to edit / build
All pages are generated from `_build/build.py` (content and page data live at the top of that file).
```bash
python3 _build/build.py          # preview build (noindex, GitHub Pages paths)
python3 _build/build.py --live   # live build for www.worldbrandsigns.co.za (indexable, sitemap)
```
Styles: `assets/css/style.css` · Behaviour: `assets/js/main.js` · Images: `assets/img/`

## Forms
The quote and contact forms do **not** store any data. They build a pre-filled WhatsApp message to +27 81 400 2417.
No server, database or secrets are needed.

## Security
- Static site only — no server code, no passwords, no API keys.
- Content-Security-Policy blocks third-party scripts; only Google Maps is allowed (as an embedded map).
- Preview build is set to `noindex` so Google does not index the demo.

## Rollback plan
Every change is a Git commit, and each release is saved as its own branch (`release/v1.0-preview`, …).
To roll back: `git checkout release/v1.0-preview -- .` then commit and push to `main` (or `git revert <commit>`). GitHub Pages redeploys in about a minute.
On Xneelo: keep the previous release zip; re-upload it to roll back.
