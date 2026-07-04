#!/usr/bin/env python3
"""
NutriSync — one-command re-integration of the "here-only" layer onto a fresh
Design export.

WHY: the web app is a compiled Design bundle. The backend/UX layer we add
(consent banner, admin live-KPI wiring, error-overlay hide, the Translations
review page + hub nav pill, the mobile i18n keys, and the current hub docs)
cannot live inside Design's source, so every fresh export lands WITHOUT it.
This script re-applies all of it in one shot. Idempotent — safe to re-run.

USAGE (from the web repo root, after dropping in a fresh Design `publish/`):
    python3 integrate.py
Then commit + push as usual.

Assets it needs live next to it in ./_integration/ :
    _integration/translations.html      the founder Translations review page
    _integration/docs/*.html            the current hub documentation to overlay
    _integration/mob_keys.json          {"en":{...},"es":{...}} mobile i18n additions
"""
import os, re, json, shutil, sys

ROOT   = os.path.dirname(os.path.abspath(__file__))
PUB    = os.path.join(ROOT, "publish")
ASSETS = os.path.join(ROOT, "_integration")

if not os.path.isdir(PUB):
    sys.exit("✗ No ./publish next to this script. Run from the web repo root.")

# ---------------------------------------------------------------- 1. error-hide + consent
ERRHIDE = '<style id="ns-err-hide">#__bundler_err{display:none!important}</style>'
CONSENT = r'''<style id="ns-consent-css">
#ns-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:99998;background:#fff;border:1px solid #EADFD5;border-radius:16px;box-shadow:0 20px 50px -20px rgba(0,0,0,.35);padding:18px 20px;max-width:640px;margin:0 auto;font-family:'Inter',system-ui,sans-serif;color:#241D1A}
#ns-consent h4{margin:0 0 6px;font-size:15px;font-weight:800}#ns-consent p{margin:0 0 12px;font-size:13px;color:#736862;line-height:1.5}
#ns-consent .row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}#ns-consent button{border:none;border-radius:24px;padding:10px 18px;font-weight:700;font-size:13px;cursor:pointer;font-family:inherit}
#ns-consent .accept{background:linear-gradient(135deg,#E8472A,#F4876F);color:#fff}#ns-consent .reject{background:#F3EBE4;color:#241D1A}#ns-consent .prefs{background:none;color:#C73A20;text-decoration:underline;padding:10px 6px}
#ns-consent .opts{margin:6px 0 12px;display:none}#ns-consent .opt{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:9px 0;border-top:1px solid #F0E7DF;font-size:13px}#ns-consent .opt small{color:#736862;display:block;font-size:11.5px}
</style>
<script id="ns-consent-js">(function(){var KEY="nutrisync.consent.v1";
function have(){try{return JSON.parse(localStorage.getItem(KEY));}catch(e){return null;}}
function save(c){c.ts=new Date().toISOString();c.version=1;try{localStorage.setItem(KEY,JSON.stringify(c));}catch(e){}window.__nsConsent=c;var b=document.getElementById("ns-consent");if(b)b.remove();}
function build(){if(have()){window.__nsConsent=have();return;}var d=document.createElement("div");d.id="ns-consent";
d.innerHTML='<h4>Your privacy</h4><p>We use essential cookies to run NutriSync. Optional analytics &amp; personalization help us improve — they are <b>off by default</b>.</p>'
+'<div class="opts" id="ns-opts"><div class="opt"><span>Essential<small>Required for the app to work</small></span><span>Always on</span></div>'
+'<div class="opt"><span>Analytics<small>Anonymous usage to fix bugs</small></span><input type="checkbox" id="ns-an"></div>'
+'<div class="opt"><span>Personalization<small>Tailors tips to your patterns</small></span><input type="checkbox" id="ns-pe"></div></div>'
+'<div class="row"><button class="accept" id="ns-accept">Accept all</button><button class="reject" id="ns-reject">Reject non-essential</button><button class="prefs" id="ns-prefs">Preferences</button></div>';
document.body.appendChild(d);
document.getElementById("ns-accept").onclick=function(){save({essential:true,analytics:true,personalization:true});};
document.getElementById("ns-reject").onclick=function(){save({essential:true,analytics:false,personalization:false});};
document.getElementById("ns-prefs").onclick=function(){var o=document.getElementById("ns-opts");if(o.style.display==="block"){save({essential:true,analytics:document.getElementById("ns-an").checked,personalization:document.getElementById("ns-pe").checked});}else{o.style.display="block";this.textContent="Save preferences";}};}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",build);else build();})();</script>'''
for f in ("index.html", "app.html"):
    p = os.path.join(PUB, f)
    if not os.path.exists(p):
        continue
    s = open(p, encoding="utf-8").read(); add = ""
    if "ns-err-hide" not in s: add += ERRHIDE
    if "ns-consent-css" not in s: add += CONSENT
    if add:
        open(p, "w", encoding="utf-8").write(s.replace("</head>", add + "</head>", 1))
        print("• consent/error-hide →", f)

