# NutriSync — Release Notes / Change Log

## 2026-07-06 — German marketing site live
- **The marketing page (and the phone prototype inside it) is now fully translated in German** — `i18n/de.json` carries the `marketing` (283 keys) and `catalog` (335 entries) sections, same contract as French. Data-only change; no rebuild.
- Marketing live: EN, ES, FR, DE · web-app live: EN, ES, FR, DE, IT, NL, EL · next: IT/NL/EL marketing, then CA, EU, OC, VAL, GL, ZH, JA packs.

## 2026-07-06 — French marketing site live
- **The marketing page (and the phone prototype inside it) is now fully translated in French** — `i18n/fr.json` carries the `marketing` (283 keys) and `catalog` (335 entries) sections. Picking FR translates hero, sections, pricing, footer, gallery cards and prototype screens; Investor & Builder rooms stay EN/ES by design.
- The last hardcoded ES/EN copy in the marketing engine (science section, Nutri intro, check-in gate, calendars, tip labels) now routes through the language packs — German, Italian, Dutch and Greek marketing sections can ship as data only.

## 2026-07-06 — Marketing selector parity
- Language pills and dropdown now show **ISO codes** (EN · ES · FR · DE · IT · NL · EL …) instead of full names, on both the marketing site and the web app.
- The marketing page's language selector matches the web app: [EN] + [OS language / ES] pills and a ▾ dropdown listing every language the web app supports. Picking one applies it across site ↔ app (shared `ns_locale`).
- Transitional: marketing-page copy falls back to English for languages whose marketing translation hasn't shipped yet — those sections are rolling out per language. Investor & Builder rooms remain English/Spanish by design.

## 2026-07-06 — Selector: Español as standing second pill
- When the device/OS language is English (or not yet supported), the second pill now defaults to **Español** instead of leaving a lone English pill with Spanish tucked in the dropdown. Two pills are always visible: [English] + [OS language, or Español].

## 2026-07-06 — Languages: Dutch & Greek live · registry grows to 14
- **Dutch (Nederlands) and Greek (Ελληνικά) are live in the web app** (`i18n/nl.json`, `i18n/el.json`).
- **Chinese (中文, continental) and Japanese (日本語) added to the supported set** — 14 languages total; each appears in the selector once its pack ships.
- Shipped: EN, ES, FR, DE, IT, NL, EL · pending: CA, EU, OC (Aranés), VAL, GL, ZH, JA — plus marketing-site sections per language (marketing page gates to EN/ES until then). Investor & Builder rooms stay EN/ES by design.

## 2026-07-06 — Hotfix: marketing page load error · Italian live
- **Fixed `index.html` failing to boot** ("Unexpected token ':'") — a malformed expression introduced with the 12-language registry in the marketing logic; both bundles now compile-checked before packaging.
- **Italian (Italiano) is live in the web app** (`i18n/it.json`). Shipped: EN, ES, FR, DE, IT · pending: NL, EL, CA, EU, OC, VAL, GL.

## 2026-07-06 — Languages: registry grows to 12 · German live
- **Supported set is now 12 languages:** Aranés, Català, Deutsch, English, Español, Euskara, Français, Galego, Italiano, Nederlands, Valencià, Ελληνικά. Each appears in the selector automatically once its `i18n/<code>.json` pack ships.
- **German (Deutsch) is live in the web app** — full professional du-form translation (`i18n/de.json`). Shipped packs so far: EN, ES (built-in), FR, DE. Pending: IT, NL, EL, CA, EU, OC, VAL, GL — plus the marketing-site sections per language.
- Scope confirmed: language packs are shared across web and mobile apps and cover both prototypes; **Investor & Builder rooms stay English/Spanish only**.

## 2026-07-06 — Languages: 7-language system + new selector
- **Language selector (marketing nav, web-app login, Settings):** two pills always visible — **[English] + [OS language]** — with a **▾ dropdown** listing the remaining supported languages alphabetically (Deutsch, Español, Français, Italiano, Nederlands, Ελληνικά). Picking from the dropdown applies the language and takes the second pill's slot. Choice persists (`ns_locale`), shared web ↔ app; backend values stay canonical English.
- **OS-language default:** first load with no saved choice follows the device language when supported.
- **French (Français) is live in the web app** — full professional translation (`i18n/fr.json`), covering auth, onboarding, daily loop, phase content, wearables, privacy & security. German, Italian, Dutch and Greek packs — and the marketing-site translations — land next; each appears in the selector automatically once its pack ships.
- i18n architecture: languages load as decoupled `i18n/<code>.json` packs (no rebuild needed); missing keys fall back to English.

## 2026-07-06 — Navigation & polish (dev-brief fixes, at source)
- **Web app · Back to site:** persistent controls — sidebar item (icon + label, collapses with the rail), a floating "← Back to site" pill fixed at the **bottom-right corner** of the auth/onboarding screens (also on mobile), and a Back-to-site row next to Log out in Settings. Replaces the stopgap floating button.
- **Web app · bigger back controls:** all in-app back links (‹ Today, ‹ Settings, ‹ Connections) are now 44px-tall pills; onboarding back is 44px with a 24px chevron.
- **Web onboarding:** Back on every step, new "Start over" (resets to step 1 and clears answers), and the browser Back button now steps the wizard back instead of leaving the flow.
- **Hub deeper back paths:** room/tab changes push history — the browser Back button steps within the hub (tab → room → landing) instead of dropping straight to the landing.
- **Bundler error overlay — root-caused, not just hidden:** the overlay only fires on a real resource miss. The one genuine miss (a Figma-typo'd mood icon, `mischevious` → `mischievous`) was fixed at source in a prior build; this build's audit confirms every dynamically-referenced asset (12 mood-face pairs, 4 phase dials, 3 Nutri bubbles, avatars, stars, check states) is declared in the bundle manifest, and both `index.html` and `app.html` load with zero console errors. The 6 "asset not found: {{ … }}" messages at export time are compile-time noise (template holes), not runtime failures. The `#__bundler_err { display:none }` rule is retained deliberately as a production safety net — a debug overlay should never reach end users even if an asset regresses — but nothing triggers it today.

## 2026-07-06 — Hub room navigation
- **Sticky room tabs:** Overview / Business case / MIS (Investors) and Overview / Documentation / Admin·MIS / Backlog (Builders) now live inside the sticky room header — always visible while scrolling any document; switching a tab returns you to the top.
- **Room switcher in header:** Investors · Builders · ← Back to site — jump Investor↔Builder directly without returning to the landing page.
- **Back control:** "← Overview" (and the active room pill) returns to that room's Overview; only "← Back to site" exits to the landing.
- **Gate at entry only:** the 123456 access gate appears when entering the hub from the site; switching rooms or tabs inside never re-locks.

## 2026-07-04 — Footer & branding
- **Footer redesign (slimmer, 3 rows):**
  - Row 1 — brand block (logo + paragraph + **Team Access**: Investors / Builders chips side by side) next to Product · Company · Legal columns.
  - Row 2 — single "STAY IN SYNC" bar: newsletter email + orange button, **App Store / Google Play badges and Instagram · LinkedIn · TikTok all on one line**.
  - Row 3 — one-line disclaimer.
- **Logo prominence:** header logo enlarged to 50 px with a larger NUTRISYNC wordmark on the main page.

---

**Package date:** July 4, 2026 · **Contents:** `index.html` (marketing) + `app.html` (web application) + `i18n/` (language resources) + `hub/` (team documents) + `assets/`

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
