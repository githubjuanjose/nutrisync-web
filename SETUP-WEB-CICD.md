# Web auto-deploy: GitHub → Cloudflare Pages

Closes **Epic B** — the web app now deploys itself on every push, exactly like the mobile OTA pipeline.

Analogy: the GitHub Action is a *conveyor belt*. You drop a change on `main`, the belt carries the `publish/` folder to Cloudflare, and the site rebuilds itself — no hand-carrying via `wrangler` anymore.

**Flow:** push to `main` → GitHub Action runs `wrangler pages deploy publish` → live at `nutrisync-collective.pages.dev` in ~30s.

---

## What's in this folder
- `publish/` — the site (marketing `index.html`, wired `app.html`, gated `hub/`).
- `.github/workflows/deploy-web.yml` — the auto-deploy Action (deploys `publish/` on push).

---

## One-time setup (~5 min)

### 1. Get your two Cloudflare values

**Account ID** — Cloudflare dashboard → **Workers & Pages** → right-hand sidebar shows **Account ID**. Copy it.

**API token** — Cloudflare → **My Profile → API Tokens → Create Token** → use the **"Edit Cloudflare Pages"** template (or Custom token with permission **Account → Cloudflare Pages → Edit**). Create → copy the token (shown once).

### 2. Create the GitHub repo and push
From this folder:
```
git init
git add .
git commit -m "NutriSync web + auto-deploy pipeline"
git branch -M main
git remote add origin https://github.com/<you>/nutrisync-web.git
git push -u origin main
```
(Create the empty `nutrisync-web` repo on github.com first, no README.)

### 3. Add the two secrets to the repo
GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**. Add exactly these names:

| Secret name | Value |
|---|---|
| `CLOUDFLARE_API_TOKEN` | the token from step 1 |
| `CLOUDFLARE_ACCOUNT_ID` | the account ID from step 1 |

### 4. Done — test it
The first push already triggered a run. Check **Actions** tab → green check = deployed.
To deploy again later, just edit anything under `publish/` and push. Or trigger manually: **Actions → Deploy Web to Cloudflare Pages → Run workflow**.

---

## Notes
- The Cloudflare **Pages project must already exist** and be named `nutrisync-collective` (it does — that's where you deployed manually). If you rename it, update `--project-name` in the workflow.
- This is the **direct-upload** flow (Action → wrangler), *not* Cloudflare's built-in Git integration — deliberately, because the built-in "Workers Builds" flow hung for us earlier. This path is reliable.
- Updating the web app after Design re-exports: drop the new `app.html` into `publish/`, commit, push. Live in seconds.
- To re-add the email whitelist: Cloudflare **Zero Trust → Access → Applications** (unaffected by this pipeline).
