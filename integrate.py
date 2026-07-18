#!/usr/bin/env python3
"""
NutriSync — one-command re-integration of the "here-only" layer onto a fresh
Design export. Re-applies: error-overlay hide, consent banner, admin live-KPI
wiring, mobile i18n keys, the Translations review page + hub nav pill, and the
current hub documentation. Idempotent — safe to re-run.

USAGE (from the web repo root, after dropping in a fresh Design `publish/`):
    python3 integrate.py

Assets it needs live next to it in ./_integration/ :
    _integration/translations.html   the founder Translations review page
    _integration/docs/*.html         the current hub documentation to overlay
    _integration/mob_keys.json       {"en":{...},"es":{...}} mobile i18n additions
"""
# ---------------------------------------------------------------------------
# WEB → MOBILE crossover rule (what to also do to the native app per web pack):
#   Design packs are WEB-ONLY (no mobile code). For each pack, check:
#     • Marketing footer / hero / web-app chrome  -> web-only, mobile untouched
#     • Wording in the shared i18n `app` section   -> re-sync into mobile bundle
#     • Brand tokens (phase colours, brand orange)  -> apply to mobile theme.ts
#     • A new product screen/feature in the design  -> build natively in the RN app
#   Only touch the mobile app (and ship nutrisync-app-full.zip OTA) when something
#   actually crosses over. Full rule + log: hub docs -> "Change Log — Web & App".
# ---------------------------------------------------------------------------
import os, re, json, shutil, sys

ROOT   = os.path.dirname(os.path.abspath(__file__))
PUB    = os.path.join(ROOT, "publish")
ASSETS = os.path.join(ROOT, "_integration")
if not os.path.isdir(PUB):
    sys.exit("No ./publish next to this script. Run from the web repo root.")

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
d.innerHTML='<h4>Your privacy</h4><p>We use essential cookies to run NutriSync. Optional analytics &amp; personalization help us improve - they are <b>off by default</b>.</p>'
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
    if not os.path.exists(p): continue
    s = open(p, encoding="utf-8", errors="ignore").read(); add = ""
    if "ns-err-hide" not in s: add += ERRHIDE
    if "ns-consent-css" not in s: add += CONSENT
    if add:
        open(p, "w", encoding="utf-8").write(s.replace("</head>", add + "</head>", 1)); print("- consent/error-hide:", f)

# admin live-KPI wiring
app = open(os.path.join(PUB, "app.html"), encoding="utf-8").read()
URL = re.search(r"https://[a-z0-9]+\.supabase\.co", app).group(0)
KEY = re.search(r"sb_publishable_[^'\"]+", app).group(0)

# marketing waitlist + newsletter capture -> public.waitlist (index.html only).
# Compiled-bundle handlers ({{ onEmail }}/{{ subscribeNl }}) are not rewireable
# from outside, so we delegate on document (capture phase, survives re-renders):
# on any button click, grab the sibling <input>'s email and POST it via PostgREST
# with the public anon key (RLS "anyone can join waitlist" insert policy allows it).
idx = os.path.join(PUB, "index.html")
if os.path.exists(idx):
    ih = open(idx, encoding="utf-8").read()
    if "ns-waitlist-js" not in ih:
        WL = ('<script id="ns-waitlist-js">(function(){var U="__U__",K="__K__";'
          'function v(e){return /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(e);}'
          'function toast(m){var t=document.createElement("div");t.textContent=m;'
          't.style.cssText="position:fixed;left:50%;bottom:26px;transform:translateX(-50%);z-index:99999;'
          'background:#241D1A;color:#fff;font-family:\'Inter\',system-ui,sans-serif;font-size:13.5px;'
          'font-weight:600;padding:11px 18px;border-radius:24px;box-shadow:0 14px 30px -12px rgba(0,0,0,.5);'
          'opacity:0;transition:opacity .25s";document.body.appendChild(t);'
          'requestAnimationFrame(function(){t.style.opacity="1";});'
          'setTimeout(function(){t.style.opacity="0";setTimeout(function(){t.remove();},300);},2600);}'
          'document.addEventListener("click",function(e){'
          'var btn=e.target.closest&&e.target.closest("button,[role=button]");if(!btn)return;'
          'var input=null,node=btn,i;for(i=0;i<4&&node;i++){node=node.parentElement;'
          'if(node){input=node.querySelector("input");if(input)break;}}'
          'if(!input)return;var email=(input.value||"").trim().toLowerCase();if(!v(email))return;'
          # W14: explicit GDPR consent — checkbox injected next to the input, submission gated on it
          'var box=input.parentElement&&input.parentElement.parentElement;'
          'var cb=box&&box.querySelector(".ns-consent-cb");'
          'if(!cb&&box){var w=document.createElement("label");'
          'w.style.cssText="display:flex;gap:8px;align-items:flex-start;margin-top:10px;font-size:11.5px;line-height:1.45;color:#8d827a;font-family:Inter,system-ui,sans-serif;cursor:pointer;text-align:left";'
          'w.innerHTML=\'<input type="checkbox" class="ns-consent-cb" style="margin-top:2px;accent-color:#EA5740"/>'
          '<span>Yes, I want NutriSync updates \\u2014 launch news, cycle-nutrition tips, and first access to the app. Unsubscribe anytime.<\\u002Fspan>\';'
          'box.appendChild(w);cb=w.querySelector(".ns-consent-cb");'
          'toast("One more step \\u2014 please tick the consent box");btn.__nsSent=null;return;}'
          'if(cb&&!cb.checked){toast("Please tick the consent box first");btn.__nsSent=null;return;}'
          'if(btn.__nsSent===email)return;btn.__nsSent=email;'
          'var src=/you@email\\.com/.test(input.placeholder||"")?"newsletter":"marketing_site";'
          'fetch(U+"/rest/v1/waitlist",{method:"POST",headers:{"apikey":K,"Authorization":"Bearer "+K,'
          '"Content-Type":"application/json","Prefer":"return=minimal"},'
          'body:JSON.stringify({email:email,source:src})}).then(function(r){'
          'if(r.status===201){toast("You\'re on the list \\u2713");}'
          'else if(r.status===409){toast("You\'re already subscribed \\u2713");}'
          'else{btn.__nsSent=null;}}).catch(function(){btn.__nsSent=null;});},true);})();</script>')
        WL = WL.replace("__U__", URL).replace("__K__", KEY)
        open(idx, "w", encoding="utf-8").write(ih.replace("</head>", WL + "</head>", 1))
        print("- marketing waitlist/newsletter capture (index.html)")

