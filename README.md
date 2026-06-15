# Arena Lite — Web Application
**Arena-JB-EMS** · Deployed on Vercel · June 2026

Arena Lite is the practitioner-facing edge product of The Arena Hub Ltd. It provides Alternative Provision and SEMH educators with a sovereign, Google Workspace-native platform for capturing and evidencing student progress.

## Tech Stack

```
Frontend:   HTML / vanilla JS (Navy + Gold UI)
Auth:       Google OAuth via GAS ENGINE_LIBRARY
Backend:    Google Apps Script (ENGINE_LIBRARY v1.8.0)
Ledger:     Google Sheets (STUDENT_VAULT — per-school sovereign deployment)
Ingestor:   Cloud Run (arena-hub-ingestor, europe-west2)
AI:         Gemini 2.0 Flash (taxonomy matching via /suggest endpoint)
Hosting:    Vercel (Production + github-pages environments)
```

## Pages

| File | Purpose |
|---|---|
| `index.html` | Landing / marketing page |
| `app.html` | Main application shell |
| `login.html` | Google OAuth login screen |
| `signup.html` | School onboarding / licence registration |
| `success.html` | Post-signup confirmation |
| `dpa.html` | Data Processing Agreement (UK GDPR Art. 28) |
| `privacy.html` | Privacy Policy |
| `terms.html` | Terms & Conditions |

## Dynamic Config

Contact details, legal identifiers, and email addresses are managed via the **ARENA_SITE_CONFIG** Google Sheet in the `05_Websites` Shared Drive folder. The `arena-config.js` script fetches config on page load and injects values via `data-config` attributes.

**Config endpoint:** Managed via GAS Web App (same deployment as main site).
**To update a contact detail:** Open ARENA_SITE_CONFIG sheet → ⚡ Arena Config → Open Admin Panel → edit → Commit.

## Assets

| File | Purpose |
|---|---|
| `assets/` | UI screenshots, product video, PWA icons |
| `arena-icon-*.png` | PWA icons (180, 192, 512, 1024px) |
| `app-manifest.json` | PWA manifest |
| `sw.js` | Service worker (offline caching) |
| `vercel.json` | Vercel deployment config |

## Company

**The Arena Hub Ltd** · Company No. 1708605 · Registered in England & Wales  
Founder: Jonathan Baguley · [thearenahub.co.uk](https://thearenahub.co.uk)