# ---------------------------------------------------------------- 2. admin live-KPI wiring
app = open(os.path.join(PUB, "app.html"), encoding="utf-8").read()
URL = re.search(r"https://[a-z0-9]+\.supabase\.co", app).group(0)
KEY = re.search(r"sb_publishable_[^'\"]+", app).group(0)
adm = os.path.join(PUB, "hub", "admin-mis-console.html")
if os.path.exists(adm):
    h = open(adm, encoding="utf-8").read()
    if "admin_kpis" not in h:
        for lab, i in (("Total users", "kTotal"), ("DAU", "kDau"), ("WAU", "kWau"), ("MAU", "kMau")):
            h = re.sub(r'(<div class="lab">' + lab + r'</div><div class="val"[^>]*>)', r'\1', h)  # keep as-is
        h = h.replace('<div class="lab">Total users</div><div class="val">12,480</div>', '<div class="lab">Total users</div><div class="val" id="kTotal">12,480</div>')
        h = h.replace('<div class="lab">DAU</div><div class="val" style="font-size:22px;">3,210</div>', '<div class="lab">DAU</div><div class="val" style="font-size:22px;" id="kDau">3,210</div>')
        h = h.replace('<div class="lab">WAU</div><div class="val" style="font-size:22px;">8,940</div>', '<div class="lab">WAU</div><div class="val" style="font-size:22px;" id="kWau">8,940</div>')
        h = h.replace('<div class="lab">MAU</div><div class="val" style="font-size:22px;">11,200</div>', '<div class="lab">MAU</div><div class="val" style="font-size:22px;" id="kMau">11,200</div>')
        WIRE = ('<div id="adminLogin" style="display:none;position:fixed;inset:0;z-index:500;background:rgba(28,23,21,.55);align-items:center;justify-content:center;"><div style="background:#fff;border-radius:18px;padding:26px 24px;max-width:340px;width:92%">'
          '<div style="font-weight:800;font-size:17px;margin-bottom:4px">Admin sign-in</div><div style="color:#736862;font-size:13px;margin-bottom:14px">Live KPIs are for registered admins only.</div>'
          '<input id="admEmail" type="email" placeholder="Email" style="width:100%;padding:11px 13px;border:1px solid #EADFD5;border-radius:10px;margin-bottom:8px;font-size:14px"/>'
          '<input id="admPass" type="password" placeholder="Password" style="width:100%;padding:11px 13px;border:1px solid #EADFD5;border-radius:10px;font-size:14px"/>'
          '<button id="admGo" class="btn btn-primary" style="width:100%;justify-content:center;margin-top:12px">Sign in</button><div id="admErr" style="color:#C73A20;font-size:12.5px;min-height:16px;margin-top:8px"></div></div></div>'
          '<script type="module">\n' + f"const U='{URL}',K='{KEY}';\n" +
          "import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';const sb=createClient(U,K);const $=i=>document.getElementById(i);\n"
          "function rA(a){const b=$('accessBars');if(!b||!a||!a.length)return;const m=Math.max(1,...a),t=new Date();b.innerHTML=a.map((v,i)=>{const d=new Date(t);d.setDate(t.getDate()-(a.length-1-i));return `<div class=\"barcol\"><div style=\"flex:1;display:flex;align-items:flex-end;width:60%\"><div class=\"bar\" style=\"width:100%;height:${v/m*100}%;background:linear-gradient(to top,var(--coral),var(--peach))\"></div></div><div class=\"barlabel\">${d.toLocaleDateString(undefined,{weekday:'short'})}</div></div>`;}).join('');b.dataset.built='1';}\n"
          "async function L(){const{data:{session}}=await sb.auth.getSession();if(!session){$('adminLogin').style.display='flex';return;}const{data,error}=await sb.rpc('admin_kpis');if(error)return;const n=x=>Number(x).toLocaleString('en-US');['kTotal','total_users','kDau','dau','kWau','wau','kMau','mau'];if($('kTotal'))$('kTotal').textContent=n(data.total_users);if($('kDau'))$('kDau').textContent=n(data.dau);if($('kWau'))$('kWau').textContent=n(data.wau);if($('kMau'))$('kMau').textContent=n(data.mau);rA(data.daily_active);}\n"
          "$('admGo')&&$('admGo').addEventListener('click',async()=>{$('admErr').textContent='';const{error}=await sb.auth.signInWithPassword({email:$('admEmail').value.trim(),password:$('admPass').value});if(error){$('admErr').textContent=error.message;return;}$('adminLogin').style.display='none';L();});L();</script>\n")
        h = h.replace("</body>", WIRE + "</body>", 1)
        open(adm, "w", encoding="utf-8").write(h)
        print("• admin live-KPI wiring → hub/admin-mis-console.html")