# Builders room "Founder Tools" header row (Waitlist / Translations / Change Log).
# These are TOOLS, not documents, so they belong at the room-header level, not inside
# the Documentation tab. The compiled bundle's room tabs (Overview/Documentation/
# Admin·MIS/Backlog) aren't rewireable, so we inject a card row right under the
# Builders tab bar (anchored via the unique "Admin · MIS" button) and keep it in
# place across the bundle's re-renders with a MutationObserver.
if os.path.exists(idx):
    ih = open(idx, encoding="utf-8").read()
    if "ns-founder-tools" not in ih:
        FT = ('<script id="ns-founder-tools">(function(){'
          'var C=[{h:"hub/prototypes.html",e:"\\uD83D\\uDCF1",t:"Prototypes",d:"Interactive app flows",'
          'bg:"linear-gradient(135deg,#6D28D9,#8B5CF6)"},'
          '{h:"hub/waitlist.html",e:"\\uD83D\\uDCCB",t:"Waitlist",d:"Signups + CSV export",'
          'bg:"linear-gradient(135deg,#0FA968,#12C07A)"},'
          '{h:"hub/review.html",e:"\\u2705",t:"Review",d:"Founders\\u2019 checklist",'
          'bg:"linear-gradient(135deg,#B7791F,#D69E2E)"},'
          '{h:"hub/translations.html",e:"\\uD83C\\uDF10",t:"Translations",d:"14-language review",'
          'bg:"linear-gradient(135deg,#E8472A,#F4876F)"},'
          '{h:"hub/documentation/08-Change-Log.html",e:"\\uD83E\\uDDFE",t:"Change Log",'
          'd:"Web & app changes",bg:"#241D1A"}];'
          'function card(x){return \'<a href="\'+x.h+\'" style="flex:1;min-width:150px;'
          'display:flex;align-items:center;gap:10px;text-decoration:none;background:\'+x.bg+\';color:#fff;'
          'border-radius:14px;padding:13px 15px;box-shadow:0 12px 26px -16px rgba(0,0,0,.5)">'
          '<span style="font-size:20px">\'+x.e+\'</span><span><span style="font-weight:800;font-size:14px;'
          'display:block">\'+x.t+\'</span><span style="font-size:11.5px;opacity:.92">\'+x.d+\'</span></span></a>\';}'
          'function build(){if(document.getElementById("ns-ft-row"))return;'
          'var bs=document.querySelectorAll("button"),mis=null,i;'
          'for(i=0;i<bs.length;i++){if(/Admin\\s*[\\u00B7.]\\s*MIS/.test(bs[i].textContent||"")){mis=bs[i];break;}}'
          'if(!mis)return;var bar=mis.parentElement;if(!bar||!bar.parentElement)return;'
          'var row=document.createElement("div");row.id="ns-ft-row";row.style.cssText="margin:14px 0 6px";'
          'row.innerHTML=\'<div style="font-size:12px;letter-spacing:.14em;font-weight:700;color:#E8472A;'
          'margin:0 0 10px">FOUNDER TOOLS</div><div style="display:flex;gap:12px;flex-wrap:wrap">\''
          '+C.map(card).join("")+\'</div>\';bar.parentElement.insertBefore(row,bar.nextSibling);}'
          'var o=new MutationObserver(function(){build();});'
          'function start(){build();o.observe(document.body,{childList:true,subtree:true});}'
          'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);else start();'
          '})();</script>')
        open(idx, "w", encoding="utf-8").write(ih.replace("</head>", FT + "</head>", 1))
        print("- Builders 'Founder Tools' header row (index.html)")

# Web app → "Back to site" exit. The compiled app.html has no route back to the
# marketing site (index.html). We inject a small persistent link (kept in place with
# a MutationObserver) — it just navigates to the sibling index.html, no bundle rewire.
ap = os.path.join(PUB, "app.html")
if os.path.exists(ap):
    ap_s = open(ap, encoding="utf-8").read()
    # Only inject the stopgap if Design's export has no native "Back to site" control.
    # (Design added native exits in the 0607v02.53 pack, so this now no-ops.)
    if "ns-exit-site" not in ap_s and "Back to site" not in ap_s:
        EX = ('<script id="ns-exit-site">(function(){'
          'function add(){if(document.getElementById("ns-exit-btn"))return;'
          'var a=document.createElement("a");a.id="ns-exit-btn";a.href="index.html";'
          'a.title="Back to the NutriSync marketing site";a.innerHTML="\\u2190\\u00A0Back to site";'
          'a.style.cssText="position:fixed;top:12px;right:14px;z-index:2147483000;'
          'background:#EA5740;color:#fff;font-family:\'Inter\',system-ui,sans-serif;'
          'font-size:14px;font-weight:800;text-decoration:none;padding:10px 17px;border-radius:24px;'
          'box-shadow:0 8px 22px -8px rgba(0,0,0,.55);border:2px solid #fff;line-height:1;white-space:nowrap";'
          'document.body.appendChild(a);}'
          'var o=new MutationObserver(function(){add();});'
          'function start(){add();o.observe(document.body,{childList:true});}'
          'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);else start();'
          '})();</script>')
        open(ap, "w", encoding="utf-8").write(ap_s.replace("</head>", EX + "</head>", 1))
        print("- Web app 'Back to site' exit link (app.html)")

# The site is public — strip the "Demo access — use code 123456" hint from the
# hub gates (the 123456 code still works; it's just no longer advertised on-screen).
if os.path.exists(idx):
    ih = open(idx, encoding="utf-8").read()
    new = re.sub(r'Demo access[\s\S]{0,240}?use code 123456<\\u002Fbutton>', '', ih)
    new = re.sub(r'Demo access[\s\S]{0,240}?use code 123456</button>', '', new)
    if new != ih:
        open(idx, "w", encoding="utf-8").write(new); print("- removed public demo-code hint")

