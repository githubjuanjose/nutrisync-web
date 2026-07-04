# NutriSync — Release Notes / Change Log
**Package date:** July 3, 2026 · **Contents:** `index.html` (marketing) + `app.html` (web application) + `i18n/` (language resources) + `hub/` (team documents) + `assets/`

This package is self-contained and static — deploy by dragging the folder into Cloudflare Pages (see `README-PUBLISH.md`).

---

## 1 · Marketing site (`index.html`)
The original NutriSync marketing site, preserved in full: hero with live phase preview, validation/traction band, The Problem, The Science (four phases), Cycle Alignment Score, platform value props, Connected Health, pricing (Free / Premium / Employers), team, waitlist and footer.
- **Team access rooms** (footer): Investors / Builders rooms (access code `123456`) with the embedded hub documents (`hub/`).
- **"Prototype" footer link** keeps the original phone prototype reachable.

## 2 · Health Flows — two prototype views
The "See NutriSync in action" section has a **Mobile app / Web app toggle**:
- **Mobile app · prototype** — the original phone screen cards; each opens the interactive phone prototype in-page (full mobile journeys).
- **Web app · prototype** — the same journeys as web cards; each opens the web application in **prototype mode** (`app.html#demo-<screen>`): full navigation on Olivia's demo data, **no account required**, marked with a "PROTOTYPE · DEMO DATA" badge. It never touches the backend.
- **"Open the app"** buttons (nav, hero, pricing, closing CTA) lead to the **live** web application.

## 3 · Responsive web application (`app.html`)
A full customer web app translating the mobile journeys to web (sidebar-dashboard shell chosen from design options):
- **Journeys:** sign-up → 8-step onboarding → all-set → daily mood/energy check-in → Home (phase hero + Cycle Alignment ring) → NutriLog → Movement → Progress → Calendar → Edit Period → Edit Health → Settings → Connected apps → Connect device → Data & Privacy → Sign-in & Security.
- **Responsive tiers:** mobile (bottom tab bar) · tablet (icon rail) · desktop (full sidebar), fluid type/spacing throughout.
- **Data modes:** first-run empty states after sign-up; populated demo persona in prototype mode.

## 4 · Live backend (Supabase)
Wired per the backend spec — same project the mobile apps use:
- Real email/password **sign-up and login** (anon key baked in).
- **Onboarding persists** to `users` + `cycles`; daily check-in, NutriLog checks, Movement sessions and Edit Period logs write through.
- **Cycle math identical to mobile**; CAS engine computes and writes `daily_scores` (5 components).
- Privacy controls: consent toggles, **JSON export**, **delete account & data**.
- Signed-out deep links are guarded (live mode always lands on login); prototype mode is the explicit no-account path.

## 5 · Wearables & connected health
- **Connected apps** screen: 6 providers (Apple Health, Oura, Garmin, Fitbit, WHOOP, Google Fit) with connect/disconnect and **per-metric consent toggles** (sleep, HRV, resting HR, temperature, workouts, steps).
- **Connect-device flow** with read-only permission priming.
- **"From your devices"** card on Home (sleep / HRV / resting HR) driven by connections + consent.

## 6 · Bilingual EN/ES (customer-facing)
- **Professional Spanish** (tú-form, neutral es) across the web app, the marketing site and the phone prototype — every screen and journey.
- **Language selector:** EN/ES pills in the marketing nav and on the web app login; **Language & region** card in web app Settings (region drives date formats: es-ES/MX/AR/CO/US, en-US/GB/CA/AU).
- Choice persists (`localStorage.ns_locale`) and is **shared across marketing ↔ web app**.
- **Backend stays canonical English**: everything stored in Supabase keeps the canonical values used by the mobile apps, so CAS and analytics are unaffected. Investor/hub materials remain English by design.

## 7 · Decoupled language resources (`i18n/`)
- `i18n/en.json` + `i18n/es.json` hold **every customer-facing string** in three sections: `app` (web application, incl. per-phase content + onboarding), `marketing` (site + phone prototype), `catalog` (English→Spanish lookups for list content).
- Both surfaces **fetch these at page load and merge over built-ins** — copy can be edited on the server with **no rebuild**; missing keys fall back safely.
- Contract, rules and how to add a language: `i18n/README-I18N.md` (in this pack).

## 8 · Mobile-fit fixes (marketing landing)
- Header now wraps on small screens; badge and secondary nav link hidden on phones; global horizontal-overflow guard — landing renders correctly on iPhone-class widths (~400 px) with no offset/overflow.

## 9 · Visual/misc
- NutriSync logos enlarged (2×) across surfaces.
- Health Flows web cards, banner and tabs re-copied to make prototype vs live explicit (EN + ES).

---

### Known configuration notes
- Email confirmation should be **off** in Supabase Auth for a smooth beta.
- To restrict access, front the Cloudflare Pages site with **Zero Trust → Access** (email whitelist) — steps in `README-PUBLISH.md`.
- Editing copy: change `i18n/*.json` values only; never change keys or canonical stored values.