# ---------------------------------------------------------------- 3. mobile i18n keys (app.mob)
mk = os.path.join(ASSETS, "mob_keys.json")
if os.path.exists(mk):
    MOB = json.load(open(mk, encoding="utf-8"))
    for lang in ("en", "es"):
        p = os.path.join(PUB, "i18n", lang + ".json")
        if os.path.exists(p):
            d = json.load(open(p, encoding="utf-8"))
            d.setdefault("app", {}).setdefault("mob", {}).update(MOB.get(lang, {}))
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("• mobile i18n keys → i18n/en.json, es.json")

# ---------------------------------------------------------------- 4. translations page + hub pill
tp = os.path.join(ASSETS, "translations.html")
if os.path.exists(tp):
    shutil.copy(tp, os.path.join(PUB, "hub", "translations.html"))
    hub = os.path.join(PUB, "hub", "full-hub-gated-site.html")
    if os.path.exists(hub):
        s = open(hub, encoding="utf-8").read()
        if "translations.html" not in s:
            old = '<button class="htab" id="bt2" onclick="bldTab(2)">📚 Project documentation</button>'
            pill = '<a class="htab" href="translations.html" target="_blank" style="text-decoration:none;display:inline-flex;align-items:center">🌐 Translations (EN/ES)</a>'
            if old in s:
                open(hub, "w", encoding="utf-8").write(s.replace(old, old + "\n      " + pill, 1))
    print("• Translations page + hub nav pill")

# ---------------------------------------------------------------- 5. overlay current hub docs
dd = os.path.join(ASSETS, "docs")
if os.path.isdir(dd):
    dst = os.path.join(PUB, "hub", "documentation")
    os.makedirs(dst, exist_ok=True)
    n = 0
    for f in os.listdir(dd):
        if f.endswith(".html"):
            shutil.copy(os.path.join(dd, f), os.path.join(dst, f)); n += 1
    print(f"• overlaid {n} hub documents")

print("\n✓ Integration complete — review, then commit + push.")