adm = os.path.join(PUB, "hub", "admin-mis-console.html")
if os.path.exists(adm):
    h = open(adm, encoding="utf-8").read()
    if "admin_kpis" not in h:
        h = h.replace('<div class="lab">Total users</div><div class="val">12,480</div>', '<div class="lab">Total users</div><div class="val" id="kTotal">12,480</div>')
        h = h.replace('<div class="lab">DAU</div><div class="val" style="font-size:22px;">3,210</div>', '<div class="lab">DAU</div><div class="val" style="font-size:22px;" id="kDau">3,210</div>')
        h = h.replace('<div class="lab">WAU</div><div class="val" style="font-size:22px;">8,940</div>', '<div class="lab">WAU</div><div class="val" style="font-size:22px;" id="kWau">8,940</div>')
        h = h.replace('<div class="lab">MAU</div><div class="val" style="font-size:22px;">11,200</div>', '<div class="lab">MAU</div><div class="val" style="font-size:22px;" id="kMau">11,200</div>')
        WIRE = ('<div id="adminLogin" style="display:none;position:fixed;inset:0;z-index:500;background:rgba(28,23,21,.55);align-items:center;justify-content:center;"><div style="background:#fff;border-radius:18px;padding:26px 24px;max-width:340px;width:92%">'
          '<div style="font-weight:800;font-size:17px;margin-bottom:4px">Admin sign-in</div><div style="color:#736862;font-size:13px;margin-bottom:14px">Live KPIs are for registered admins only.</div>'
          '<input id="admEmail" type="email" placeholder="Email" style="width:100%;padding:11px 13px;border:1px solid #EADFD5;border-radius:10px;margin-bottom:8px;font-size:14px"/>'
          '<input id="admPass" type="password" placeholder="Password" style="width:100%;padding:11px 13px;border:1px solid #EADFD5;border-radius:10px;font-size:14px"/>'
          '<button id="admGo" class="btn btn-primary" style="width:100%;justify-content:center;margin-top:12px">Sign in</button><div id="admErr" style="color:#C73A20;font-size:12.5px;min-height:16px;margin-top:8px"></div></div></div>'
          '<script type="module">\n' + "const U='%s',K='%s';\n" % (URL, KEY) +
          "import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';const sb=createClient(U,K);const $=i=>document.getElementById(i);\n"
          "function rA(a){const b=$('accessBars');if(!b||!a||!a.length)return;const m=Math.max(1,...a),t=new Date();b.innerHTML=a.map((v,i)=>{const d=new Date(t);d.setDate(t.getDate()-(a.length-1-i));return `<div class=\"barcol\"><div style=\"flex:1;display:flex;align-items:flex-end;width:60%\"><div class=\"bar\" style=\"width:100%;height:${v/m*100}%;background:linear-gradient(to top,var(--coral),var(--peach))\"></div></div><div class=\"barlabel\">${d.toLocaleDateString(undefined,{weekday:'short'})}</div></div>`;}).join('');b.dataset.built='1';}\n"
          "async function L(){const{data:{session}}=await sb.auth.getSession();if(!session){$('adminLogin').style.display='flex';return;}const{data,error}=await sb.rpc('admin_kpis');if(error)return;const n=x=>Number(x).toLocaleString('en-US');if($('kTotal'))$('kTotal').textContent=n(data.total_users);if($('kDau'))$('kDau').textContent=n(data.dau);if($('kWau'))$('kWau').textContent=n(data.wau);if($('kMau'))$('kMau').textContent=n(data.mau);rA(data.daily_active);}\n"
          "$('admGo')&&$('admGo').addEventListener('click',async()=>{$('admErr').textContent='';const{error}=await sb.auth.signInWithPassword({email:$('admEmail').value.trim(),password:$('admPass').value});if(error){$('admErr').textContent=error.message;return;}$('adminLogin').style.display='none';L();});L();</script>\n")
        h = h.replace("</body>", WIRE + "</body>", 1)
        open(adm, "w", encoding="utf-8").write(h); print("- admin live-KPI wiring")

mk = os.path.join(ASSETS, "mob_keys.json")
if os.path.exists(mk):
    MOB = json.load(open(mk, encoding="utf-8"))
    for lang in ("en", "es"):
        p = os.path.join(PUB, "i18n", lang + ".json")
        if os.path.exists(p):
            d = json.load(open(p, encoding="utf-8")); d.setdefault("app", {}).setdefault("mob", {}).update(MOB.get(lang, {}))
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("- mobile i18n keys")

tp = os.path.join(ASSETS, "translations.html")
if os.path.exists(tp):
    shutil.copy(tp, os.path.join(PUB, "hub", "translations.html"))
    hub = os.path.join(PUB, "hub", "full-hub-gated-site.html")
    if os.path.exists(hub):
        s = open(hub, encoding="utf-8").read()
        if "translations.html" not in s:
            old = '<button class="htab" id="bt2" onclick="bldTab(2)">📚 Project documentation</button>'
            pill = '<a class="htab" href="translations.html" target="_blank" style="text-decoration:none;display:inline-flex;align-items:center">🌐 Translations (EN/ES)</a>'
            if old in s: open(hub, "w", encoding="utf-8").write(s.replace(old, old + "\n      " + pill, 1))
    print("- Translations page + hub pill")

# Founders' review checklist (static, no backend).
rv = os.path.join(ASSETS, "review.html")
if os.path.exists(rv):
    shutil.copy(rv, os.path.join(PUB, "hub", "review.html"))
    print("- Founders' review checklist page")

# Founders' waitlist dashboard (admin-gated read via admin_waitlist RPC).
wl = os.path.join(ASSETS, "waitlist.html")
if os.path.exists(wl):
    w = open(wl, encoding="utf-8").read().replace("__NS_URL__", URL).replace("__NS_KEY__", KEY)
    open(os.path.join(PUB, "hub", "waitlist.html"), "w", encoding="utf-8").write(w)
    hub = os.path.join(PUB, "hub", "full-hub-gated-site.html")
    if os.path.exists(hub):
        s = open(hub, encoding="utf-8").read()
        if "waitlist.html" not in s:
            old = '<button class="htab" id="bt2" onclick="bldTab(2)">📚 Project documentation</button>'
            pill = '<a class="htab" href="waitlist.html" target="_blank" style="text-decoration:none;display:inline-flex;align-items:center">📋 Waitlist</a>'
            if old in s: open(hub, "w", encoding="utf-8").write(s.replace(old, old + "\n      " + pill, 1))
    print("- Waitlist dashboard + hub pill")

dd = os.path.join(ASSETS, "docs")
if os.path.isdir(dd):
    dst = os.path.join(PUB, "hub", "documentation"); os.makedirs(dst, exist_ok=True); n = 0
    for f in os.listdir(dd):
        if f.endswith(".html"): shutil.copy(os.path.join(dd, f), os.path.join(dst, f)); n += 1
    print("- overlaid %d hub documents" % n)

# ── Prototypes: moved OUT of the public marketing site, INTO the Builders area. ──
# The marketing bundle's "HEALTH FLOWS / See NutriSync in action" showcase is a
# single <section id="screens"> (plus nav/hero/footer links to "#screens"). It's
# prototype material, so we (1) strip that section and its "#screens" links from the
# PUBLIC site at runtime, and (2) publish a gated hub/prototypes.html that deep-links
# every screen of the working prototype (app.html#demo-<route>).
PROTO_GROUPS = [
    ("Onboarding & sign-up", [("login", "Log in"), ("signup", "Create account"), ("onboarding", "Onboarding wizard"), ("allset", "All set")]),
    ("Daily experience", [("gate", "Daily check-in gate"), ("home", "Home · Cycle Alignment Score"), ("nutrilog", "NutriLog"), ("movement", "Movement")]),
    ("Tracking", [("editperiod", "Edit period"), ("edithealth", "Edit health"), ("progress", "Progress"), ("calendar", "Calendar")]),
    ("Account & privacy", [("settings", "Settings"), ("connections", "Connections"), ("privacy", "Privacy"), ("security", "Security")]),
]
_pg = ""
for _title, _items in PROTO_GROUPS:
    _cards = "".join(
        '<a class="pcard" href="../app.html#demo-%s"><span class="pdot"></span>'
        '<span class="plabel">%s</span><span class="parrow">→</span></a>' % (r, lbl)
        for r, lbl in _items)
    _pg += '<div class="pgroup"><div class="pgtitle">%s</div><div class="pgrid">%s</div></div>' % (_title, _cards)
PROTO_HTML = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1">'
    '<title>Prototypes · NutriSync</title><style>'
    ':root{--coral:#E8472A;--ink:#231F20;--muted:#6B615C;}'
    '*{box-sizing:border-box}body{margin:0;font-family:Poppins,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;'
    'color:var(--ink);background:radial-gradient(circle at 28% 16%,#FDE2D6 0%,#FBEFE6 36%,#FFF8F1 62%,#F9D7BD 100%);min-height:100vh}'
    '.wrap{max-width:860px;margin:0 auto;padding:28px 22px 60px}'
    '.back{display:inline-block;color:var(--muted);text-decoration:none;font-size:14px;font-weight:600;margin-bottom:18px}'
    '.back:hover{color:var(--ink)}'
    '.label{font-size:12px;letter-spacing:.16em;font-weight:700;color:var(--coral)}'
    'h1{font-size:clamp(26px,4vw,38px);margin:8px 0 8px;line-height:1.05}'
    '.lead{color:var(--muted);font-size:15px;line-height:1.55;max-width:560px;margin:0 0 18px}'
    '.enter{display:inline-flex;align-items:center;gap:8px;background:linear-gradient(135deg,#EA5740,#F4876F);color:#fff;'
    'text-decoration:none;font-weight:700;font-size:15px;padding:13px 22px;border-radius:100px;box-shadow:0 12px 26px -14px rgba(234,87,64,.7)}'
    '.pgroup{margin-top:26px}.pgtitle{font-size:12px;letter-spacing:.12em;font-weight:700;color:var(--muted);margin:0 0 10px}'
    '.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}'
    '.pcard{display:flex;align-items:center;gap:11px;background:#fff;border:1px solid #EFE3D7;border-radius:13px;'
    'padding:14px 15px;text-decoration:none;color:var(--ink);box-shadow:0 8px 20px -16px rgba(0,0,0,.4);transition:transform .12s,box-shadow .12s}'
    '.pcard:hover{transform:translateY(-2px);box-shadow:0 14px 28px -14px rgba(0,0,0,.35)}'
    '.pdot{width:9px;height:9px;border-radius:50%;background:var(--coral);flex:none}'
    '.plabel{font-weight:600;font-size:14px;flex:1}.parrow{color:var(--muted);font-weight:700}'
    '.note{margin-top:30px;color:var(--muted);font-size:12.5px;line-height:1.5}'
    '</style></head><body><div class="wrap">'
    '<a class="back" href="full-hub-gated-site.html" onclick="if(history.length>1){history.back();return false;}return true;">‹ Back</a>'
    '<div class="label">PROTOTYPES</div>'
    '<h1>See NutriSync in action.</h1>'
    '<p class="lead">From the first hello to the daily Cycle Alignment Score, step through how NutriSync guides '
    'nutrition, movement and mood across every phase. Each card opens the working prototype on demo data — '
    'full navigation, no account needed.</p>'
    '<a class="enter" href="../app.html">Open the web app prototype →</a>'
    + _pg +
    '<p class="note">Prototype runs on demo data in your browser — nothing here writes to a real account. '
    'This showcase is Builders-only; it is no longer shown on the public marketing site.</p>'
    '</div></body></html>')
open(os.path.join(PUB, "hub", "prototypes.html"), "w", encoding="utf-8").write(PROTO_HTML)
print("- Prototypes hub page (hub/prototypes.html)")

# Strip the HEALTH FLOWS showcase (<section id="screens">) + its #screens links from
# the PUBLIC marketing site, kept in place across re-renders with a MutationObserver.
if os.path.exists(idx):
    ih = open(idx, encoding="utf-8").read()
    if "ns-move-prototypes" not in ih:
        MP = ('<script id="ns-move-prototypes">(function(){'
          'function strip(){var s=document.getElementById("screens");if(s&&s.parentNode)s.parentNode.removeChild(s);'
          'var a=document.querySelectorAll(\'a[href="#screens"]\'),i;for(i=0;i<a.length;i++){if(a[i].parentNode)a[i].parentNode.removeChild(a[i]);}}'
          'var o=new MutationObserver(function(){strip();});'
          'function start(){strip();o.observe(document.body,{childList:true,subtree:true});}'
          'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);else start();'
          '})();</script>')
        open(idx, "w", encoding="utf-8").write(ih.replace("</head>", MP + "</head>", 1))
        print("- removed HEALTH FLOWS showcase from public site (moved to Builders)")

# Prototypes pill on the standalone gated hub nav.
hub = os.path.join(PUB, "hub", "full-hub-gated-site.html")
if os.path.exists(hub):
    s = open(hub, encoding="utf-8").read()
    if "prototypes.html" not in s:
        old = '<button class="htab" id="bt2" onclick="bldTab(2)">📚 Project documentation</button>'
        pill = '<a class="htab" href="prototypes.html" target="_blank" style="text-decoration:none;display:inline-flex;align-items:center">📱 Prototypes</a>'
        if old in s:
            open(hub, "w", encoding="utf-8").write(s.replace(old, old + "\n      " + pill, 1))
            print("- Prototypes pill on gated hub nav")

# ═══════════════ PO Review Round 1 — Iteration 1 (W1 W8 W9 W10 W11 W24f) ═══════════════
# Source: docs/15-PO-Review-Round-1.md. All patches idempotent, applied to the raw
# bundle text (which stores templates as JS strings — quotes appear as \" and
# closing tags as </...>). Non-ASCII replacement text uses JS \uXXXX escapes
# so file encoding never matters.
def _patch(path, pairs, label):
    if not os.path.exists(path): return
    s = open(path, encoding="utf-8", errors="surrogateescape").read()
    orig = s; n = 0
    for pat, rep, isre in pairs:
        if isre:
            s2 = re.sub(pat, rep, s)
        else:
            s2 = s.replace(pat, rep)
        if s2 != s: n += 1
        s = s2
    if s != orig:
        open(path, "w", encoding="utf-8", errors="surrogateescape").write(s)
        print("- %s (%d/%d patches)" % (label, n, len(pairs)))

IDX = os.path.join(PUB, "index.html")
APH = os.path.join(PUB, "app.html")
INV = os.path.join(PUB, "hub", "investors-business-case.html")

# W4 — footer socials: all three live (PO 17/7).
_patch(IDX, [
    (r'<a href=\\"#\\" aria-label=\\"LinkedIn\\"',
     r'<a href=\\"https://www.linkedin.com/company/nutrisync-collective\\" target=\\"_blank\\" rel=\\"noopener\\" aria-label=\\"LinkedIn\\"', True),
    (r'<a href=\\"#\\" aria-label=\\"Instagram\\"',
     r'<a href=\\"https://www.instagram.com/nutrisync.collective/\\" target=\\"_blank\\" rel=\\"noopener\\" aria-label=\\"Instagram\\"', True),
    (r'<a href=\\"#\\" aria-label=\\"TikTok\\"',
     r'<a href=\\"https://www.tiktok.com/@nutrisyncc\\" target=\\"_blank\\" rel=\\"noopener\\" aria-label=\\"TikTok\\"', True),
], "W4 socials complete (LinkedIn + Instagram + TikTok)")

# Access-first entry (18 Jul): the marketing 6-digit gate predates Cloudflare
# Access. Footer Investors/Builders now link STRAIGHT to the hub pages, where
# Access enforces email+PIN at the edge. The hub's inner 123456 gate auto-unlocks
# on the custom domain (Access already authenticated); on any other host it still
# asks the code, and a canonical-host script bounces pages.dev visitors to the
# custom domain anyway (closing the unprotected-alias side door).
if os.path.exists(IDX):
    _s = open(IDX, encoding="utf-8", errors="surrogateescape").read()
    _n = 0
    for _a, _b in (
        ('sc-camel-on-click=\\"{{ openInvestors }}\\"', 'href=\\"hub/investors-business-case.html\\"'),
        ('sc-camel-on-click=\\"{{ openBuilders }}\\"', 'href=\\"hub/full-hub-gated-site.html\\"'),
    ):
        if _a in _s:
            _s = _s.replace(_a, _b); _n += 1
    if _n:
        open(IDX, "w", encoding="utf-8", errors="surrogateescape").write(_s)
        print("- Access-first: footer Investors/Builders -> direct hub links (%d/2)" % _n)

_CANON = ('<script id="ns-canonical">(function(){var h=location.hostname;'
  'if(h.slice(-10)===".pages.dev"){location.replace("https://nutrisynccollective.com"+location.pathname+location.search+location.hash);}})();</script>')
_hubdir = os.path.join(PUB, "hub")
if os.path.isdir(_hubdir):
    _n = 0
    for _r, _d, _fs in os.walk(_hubdir):
        for _f in _fs:
            if not _f.endswith(".html"):
                continue
            _p = os.path.join(_r, _f)
            _s = open(_p, encoding="utf-8", errors="surrogateescape").read()
            if "ns-canonical" in _s or "</head>" not in _s:
                continue
            open(_p, "w", encoding="utf-8", errors="surrogateescape").write(_s.replace("</head>", _CANON + "</head>", 1))
            _n += 1
    if _n:
        print("- canonical-host redirect on %d hub pages (pages.dev -> custom domain)" % _n)

_gs = os.path.join(PUB, "hub", "full-hub-gated-site.html")
if os.path.exists(_gs):
    _s = open(_gs, encoding="utf-8", errors="surrogateescape").read()
    if "ns-access-unlock" not in _s and "applyAuth" in _s:
        _u = ('<script id="ns-access-unlock">(function(){var h=location.hostname;'
              'if(h==="nutrisynccollective.com"||h==="www.nutrisynccollective.com"){'
              'try{AUTH.inv=true;AUTH.adm=true;applyAuth();}catch(e){}}})();</script>')
        open(_gs, "w", encoding="utf-8", errors="surrogateescape").write(_s.replace("</body>", _u + "</body>", 1))
        print("- inner gate auto-unlocks behind Access (custom domain)")

# Support email: the real mailbox is contact@ (founders, 18 Jul). Design's pack
# still ships hello@ in the deactivation copy (flagged for source fix).
for _f in ('app.html', 'index.html'):
    _p = os.path.join(PUB, _f)
    if os.path.exists(_p):
        _s = open(_p, encoding='utf-8', errors='surrogateescape').read()
        if 'hello@nutrisynccollective.com' in _s:
            open(_p, 'w', encoding='utf-8', errors='surrogateescape').write(_s.replace('hello@nutrisynccollective.com', 'contact@nutrisynccollective.com'))
            print('- support email hello@ -> contact@ (' + _f + ')')

# Footer QR — scan-to-open the web app (founder request 18 Jul). Not in Design's
# pack yet (flagged in doc 12 to adopt at source): white tile after the store
# buttons, links to app.html, QR encodes https://nutrisynccollective.com/app.html.
if os.path.exists(IDX):
    _QR_SVG = '<svg style="width:100%;height:100%;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 33 33" class="segno"><path class="qrline" stroke="#1a1512" d="M2 2.5h7m1 0h2m1 0h1m2 0h1m2 0h2m3 0h7m-29 1h1m5 0h1m1 0h3m2 0h2m2 0h3m2 0h1m5 0h1m-29 1h1m1 0h3m1 0h1m1 0h4m1 0h1m5 0h2m1 0h1m1 0h3m1 0h1m-29 1h1m1 0h3m1 0h1m4 0h3m1 0h3m2 0h1m1 0h1m1 0h3m1 0h1m-29 1h1m1 0h3m1 0h1m1 0h4m5 0h1m1 0h1m2 0h1m1 0h3m1 0h1m-29 1h1m5 0h1m3 0h1m1 0h1m1 0h1m1 0h2m4 0h1m5 0h1m-29 1h7m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h1m1 0h7m-19 1h1m1 0h3m3 0h2m-20 1h1m2 0h10m1 0h2m1 0h1m3 0h1m2 0h1m1 0h3m-29 1h3m8 0h5m1 0h3m3 0h2m1 0h2m-27 1h1m4 0h1m1 0h5m2 0h1m1 0h2m1 0h4m2 0h1m-24 1h1m1 0h1m2 0h1m1 0h1m1 0h1m1 0h1m1 0h2m2 0h6m2 0h1m-28 1h1m2 0h4m2 0h1m4 0h1m4 0h1m1 0h1m5 0h1m-29 1h1m1 0h1m1 0h1m2 0h2m2 0h2m1 0h3m4 0h8m-28 1h3m1 0h4m1 0h2m1 0h3m1 0h1m1 0h4m1 0h1m1 0h1m1 0h1m-28 1h1m1 0h1m3 0h4m1 0h1m1 0h1m1 0h1m1 0h2m1 0h1m1 0h2m1 0h1m1 0h1m-29 1h1m2 0h2m1 0h2m1 0h1m1 0h2m1 0h2m3 0h2m4 0h1m-26 1h1m2 0h1m1 0h1m2 0h2m2 0h1m2 0h1m1 0h5m2 0h1m1 0h2m-28 1h4m1 0h2m2 0h1m1 0h5m1 0h1m1 0h1m1 0h1m2 0h2m2 0h1m-29 1h4m1 0h1m1 0h2m2 0h1m1 0h4m3 0h2m1 0h4m-27 1h3m1 0h1m1 0h1m1 0h3m2 0h1m2 0h12m-20 1h1m1 0h1m1 0h7m1 0h1m3 0h2m-26 1h7m1 0h2m3 0h1m1 0h2m2 0h2m1 0h1m1 0h2m-26 1h1m5 0h1m1 0h2m3 0h1m3 0h4m3 0h1m3 0h1m-29 1h1m1 0h3m1 0h1m1 0h2m1 0h3m2 0h1m2 0h7m1 0h1m-28 1h1m1 0h3m1 0h1m1 0h3m1 0h1m1 0h3m1 0h1m2 0h1m1 0h1m4 0h1m-29 1h1m1 0h3m1 0h1m2 0h1m1 0h1m1 0h1m1 0h1m1 0h3m1 0h1m1 0h2m1 0h3m-29 1h1m5 0h1m4 0h1m2 0h2m5 0h1m3 0h2m1 0h1m-29 1h7m1 0h4m1 0h2m4 0h4"/></svg>'
    _tile = ('<a id="ns-qr-app" href="app.html" title="Scan to open the NutriSync web app" '
             'style="display:inline-flex;align-items:center;justify-content:center;width:52px;height:52px;'
             'background:#FFF9F7;border-radius:10px;padding:4px;margin-left:2px;flex:none;">' + _QR_SVG + '</a>')
    _esc = _tile.replace('</', '<\\u002F').replace('"', '\\"')
    _anc = 'Google Play<\\u002Fspan><\\u002Fa>'
    _s = open(IDX, encoding="utf-8", errors="surrogateescape").read()
    if 'ns-qr-app' not in _s and 'ftScan' not in _s and _anc in _s:  # skip when the pack ships its own QR (v11.44+)
        open(IDX, "w", encoding="utf-8", errors="surrogateescape").write(_s.replace(_anc, _anc + '\\n          ' + _esc, 1))
        print("- footer QR tile -> app.html")

# W8-live — replace the static count with the live waitlist_count() RPC at runtime.
# The template's "140+" stays as the no-JS/SSR fallback; once the RPC responds, every
# element showing exactly "140+" is updated to the real number (never lower than 140).
if os.path.exists(IDX):
    # NOTE (po9 hotfix): the first version of this script used a MutationObserver
    # that re-swept the whole document on every DOM mutation. When the RPC returned
    # exactly 140 it rewrote "140+" with "140+", each write re-triggered the
    # observer -> infinite loop -> "Page Unresponsive" and the footer never
    # rendered. Now: only write when the value actually CHANGES (n > 140), and
    # instead of an observer, re-sweep on a bounded timer (10 x 1s) to catch the
    # SPA's late-rendered sections, then stop. Total work is finite by design.
    _lw = ('<script id="ns-live-waitlist">(function(){var U="__U__",K="__K__";'
      'fetch(U+"/rest/v1/rpc/waitlist_count",{method:"POST",headers:{"apikey":K,"Authorization":"Bearer "+K,"Content-Type":"application/json"},body:"{}"})'
      '.then(function(r){return r.json();}).then(function(n){'
      'if(typeof n!=="number"||n<=140)return;var txt=n+"+";'
      'function sweep(){var els=document.querySelectorAll("strong,b,span,div");'
      'for(var i=0;i<els.length;i++){var e=els[i];'
      'if(e.childElementCount===0&&e.textContent.trim()==="140+"&&e.textContent.trim()!==txt)e.textContent=txt;}}'
      'sweep();var k=0,iv=setInterval(function(){sweep();if(++k>=10)clearInterval(iv);},1000);'
      '}).catch(function(){});})();</script>').replace("__U__", URL).replace("__K__", KEY)
    _ih = open(IDX, encoding="utf-8", errors="surrogateescape").read()
    if "ns-live-waitlist" not in _ih:
        open(IDX, "w", encoding="utf-8", errors="surrogateescape").write(_ih.replace("</head>", _lw + "</head>", 1))
        print("- W8-live waitlist count wired (marketing)")
    _inv = os.path.join(PUB, "hub", "investors-business-case.html")
    if os.path.exists(_inv):
        _s2 = open(_inv, encoding="utf-8").read()
        if "ns-live-waitlist" not in _s2:
            open(_inv, "w", encoding="utf-8").write(_s2.replace("</body>", _lw + "</body>", 1))
            print("- W8-live waitlist count wired (investor)")

# W8 — waitlist stat 130 → 140+ (marketing stats bar + investor page)
_patch(IDX, [
    (r'130<\\u002Fstrong>&nbsp; \{\{ t\.trWaitlist \}\}', r'140+<\\u002Fstrong>&nbsp; {{ t.trWaitlist }}', True),
], "W8 waitlist 140+ (marketing)")
_patch(INV, [
    ('130</b> women waitlist', '140+</b> women waitlist', False),
    ('130</b> women on the waitlist', '140+</b> women on the waitlist', False),
], "W8 waitlist 140+ (investor)")

# W9 — diagnosis-delay stat card (EN + ES embedded dicts)
_patch(IDX, [
    (r"prYears: 'Years'", r"prYears: '~4 yrs'", True),
    (r"prC2t: 'Later diagnoses & delayed care'", r"prC2t: 'Later diagnoses than men'", True),
    (r"prC2b: 'Women[^']*delaying the care they need\.'",
     r"prC2b: 'Diagnosed ~4 years later than men on average \\u2014 4.5y later for metabolic conditions, 2.5y for cancer, 5\\u20136y for conditions like ADHD.'", True),
    (r"prYears: 'A[^']{1,4}os'", r"prYears: '~4 a\\u00f1os'", True),
    (r"prC2t: 'Diagn[^']{1,60}demorada'", r"prC2t: 'Diagn\\u00f3sticos m\\u00e1s tard\\u00edos que los hombres'", True),
    (r"prC2b: 'Los s[^']*?que necesitan\.'",
     r"prC2b: 'Diagnosticadas de media ~4 a\\u00f1os m\\u00e1s tarde que los hombres \\u2014 4,5 a\\u00f1os en enfermedades metab\\u00f3licas, 2,5 en c\\u00e1ncer y 5\\u20136 en condiciones como el TDAH.'", True),
], "W9 diagnosis-delay copy (EN+ES)")

# W10 — CAS section: add the "improvement over time" sentence (EN + ES)
_patch(IDX, [
    (r"(casP: 'A live 0[^']*?in real time)\.'",
     r"\1 \\u2014 and tracks how your alignment improves over time, so you can see the progress you\\u2019re actually making.'", True),
    (r"(casP: 'Un n[^']*?tiempo real)\.'",
     r"\1 \\u2014 y mide c\\u00f3mo mejora con el tiempo, para que veas el progreso real que est\\u00e1s logrando.'", True),
], "W10 CAS improvement sentence (EN+ES)")

# W9+W10 must also land in i18n/en.json + es.json (they override the embedded dicts at load)
for _lang, _vals in {
    "en": {"prYears": "~4 yrs", "prC2t": "Later diagnoses than men",
           "prC2b": "Diagnosed ~4 years later than men on average — 4.5y later for metabolic conditions, 2.5y for cancer, 5–6y for conditions like ADHD.",
           "_casAdd": " — and tracks how your alignment improves over time, so you can see the progress you’re actually making."},
    "es": {"prYears": "~4 años", "prC2t": "Diagnósticos más tardíos que los hombres",
           "prC2b": "Diagnosticadas de media ~4 años más tarde que los hombres — 4,5 años en enfermedades metabólicas, 2,5 en cáncer y 5–6 en condiciones como el TDAH.",
           "_casAdd": " — y mide cómo mejora con el tiempo, para que veas el progreso real que estás logrando."},
}.items():
    _p = os.path.join(PUB, "i18n", _lang + ".json")
    if os.path.exists(_p):
        _d = json.load(open(_p, encoding="utf-8"))
        _mk = _d.get("marketing") or _d.get("app", {}).get("marketing")
        # Only patch if the OLD copy is still present — from v11.43 Design ships the
        # corrected copy at source (native-written), which must win over ours.
        if _mk and _mk.get("prYears") in ("Years", "Años"):
            _add = _vals.pop("_casAdd")
            _mk.update(_vals)
            if _mk.get("casP") and "progres" not in _mk["casP"] and "progress" not in _mk["casP"]:
                # strip the trailing period so the em-dash continues the sentence cleanly
                _mk["casP"] = _mk["casP"].rstrip(". ") + _add
            json.dump(_d, open(_p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print("- W9/W10 i18n/%s.json marketing keys" % _lang)
# NOTE: the other 12 locale files keep their old translated stat until Design's
# translators update them — logged on doc 12 for the next translation round.

# W11 — center Lucía's headshot. Root cause: the marketing card points at a stale
# UUID asset (not shipped in current packs, badly cropped). Point it at Design's
# own well-framed square export instead; plain center crop, no transforms.
_patch(IDX, [
    (r'src=\\"8a56a246-0412-42c8-81e5-86aa777ef702\\"( alt=\\"Lucia Cebrian\\")',
     r'src=\\"assets/team/co3_sq.png\\"\1', True),
], "W11 Lucia headshot -> assets/team/co3_sq.png")

# W24f — remove the footer "Prototype" button (last public prototype entry point)
_patch(IDX, [
    (r'<button onclick=\\"\{\{ openPrototype \}\}\\"[^>]*>\{\{ t\.ftProto \}\}<\\u002Fbutton>', '', True),
], "W24f footer Prototype button removed")

# W6 — pricing (Pilar 17/7): standard tier only at €4.99/mo + employer tier.
# Remove the whole Free/€0 card from the pricing grid and reprice Premium.
# (W7: the investor page already shows €4.99 Basic + B2B in v11.42 — consistent, no change.)
_patch(IDX, [
    # the Free card: white card containing {{ t.przFree }} through its Start-free button
    (r'<div style=\\"background: #fff;[^"]*?flex-direction: column;\\">\\n\s*<div style=\\"font-weight: 700; font-size: 16px; color: #6B615C;\\">\{\{ t\.przFree \}\}[\s\S]*?\{\{ t\.przStart \}\}<\\u002Fbutton>\\n\s*<\\u002Fdiv>\\n\s*', '', True),
    ('€5.99', '€4.99', False),
], "W6 pricing: Free tier removed, €4.99/mo")

# W3 — Edit Period must start with NOTHING pre-selected (data integrity: the old
# defaults Flow='Medium' / Mood='Content' could be saved without the user ever
# touching them, corrupting CAS + Cycle Stability inputs). Mobile app already clean.
_patch(APH, [
    ("epFlow: 'Medium', epMood: 'Content'", "epFlow: null, epMood: null", False),
    ("mood_state: [st.epMood],", "mood_state: st.epMood ? [st.epMood] : null,", False),
], "W3 no pre-selected Flow/Mood (Edit Period)")

# W2 (integrity half) — Movement screen:
#  (1) "Mark as done" used to fabricate a checked row for EVERY session part; now it
#      writes ONE honest session row (the session title) — no invented per-part data.
#  (2) The "This week" list showed hardcoded demo workouts as already Done for live
#      accounts; for authed users those rows now show as planned instead.
#  The full redesign (per-activity selection + "Other" input) ships with the Round-2
#  Movement Log rebuild (wireframes delivered) — tracked on doc 15.
_patch(APH, [
    ("if (done) await this.sb.from('movement_checklist').insert(CC.mvParts.map((p) => ({ user_id: uid, date: today, phase: cyc ? cyc.disp : null, item_name: p.label, category_tag: 'session', intensity_level: intensity, checked: true })));",
     "if (done) await this.sb.from('movement_checklist').insert([{ user_id: uid, date: today, phase: cyc ? cyc.disp : null, item_name: (CC.mvTitle || 'Session'), category_tag: 'session', intensity_level: intensity, checked: true }]);", False),
    ("const mvWeekData = CC.week;",
     "const mvWeekData = authed ? CC.week.map((w) => (w.done && !w.today) ? Object.assign({}, w, { done: false, state: ((CC.week.filter((x) => !x.done && !x.today)[0] || {}).state || w.state) }) : w) : CC.week;", False),
], "W2 movement: honest session log + no fake Done history (live)")

# W21 — day-of-week strip: rectangular/pill cells → circular buttons (per wireframe).
# One shared template + one JS style string drive every use of the strip, so this
# fixes all screens at once. aspect-ratio keeps the circle round at any width.
_patch(APH, [
    ("style: 'flex:1;text-align:center;padding:9px 0;border-radius:12px;'",
     "style: 'flex:1 1 0;aspect-ratio:1/1;max-width:48px;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:50%;text-align:center;'", False),
    ('style=\\"display: flex; gap: 8px; background: #fff; border: 1px solid #EDE0D2; border-radius: 18px; padding: 12px; margin-top: 18px;\\"',
     'style=\\"display: flex; gap: 8px; justify-content: space-between; align-items: center; background: #fff; border: 1px solid #EDE0D2; border-radius: 18px; padding: 12px; margin-top: 18px;\\"', False),
], "W21 circular day buttons (shared strip)")

# F16 (confirmed by POs + verified: PCOS officially renamed PMOS, May 2026) —
# display "PMOS" everywhere while KEEPING the stored canonical key 'PCOS' so no
# existing user data breaks. dsp() falls back to the raw key for languages
# without a label, so the ternary covers EN + all untranslated locales at once.
_patch(APH, [
    ("label: dsp('condLabels', c), onToggle:",
     "label: (dsp('condLabels', c) === 'PCOS' ? 'PMOS' : dsp('condLabels', c)), onToggle:", False),
    ("condLabels: { PCOS: 'SOP',", "condLabels: { PCOS: 'PMOS',", False),
], "F16 PCOS -> PMOS labels (web app)")
_patch(IDX, [
    ("'Fibroids', 'Endometriosis', 'PCOS',", "'Fibroids', 'Endometriosis', 'PMOS',", False),
], "F16 PMOS in demo onboarding options")
_es = os.path.join(PUB, "i18n", "es.json")
if os.path.exists(_es):
    _d = json.load(open(_es, encoding="utf-8"))
    _cl = _d.get("app", {}).get("condLabels")
    if _cl and _cl.get("PCOS") != "PMOS":
        _cl["PCOS"] = "PMOS"
        json.dump(_d, open(_es, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("- F16 i18n/es.json condLabels PMOS")

# W1 — forgot-password link
_patch(APH, [
    (r'(cursor: pointer;)\\">\{\{ t\.forgot \}\}', r'\1\\" id=\\"ns-forgot\\">{{ t.forgot }}', True),
], "W1 forgot link tagged")
if os.path.exists(APH):
    s = open(APH, encoding="utf-8", errors="surrogateescape").read()
    if "ns-forgot-pw" not in s:
        FP = ('<script id="ns-forgot-pw" type="module">\n'
          "const U='%s',K='%s';\n" % (URL, KEY) +
          "import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';\n"
          "const sb=createClient(U,K,{auth:{persistSession:false}});\n"
          "document.addEventListener('click',async(e)=>{\n"
          "  const el=e.target.closest('#ns-forgot'); if(!el) return;\n"
          "  if((location.hash||'').indexOf('demo')>-1){alert('Demo mode \\u2014 password reset works in the live app.');return;}\n"
          "  let email='';\n"
          "  document.querySelectorAll('input').forEach(i=>{if(!email&&/@.+\\./.test(i.value||''))email=i.value.trim();});\n"
          "  if(!email) email=(window.prompt('Enter your account email:')||'').trim();\n"
          "  if(!email||!/@.+\\./.test(email)) return;\n"
          "  const {error}=await sb.auth.resetPasswordForEmail(email,{redirectTo:location.origin+location.pathname.replace(/[^\\/]*$/,'')+'reset.html'});\n"
          "  alert(error?('Could not send reset email: '+error.message):('Reset link sent to '+email+' \\u2014 check your inbox.'));\n"
          "},true);\n"
          "</script>")
        open(APH, "w", encoding="utf-8", errors="surrogateescape").write(s.replace("</head>", FP + "</head>", 1))
        print("- W1 forgot-password wiring (app.html)")

RESET_HTML = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
  '<meta name="viewport" content="width=device-width, initial-scale=1"><title>Reset password · NutriSync</title><style>'
  'body{margin:0;font-family:Poppins,-apple-system,sans-serif;color:#231F20;min-height:100vh;display:flex;align-items:center;justify-content:center;'
  'background:radial-gradient(circle at 28% 16%,#FDE2D6 0%,#FBEFE6 36%,#FFF8F1 62%,#F9D7BD 100%)}'
  '.card{background:#fff;border-radius:20px;box-shadow:0 24px 60px -24px rgba(0,0,0,.28);padding:30px 28px;max-width:380px;width:90%}'
  'h1{font-size:22px;margin:0 0 6px}p{color:#6B615C;font-size:13.5px;line-height:1.5;margin:0 0 16px}'
  'input{width:100%;box-sizing:border-box;padding:13px 15px;border:1px solid #EADFD5;border-radius:12px;font-size:14.5px;font-family:inherit;margin-bottom:10px}'
  'button{width:100%;border:none;cursor:pointer;background:linear-gradient(135deg,#EA5740,#F4876F);color:#fff;font-weight:700;font-size:15px;'
  'padding:14px;border-radius:100px;font-family:inherit}'
  '#msg{min-height:18px;font-size:12.5px;margin-top:10px}.ok{color:#0FA968}.err{color:#C73A20}'
  'a{color:#E8472A;font-weight:600;text-decoration:none}</style></head><body><div class="card">'
  '<h1>Set a new password</h1><p>You followed a reset link — choose a new password for your NutriSync account.</p>'
  '<input id="p1" type="password" placeholder="New password (6+ characters)"><input id="p2" type="password" placeholder="Repeat new password">'
  '<button id="go">Save new password</button><div id="msg"></div>'
  '<p style="margin-top:14px">Done? <a href="app.html">Open the app and log in →</a></p></div>'
  '<script type="module">\n'
  "const U='__U__',K='__K__';\n"
  "import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';\n"
  "const sb=createClient(U,K);const $=i=>document.getElementById(i);const m=$('msg');\n"
  "const {data:{session}}=await sb.auth.getSession();\n"
  "if(!session){m.textContent='This page only works from the link in your reset email (link may have expired).';m.className='err';}\n"
  "$('go').addEventListener('click',async()=>{m.textContent='';m.className='';\n"
  "  const a=$('p1').value,b=$('p2').value;\n"
  "  if(a.length<6){m.textContent='Password must be at least 6 characters.';m.className='err';return;}\n"
  "  if(a!==b){m.textContent='Passwords do not match.';m.className='err';return;}\n"
  "  const {error}=await sb.auth.updateUser({password:a});\n"
  "  if(error){m.textContent=error.message;m.className='err';}\n"
  "  else{m.textContent='Password updated \\u2713 \\u2014 you can log in now.';m.className='ok';}});\n"
  '</script></body></html>')
open(os.path.join(PUB, "reset.html"), "w", encoding="utf-8").write(RESET_HTML.replace("__U__", URL).replace("__K__", KEY))
print("- W1 reset.html page")
# ⚠ One-time Supabase step: Auth → URL Configuration → add
#   https://nutrisynccollective.com/reset.html  to Redirect URLs
#   (keep https://nutrisync-collective.pages.dev/reset.html as alias).
# ═══════════════ end PO Round 1 · Iteration 1 ═══════════════

# Cloudflare Pages cache policy: force browsers to revalidate HTML + language
# files so new deploys and newly-shipped language packs appear immediately
# (the ~660KB app.html otherwise caches hard and shows a stale UI/selector).
# Static assets (js/css/images/fonts) keep normal caching.
open(os.path.join(PUB, "_headers"), "w", encoding="utf-8").write(
    "/\n  Cache-Control: public, max-age=0, must-revalidate\n"
    "/*.html\n  Cache-Control: public, max-age=0, must-revalidate\n"
    "/hub/*\n  Cache-Control: public, max-age=0, must-revalidate\n"
    "/i18n/*\n  Cache-Control: public, max-age=0, must-revalidate\n")
print("- _headers cache policy (revalidate HTML + i18n)")

print("\nIntegration complete - review, then commit + push.")
