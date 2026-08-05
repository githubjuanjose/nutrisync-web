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
/* po60: el motor de Design reconstruye el DOM al arrancar y puede llevarse la
   hoja del head -> el banner salia CRUDO arriba-izquierda. El JS ahora garantiza
   su CSS (lo re-crea si falta), fija estilos inline criticos en el contenedor y
   reintenta una vez si el motor arranco el banner. */
function ensureCss(){if(document.getElementById("ns-consent-css-live"))return;var src=document.getElementById("ns-consent-css");var st=document.createElement("style");st.id="ns-consent-css-live";st.textContent=src?src.textContent:"";(document.head||document.documentElement).appendChild(st);}
function build(){if(have()){window.__nsConsent=have();return;}if(document.getElementById("ns-consent"))return;ensureCss();
/* po61: TODO inline (el motor no puede despeinarlo) + bilingue ES/EN + diseno NutriSync */
/* po77 (decision counsel + Juanjo): mientras NO exista analitica ni
   personalizacion, el banner es INFORMATIVO solo-esenciales — sin toggles
   inactivos. Cuando se activen tratamientos opcionales, se restaura el
   selector con consentimiento granular + actualizacion del inventario. */
var ES=(navigator.language||"en").toLowerCase().indexOf("es")===0;
var T=ES?{t:"Tu privacidad",p:"Usamos <b>unicamente cookies esenciales</b> para que NutriSync funcione (sesion, idioma y esta eleccion). Sin analitica, sin publicidad, sin rastreadores.",ok:"Entendido"}
:{t:"Your privacy",p:"We use <b>essential cookies only</b> to run NutriSync (session, language and this choice). No analytics, no advertising, no trackers.",ok:"Got it"};
var F="font-family:'Poppins','Inter',system-ui,sans-serif";
var d=document.createElement("div");d.id="ns-consent";
d.style.cssText="position:fixed;left:16px;right:16px;bottom:18px;z-index:99998;background:#FFFDFA;border:1px solid #EFE3D7;border-radius:20px;box-shadow:0 24px 60px -18px rgba(35,31,32,.35);padding:20px 22px;max-width:560px;margin:0 auto;"+F+";color:#241D1A;line-height:1.5";
d.innerHTML='<div style="display:flex;align-items:center;gap:9px;margin-bottom:6px"><span style="width:28px;height:28px;border-radius:9px;background:linear-gradient(135deg,#FF7600,#FD400C);display:inline-flex;align-items:center;justify-content:center;font-size:14px">🍪</span><b style="font-size:15px;font-weight:800">'+T.t+'</b></div>'
+'<p style="margin:0 0 10px;font-size:13px;color:#736862">'+T.p+'</p>'
+'<p style="margin:0 0 14px;font-size:12px"><a href="/legal/privacy.html" style="color:#C73A20">'+(ES?"Política de privacidad":"Privacy policy")+'</a> · <a href="/legal/cookies.html" style="color:#C73A20">Cookies</a></p>'
+'<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">'
+'<button id="ns-accept" style="'+F+';border:none;border-radius:999px;padding:11px 20px;font-weight:700;font-size:13px;cursor:pointer;background:linear-gradient(135deg,#FF7600,#FD400C);color:#fff">'+T.ok+'</button></div>';
document.body.appendChild(d);
document.getElementById("ns-accept").onclick=function(){save({essential:true,analytics:false,personalization:false});};}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",build);else build();
setTimeout(function(){if(!have()&&!document.getElementById("ns-consent"))build();},1600);})();</script>'''

for f in ("index.html", "app.html"):
    p = os.path.join(PUB, f)
    if not os.path.exists(p): continue
    s = open(p, encoding="utf-8", errors="ignore").read()
    # po60: refresh-on-change — quitar el bloque consent previo (css+js contiguos)
    # y reinyectar la version actual, para que las mejoras lleguen a ficheros vivos
    s2 = re.sub(r'<style id="ns-consent-css">.*?</script>', '', s, count=1, flags=re.S)
    add = ""
    if "ns-err-hide" not in s2: add += ERRHIDE
    add += CONSENT
    s2 = s2.replace("</head>", add + "</head>", 1)
    if s2 != s:
        open(p, "w", encoding="utf-8").write(s2); print("- consent/error-hide:", f)

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

# ns-docs-path (po58): el router del gated pedía docs/index.html (carpeta que un
# pack borró y que nunca existió en publish) → 404 → Pages devolvía la portada
# ("Project documentation lleva a la página principal"). Los docs viven en
# hub/documentation/ — se reapunta el iframe ahí. Idempotente.
_gsite = os.path.join(PUB, "hub", "full-hub-gated-site.html")
if os.path.exists(_gsite):
    _gs = open(_gsite, encoding="utf-8").read()
    if "docs/index.html" in _gs:
        _gs = _gs.replace("docs/index.html", "documentation/index.html")
        open(_gsite, "w", encoding="utf-8").write(_gs)
        print("- ns-docs-path: iframe de documentación → hub/documentation/index.html")

# ns-default-route v2 (po62→po63): el redirect de Cloudflare Access PIERDE el
# hash (#/builders no sobrevive) → entrada pública con ?r=<ruta> (la query SÍ
# sobrevive) que aquí se convierte en hash; sin nada → #/builders (detrás de
# Access solo hay founders). Además FRAME-BUST: si el gated acaba dentro de un
# iframe (clon del marketing → "páginas en bucle"), toma la ventana superior.
# Refresh-on-change.
if os.path.exists(_gsite):
    _gs0 = open(_gsite, encoding="utf-8").read()
    _gs = re.sub(r'<script id="ns-default-route">.*?</script>', "", _gs0, flags=re.S)
    _snip = ('<script id="ns-default-route">(function(){'
             # po65: la navbar es LA navegación — la fila interna de píldoras
             # de Builders (bt1/bt2 + enlaces htab) se oculta; su panel por
             # defecto (Admin & MIS) queda como contenido del Overview.
             # po67: fuera también la cabecera interna del gated ("Member — open
             # the app" y el logo goto('/') llevaban de vuelta al marketing)
             "document.addEventListener('DOMContentLoaded',function(){"
             "var b=document.getElementById('bt1');if(b&&b.parentElement)b.parentElement.style.display='none';"
             "var ep=document.querySelector('.header-eps');if(ep){var hd=ep.closest('header');(hd||ep).style.display='none';}"
             "});"
             "try{if(window.top!==window.self&&window.top.location.host===location.host){window.top.location=location.pathname+location.hash;return;}}catch(e){}"
             "var r=new URLSearchParams(location.search).get('r');"
             "if(r&&/^[a-z-]+$/.test(r)){location.replace(location.pathname+'#/'+r);return;}"
             "if(!location.hash||location.hash==='#'||location.hash==='#/'){location.replace(location.pathname+'#/builders');}"
             "})();</script>")
    _mm = re.search(r"<body[^>]*>", _gs)
    if _mm:
        _gs = _gs[:_mm.end()] + _snip + _gs[_mm.end():]
    if _gs != _gs0:
        open(_gsite, "w", encoding="utf-8").write(_gs)
        print("- ns-default-route v2: ?r=→hash + sin-hash→#/builders + frame-bust")

# ── Builders "Access" page: who can enter the gated areas + how it works. ──
# Informational SNAPSHOT (the live source of truth is the Cloudflare Access
# policy); protected by Access itself, so listing the emails here is safe.
_ACCESS_EMAILS = [
    ("juanjose.cebrian@gmail.com", "Juanjo — Engineering"),
    ("juanjosecebrian@icloud.com", "Juanjo — Apple ID (admin, 4-ago)"),
    ("lcebrian@nutrisynccollective.com", "Luc\u00eda — COO (domain)"),
    ("pgonzalez@nutrisynccollective.com", "Pilar — CEO (domain)"),
    ("mgarzon@nutrisynccollective.com", "Mar\u00eda Paula — CMO (domain)"),
    ("pilargonz05@gmail.com", "Pilar — personal"),
    ("cebrianlucia281@gmail.com", "Luc\u00eda — personal"),
    ("mapigarzon2204@gmail.com", "Mar\u00eda Paula — personal"),
]
_rows = "".join(
    '<tr><td><code>%s</code></td><td>%s</td></tr>' % (e, w) for e, w in _ACCESS_EMAILS
)
_ACCESS_HTML = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
  '<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Access \u00b7 NutriSync Builders</title>'
  '<style>body{font-family:Inter,system-ui,sans-serif;background:#FBF4EE;color:#241D1A;margin:0;line-height:1.6}'
  '.wrap{max-width:760px;margin:0 auto;padding:40px 22px 80px}'
  'h1{font-size:30px;font-weight:900;margin:0 0 6px}p{color:#6f655e}'
  'table{width:100%;border-collapse:collapse;margin:18px 0;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 10px 30px -18px rgba(0,0,0,.25)}'
  'th{background:#EA5740;color:#fff;text-align:left;padding:10px 14px;font-size:13px}'
  'td{padding:10px 14px;border-top:1px solid #F0E7DF;font-size:14px}'
  'code{background:#FBEDE6;color:#9a3a25;padding:2px 7px;border-radius:6px;font-size:.92em}'
  '.card{background:#fff;border-radius:14px;padding:16px 18px;margin:12px 0;box-shadow:0 10px 30px -18px rgba(0,0,0,.18);font-size:14px}'
  '.card b{display:block;margin-bottom:4px}'
  'a{color:#D8452F;font-weight:700}.top{font-size:13px}</style></head><body><div class="wrap">'
  '<p class="top"><a href="full-hub-gated-site.html">\u2039 Back to Builders</a></p>'
  '<h1>Who can access Builders &amp; Pitch</h1>'
  '<p>These addresses pass the Cloudflare Access gate (email + one-time PIN) on <code>/hub/*</code>. '
  'Sessions last 24h. This page is a snapshot \u2014 the live list is the Access policy.</p>'
  '<table><tr><th>Email</th><th>Who</th></tr>' + _rows + '</table>'
  '<div class="card"><b>How login works</b>Open any Builders/Pitch link \u2192 enter your email \u2192 '
  'a 6-digit code arrives by email \u2192 you are in for 24h. Only listed addresses receive codes.</div>'
  '<div class="card"><b>Add / remove someone</b>Cloudflare dashboard \u2192 Zero Trust \u2192 Access \u2192 '
  'Applications \u2192 <i>NutriSync Builders Hub</i> \u2192 policy <i>Founders</i> \u2192 Include \u2192 Emails. '
  'Changes apply immediately \u2014 no deploy needed. Keep this page in sync (ask Engineering).</div>'
  '<div class="card"><b>Related but separate</b>Reading app feedback / admin KPIs uses the <code>public.admins</code> '
  'allowlist in Supabase (SQL editor) \u2014 being on this page does not grant that automatically.</div>'
  '</div></body></html>')
_ap = os.path.join(PUB, "hub", "access.html")
open(_ap, "w", encoding="utf-8").write(_ACCESS_HTML)
print("- Builders Access page (hub/access.html)")
_hub = os.path.join(PUB, "hub", "full-hub-gated-site.html")
if os.path.exists(_hub):
    _s = open(_hub, encoding="utf-8").read()
    if "access.html" not in _s:
        _old = '<button class="htab" id="bt2" onclick="bldTab(2)">\U0001F4DA Project documentation</button>'
        _pill = '<a class="htab" href="access.html" target="_blank" style="text-decoration:none;display:inline-flex;align-items:center">\U0001F510 Access</a>'
        if _old in _s:
            open(_hub, "w", encoding="utf-8").write(_s.replace(_old, _old + "\n      " + _pill, 1))
            print("- Access pill on gated hub nav")

# ── Prototypes: moved OUT of the public marketing site, INTO the Builders area. ──
# The marketing bundle's "HEALTH FLOWS / See NutriSync in action" showcase is a
# single <section id="screens"> (plus nav/hero/footer links to "#screens"). It's
# prototype material, so we (1) strip that section and its "#screens" links from the
# PUBLIC site at runtime, and (2) publish a gated hub/prototypes.html that deep-links
# every screen of the working prototype (app.html#demo-<route>).
# ns-prototypes (r12): la página se genera con _integration/gen_prototypes.py
# (storytelling + Figma + recursos + 4 superficies con journey y pantallas) y
# aquí SOLO se copia — regla CLAUDE.md: snippet-files, nunca strings con escapes.
_proto = os.path.join(ASSETS, "prototypes.html")
if os.path.exists(_proto):
    shutil.copy(_proto, os.path.join(PUB, "hub", "prototypes.html"))
    print("- Prototypes hub page (hub/prototypes.html) desde _integration")

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

# Footer QR -> mobile PWA (founder decision 18 Jul): the QR now encodes
# https://m.nutrisynccollective.com (the installable PWA) instead of app.html.
# We overwrite Design's qr_app.png with a pre-generated PNG (embedded, no deps)
# and point the tile's click at the PWA. Asked of Design at source (doc 12).
import base64 as _b64
_QR_M_PNG = ('iVBORw0KGgoAAAANSUhEUgAAAlIAAAJSAQMAAAAyEbkwAAAABlBMVEUaFRL///9VhDnGAAACeUlEQVR42u3dQU7DMBAFUIseIEfK1XOkHiBSELS4M2OHglQWSM8raNK3yOJrYo/ddrxsbI3FYrFYLBaLxfoL69ryWB83fF5K9ywf/5UvXD6tt/a6wWKxWP/VumfmJWRtz9V033LsIXJL9spVFovFGnO1V54pM4+POA316vp181o+kassFov1NFdvf+zp9T9ckqssFov161ztI5SpcpXFYrF+lqtpfnV82e9Ju5hfZbFYrOe5mkfK1ZM/0pCrLBaLlXL1ZJTqdE8pOunZ8uxZLBYrzwNsj2aq8Mm9z7Wle8IlucpisViTenVPn6QU7YXrnha51tiCZR6AxWKxSr3a47Td6tWamUdsuNrTza3XtJ49i8Vi5Vw9SpzO2wB6CC/pklxlsVis83q171ptra9SzQ4K2POkgWfPYrFYLfQDlOWqvDi1xa/oB2CxWKyn9WptUu3HXS2TgwIuYSUrJK1cZbFYrFKvPhIynl61Dzf3XqyWa1rPnsVisVpartpam+yuuo/cBpCOcJWrLBaLNS9BW2n1nx9wXRuu9K+yWCzWkKsne//TtGpd2wr1qvlVFovFGurVvKlqm771x1Wq1DwgV1ksFmtWr46Fa5hxbT0843dL84Bnz2KxWO3sPKvZDqwYp+Np2HKVxWKxYr2ax/g7LGvcb3UZNhGoV1ksFms+DzD7jZVa017TzlbzACwWi3WWq/2NPp1ndZTjVk4nBOQqi8VifZer17JKtT72DizlJwWdZ8VisVi/q1fH+dVWDmtVr7JYLNYsV8dtVmkXwOmMq3UrFovFmuRqHut00T8WrrfX/925KywWizXN1deMjcVisVgsFovFerX1DhIYr/RtDcrOAAAAAElFTkSuQmCC')
# Write to a NEW filename (cache-busting: the old qr_app.png/UUID stays cached
# in browsers/CDN forever) and re-point the <img> at it.
_qr_asset = os.path.join(PUB, 'assets', 'qr-m.png')
open(_qr_asset, 'wb').write(_b64.b64decode(_QR_M_PNG))
print('- footer QR asset -> assets/qr-m.png (encodes the PWA URL)')
if os.path.exists(IDX):
    _s = open(IDX, encoding='utf-8', errors='surrogateescape').read()
    _s2 = re.sub(r'src=\\"[^"\\]*\\" alt=\\"QR code', r'src=\\"assets/qr-m.png\\" alt=\\"QR code', _s, count=1)
    if _s2 != _s:
        open(IDX, 'w', encoding='utf-8', errors='surrogateescape').write(_s2)
        print('- footer QR img re-pointed to assets/qr-m.png')
if os.path.exists(IDX):
    _s = open(IDX, encoding='utf-8', errors='surrogateescape').read()
    _a = 'sc-camel-on-click=\\"{{ enterApp }}\\" title=\\"{{ t.ftScan }}\\"'
    _b = 'href=\\"https://m.nutrisynccollective.com\\" title=\\"{{ t.ftScan }}\\"'
    if _a in _s:
        open(IDX, 'w', encoding='utf-8', errors='surrogateescape').write(_s.replace(_a, _b, 1))
        print('- footer QR tile click -> PWA')

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


# ---------------------------------------------------------------------------
# G3 phase 1 (Wave 1): Growth panel with REAL actuals (admin_growth RPC) +
# editable model assumptions (localStorage, per device) in the admin console.
# Aggregate-only, no PII; RPC gated on public.admins.
adm = os.path.join(PUB, "hub", "admin-mis-console.html")
if os.path.exists(adm):
    h = open(adm, encoding="utf-8").read()
    if "ns-growth" not in h:
        GHTML = (
          '<div class="panel" id="ns-growth">'
          '<h3>Growth — real actuals (live)</h3>'
          '<div style="display:flex;gap:26px;flex-wrap:wrap;margin-bottom:10px;">'
          '<div class="kpi" style="border:none;padding:4px 0;"><div class="lab">Registered users</div><div class="val" style="font-size:22px;" id="gUsers">—</div></div>'
          '<div class="kpi" style="border:none;padding:4px 0;"><div class="lab">Waitlist</div><div class="val" style="font-size:22px;" id="gWait">—</div></div>'
          '<div class="kpi" style="border:none;padding:4px 0;"><div class="lab">Waitlist → users</div><div class="val" style="font-size:22px;" id="gConv">—</div></div>'
          '<div class="kpi" style="border:none;padding:4px 0;"><div class="lab">Conversion</div><div class="val" style="font-size:22px;" id="gConvPct">—</div></div>'
          '</div>'
          '<div class="bars" id="growthBars" style="height:170px;"></div>'
          '<div class="legend"><span><span class="dot" style="background:var(--coral)"></span> New users / month</span>'
          '<span><span class="dot" style="background:var(--peach)"></span> Waitlist signups / month</span></div>'
          '<div style="font-size:12px;color:var(--muted);margin-top:8px;">Live from Supabase (admin_growth) · last 12 months · admin sign-in required.</div>'
          '</div>'
          '<div class="panel" id="ns-assump">'
          '<h3>Model assumptions — editable (saved on this device)</h3>'
          '<div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end;margin-bottom:12px;">'
          '<label style="font-size:12px;color:var(--muted);">Monthly user growth %<br/><input id="aG" type="number" step="1" min="0" style="width:110px;padding:9px 11px;border:1px solid var(--line);border-radius:10px;font-size:14px;margin-top:4px;"/></label>'
          '<label style="font-size:12px;color:var(--muted);">Premium share %<br/><input id="aP" type="number" step="0.5" min="0" max="100" style="width:110px;padding:9px 11px;border:1px solid var(--line);border-radius:10px;font-size:14px;margin-top:4px;"/></label>'
          '<label style="font-size:12px;color:var(--muted);">ARPU €/month<br/><input id="aA" type="number" step="0.01" min="0" style="width:110px;padding:9px 11px;border:1px solid var(--line);border-radius:10px;font-size:14px;margin-top:4px;"/></label>'
          '</div>'
          '<table><thead><tr><th>Month</th><th>Users</th><th>Premium</th><th>MRR</th></tr></thead><tbody id="projTable"></tbody></table>'
          '<div style="font-size:12px;color:var(--muted);margin-top:8px;">Projection = current real user total compounded by your assumptions, 12 months forward. Plan reference: Y1 755 users · €28,068 revenue (Conservative).</div>'
          '</div>')
        i = h.find('<h3>Business case tracking')
        j = h.rfind('<div class="panel">', 0, i)
        if i > -1 and j > -1:
            h = h[:j] + GHTML + h[j:]
        GJS = ('<script type="module" id="ns-growth-js">\n'
          + "const U='%s',K='%s';\n" % (URL, KEY) +
          "import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';const sb=createClient(U,K);const $=i=>document.getElementById(i);\n"
          "const eur=n=>'€'+Math.round(n).toLocaleString('en-US');const num=n=>Number(n).toLocaleString('en-US');\n"
          "function bars(el,rows){if(!el||!rows||!rows.length)return;const m=Math.max(1,...rows.map(r=>Math.max(r.signups,r.waitlist)));"
          "el.innerHTML=rows.map(r=>`<div class='barcol'><div style='flex:1;display:flex;align-items:flex-end;gap:3px;width:70%;justify-content:center;'>"
          "<div class='bar' title='${r.signups} users' style='width:45%;height:${Math.max(2,r.signups/m*100)}%;background:var(--coral);'></div>"
          "<div class='bar' title='${r.waitlist} waitlist' style='width:45%;height:${Math.max(2,r.waitlist/m*100)}%;background:var(--peach);'></div>"
          "</div><div class='barlabel'>${r.m.slice(2)}</div></div>`).join('');}\n"
          "const DEF={g:20,p:10,a:5.99};let TOT=0;\n"
          "function readA(){try{return{...DEF,...JSON.parse(localStorage.getItem('ns.biz.assump')||'{}')}}catch(e){return DEF}}\n"
          "function proj(){const a=readA();if($('aG')&&document.activeElement!==$('aG'))$('aG').value=a.g;"
          "if($('aP')&&document.activeElement!==$('aP'))$('aP').value=a.p;"
          "if($('aA')&&document.activeElement!==$('aA'))$('aA').value=a.a;"
          "let u=Math.max(TOT,1),rows='';const now=new Date();"
          "for(let i=1;i<=12;i++){u=u*(1+a.g/100);const d=new Date(now.getFullYear(),now.getMonth()+i,1);const prem=u*a.p/100;"
          "rows+=`<tr><td>${d.toLocaleDateString('en-GB',{month:'short',year:'2-digit'})}</td><td>${num(Math.round(u))}</td><td>${num(Math.round(prem))}</td><td>${eur(prem*a.a)}</td></tr>`;}"
          "if($('projTable'))$('projTable').innerHTML=rows;}\n"
          "function saveA(){const a={g:+$('aG').value||0,p:+$('aP').value||0,a:+$('aA').value||0};localStorage.setItem('ns.biz.assump',JSON.stringify(a));proj();}\n"
          "['aG','aP','aA'].forEach(i=>$(i)&&$(i).addEventListener('input',saveA));\n"
          "async function G(){const{data:{session}}=await sb.auth.getSession();if(!session){proj();return;}"
          "const{data,error}=await sb.rpc('admin_growth');if(error||!data){proj();return;}"
          "const t=data.totals;$('gUsers').textContent=num(t.users);$('gWait').textContent=num(t.waitlist);$('gConv').textContent=num(t.converted);"
          "$('gConvPct').textContent=t.waitlist?Math.round(t.converted/t.waitlist*100)+'%':'—';"
          "bars($('growthBars'),data.months);TOT=t.users;proj();}\n"
          "sb.auth.onAuthStateChange(()=>G());G();\n"
          "</script>\n")
        h = h.replace("</body>", GJS + "</body>", 1)
        open(adm, "w", encoding="utf-8").write(h)
        print("- G3 growth panel + assumptions (admin console)")


# ---------------------------------------------------------------------------
# ns-ob-i18n: Onboarding i18n (ob.*) into the web i18n packs, so the hub Translations tool
# can review them next to marketing/app/catalog. Source: _integration/ob_keys.json
# (14 languages, generated from the mobile catalogs). Deep-merged, idempotent.
obk = os.path.join(ASSETS, "ob_keys.json")
if os.path.exists(obk):
    OBALL = json.load(open(obk, encoding="utf-8"))
    def _deepmerge(dst, src):
        for k, v in src.items():
            if isinstance(v, dict) and isinstance(dst.get(k), dict):
                _deepmerge(dst[k], v)
            else:
                dst[k] = v
    n = 0
    for lang, ob in OBALL.items():
        p = os.path.join(PUB, "i18n", lang + ".json")
        if not os.path.exists(p):
            continue
        cat = json.load(open(p, encoding="utf-8"))
        _deepmerge(cat.setdefault("ob", {}), ob)
        json.dump(cat, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        n += 1
    print("- onboarding ob.* merged into %d i18n packs" % n)


# ---------------------------------------------------------------------------
# ns-pricing-polish (interim, Design asked to fix at source — doc 12 §19):
# pricing cards: pin CTAs to the card bottom (a later margin-top:26px was
# overriding margin-top:auto), give the features list a fixed bottom gap,
# lift the enterprise card (warm bg + shadow), add check glyphs to features.
idx = os.path.join(PUB, "index.html")
if os.path.exists(idx):
    h = open(idx, encoding="utf-8").read()
    if "ns-pricing-polish" not in h and "{{ t.przEmp }}" in h:
        h = h.replace('cursor: pointer; margin-top: 26px;', 'cursor: pointer;')
        h = h.replace('gap: 10px; font-size: 14.5px; color: #DCD1D7;',
                      'gap: 10px; font-size: 14.5px; color: #DCD1D7; margin-bottom: 26px;')
        h = h.replace('gap: 10px; font-size: 14.5px; color: #4A4340;',
                      'gap: 10px; font-size: 14.5px; color: #4A4340; margin-bottom: 26px;')
        h = h.replace('background: #fff; border: 1px solid #EADFD0; border-radius: 24px; padding: 30px; display: flex; flex-direction: column;',
                      'background: #FFFDF8; border: 1px solid #EADFD0; border-radius: 24px; padding: 30px; display: flex; flex-direction: column; box-shadow: 0 30px 60px -30px rgba(60,30,20,.22);')
        CKP = '<span><span style=\\"color: #F3A38C; font-weight: 700; margin-right: 8px;\\">✓<\\u002Fspan>'
        CKE = '<span><span style=\\"color: #E8472A; font-weight: 700; margin-right: 8px;\\">✓<\\u002Fspan>'
        for k in ('przP1', 'przP2', 'przP3', 'przP4'):
            h = h.replace('<span>{{ t.%s }}' % k, CKP + '{{ t.%s }}' % k)
        for k in ('przE1', 'przE2', 'przE3'):
            h = h.replace('<span>{{ t.%s }}' % k, CKE + '{{ t.%s }}' % k)
        h = h.replace('</body>', '<!-- ns-pricing-polish --></body>', 1)
        open(idx, "w", encoding="utf-8").write(h)
        print("- pricing cards polish (CTA alignment + enterprise card depth)")


# ---------------------------------------------------------------------------
# ns-mob2-i18n: R3–R5 mobile-only strings (mob.*/ui.* additions) into the web
# i18n packs so the hub Translations tool can review them (section "mob"/"ui").
# Source: _integration/mob2_keys.json (EN source + ES hand pass + auto-reused
# matches per language). Deep-merged, idempotent.
m2 = os.path.join(ASSETS, "mob2_keys.json")
if os.path.exists(m2):
    M2ALL = json.load(open(m2, encoding="utf-8"))
    def _dm2(dst, src):
        for k, v in src.items():
            if isinstance(v, dict) and isinstance(dst.get(k), dict):
                _dm2(dst[k], v)
            else:
                dst[k] = v
    n = 0
    for lang, tree in M2ALL.items():
        p = os.path.join(PUB, "i18n", lang + ".json")
        if not os.path.exists(p):
            continue
        cat = json.load(open(p, encoding="utf-8"))
        _dm2(cat, tree)
        json.dump(cat, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        n += 1
    print("- mobile-string (mob/ui) keys merged into %d i18n packs" % n)


# ---------------------------------------------------------------------------
# ns-mob3-i18n: r8b sweep — Settings/Notifications/moods/meals UI keys (mob.*)
# plus the CONTENT CATALOG names (foods + movements + categories) into the web
# i18n packs so the hub Translations tool lists them. Empty values mark keys
# PENDING translation and never overwrite existing entries.
m3 = os.path.join(ASSETS, "mob3_keys.json")
if os.path.exists(m3):
    M3ALL = json.load(open(m3, encoding="utf-8"))
    def _dm3(dst, src):
        for k, v in src.items():
            if isinstance(v, dict):
                node = dst.get(k)
                if not isinstance(node, dict):
                    node = {}
                    dst[k] = node
                _dm3(node, v)
            elif v == "":
                dst.setdefault(k, "")
            else:
                dst[k] = v
    n3 = 0
    for lang, tree in M3ALL.items():
        p3 = os.path.join(PUB, "i18n", lang + ".json")
        if not os.path.exists(p3):
            continue
        c3 = json.load(open(p3, encoding="utf-8"))
        _dm3(c3, tree)
        json.dump(c3, open(p3, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        n3 += 1
    print("- r8b mob3 keys (settings/notifs/moods/meals + content catalog) merged into %d packs" % n3)



# ---------------------------------------------------------------------------
# ns-feedback-panel: the in-app "Send Feedback" writes to public.feedback and
# founders read via admin_feedback() — but the hub never had a panel. Adds a
# Feedback card to the admin console (same session + RPC pattern as admin_kpis).
fbp = os.path.join(PUB, "hub", "admin-mis-console.html")
if os.path.exists(fbp):
    hf = open(fbp, encoding="utf-8").read()
    if "ns-feedback-panel" not in hf:
        panel = (
            '<!-- ns-feedback-panel -->'
            '<div class="section" style="padding:26px 0 60px;"><div style="max-width:1080px;margin:0 auto;padding:0 22px;">'
            '<h2 class="title" style="font-size:22px;margin:0 0 4px;">App Feedback</h2>'
            '<div style="color:var(--muted);font-size:13px;margin-bottom:14px;">Mensajes de Settings &rarr; Send Feedback (tabla feedback &middot; solo admins)</div>'
            '<div id="fbList" style="display:flex;flex-direction:column;gap:10px;"><div style="color:var(--muted);font-size:13px;">Cargando&hellip;</div></div>'
            '</div></div>'
            '<script type="module">'
            "import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';"
            "const U='https://nebkqncvapelrarruyqb.supabase.co',K='sb_publishable_GYj7DKlcWZ2cxdwv-GkyHQ_WBbQWHau';"
            "const sb=createClient(U,K);const box=document.getElementById('fbList');"
            "const esc=t=>t.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));"
            "(async()=>{const{data:{session}}=await sb.auth.getSession();"
            "if(!session){box.innerHTML='<div style=\'color:var(--muted);font-size:13px;\'>Inicia sesi&oacute;n de admin arriba para ver el feedback.</div>';return;}"
            "const{data,error}=await sb.rpc('admin_feedback',{limit_n:200});"
            "if(error){box.innerHTML='<div style=\'color:var(--muted);font-size:13px;\'>Sin acceso ('+esc(error.message)+')</div>';return;}"
            "if(!data||!data.length){box.innerHTML='<div style=\'color:var(--muted);font-size:13px;\'>Sin mensajes todav&iacute;a.</div>';return;}"
            "box.innerHTML=data.map(r=>'<div style=\'background:#fff;border:1px solid #EFE3D7;border-radius:14px;padding:14px 16px;\'>'"
            "+'<div style=\'font-size:12px;color:var(--muted);margin-bottom:6px;\'>'+new Date(r.created_at).toLocaleString()+' &middot; v'+esc(r.app_version||'?')+' &middot; '+esc(r.platform||'?')+'</div>'"
            "+'<div style=\'font-size:14px;line-height:1.5;white-space:pre-wrap;\'>'+esc(r.message)+'</div></div>').join('');})();"
            '</script>'
        )
        hf = hf.replace('</body>', panel + '</body>', 1)
        open(fbp, "w", encoding="utf-8").write(hf)
        print("- feedback panel added to the admin console (admin_feedback RPC)")

# ---------------------------------------------------------------------------
# ns-pilot-funnel: pilot funnel card in the admin console (snippet file, r11).
# Lesson v11.50: EVERYTHING ours must be a registered idempotent block — the
# pack overwrote the console and this card only survived because we re-inject.
pf = os.path.join(ASSETS, "pilot-funnel.html")
cns = os.path.join(PUB, "hub", "admin-mis-console.html")
if os.path.exists(pf) and os.path.exists(cns):
    ch = open(cns, encoding="utf-8").read()
    if "ns-pilot-funnel" not in ch and "<!-- ns-feedback-panel -->" in ch:
        ch = ch.replace("<!-- ns-feedback-panel -->",
                        open(pf, encoding="utf-8").read() + "<!-- ns-feedback-panel -->", 1)
        open(cns, "w", encoding="utf-8").write(ch)
        print("- pilot funnel card added to the admin console (admin_pilot_funnel RPC)")

# ns-finance: Finanzas — hub tab (libro diario + P&L + cierres) + MIS card.
fin = os.path.join(ASSETS, "finance.html")
if os.path.exists(fin):
    shutil.copy(fin, os.path.join(PUB, "hub", "finance.html"))
    print("- finance tool copied to hub/finance.html")
    _figh = os.path.join(PUB, "hub", "full-hub-gated-site.html")
    _fiht = open(os.path.join(ASSETS, "finance-htab.snippet"), encoding="utf-8").read()
    if os.path.exists(_figh):
        _fih = open(_figh, encoding="utf-8").read()
        if 'finance.html' not in _fih:
            open(_figh, "w", encoding="utf-8").write(
                _fih.replace('<a class="htab" href="waitlist.html"', _fiht + '<a class="htab" href="waitlist.html"', 1))
            print("- finance htab added to hub nav")
fmis = os.path.join(ASSETS, "finance-mis.html")
if os.path.exists(fmis) and os.path.exists(cns):
    ch = open(cns, encoding="utf-8").read()
    if "ns-finance-mis" not in ch:
        ch = ch.replace("</body>", open(fmis, encoding="utf-8").read() + "</body>", 1)
        open(cns, "w", encoding="utf-8").write(ch)
        print("- finance summary card wired into the admin console")

# ns-feedback-page: App Feedback as its OWN hub tab (r11d — moved out of the
# console). Copies the page + adds the 💬 htab; also STRIPS the legacy embedded
# panel from the console if a pack or old integrate left it there.
fbpage = os.path.join(ASSETS, "feedback.html")
if os.path.exists(fbpage):
    shutil.copy(fbpage, os.path.join(PUB, "hub", "feedback.html"))
    print("- feedback tool copied to hub/feedback.html")
    _fgh = os.path.join(PUB, "hub", "full-hub-gated-site.html")
    _fht = open(os.path.join(ASSETS, "feedback-htab.snippet"), encoding="utf-8").read()
    if os.path.exists(_fgh):
        _fh = open(_fgh, encoding="utf-8").read()
        if 'feedback.html' not in _fh:
            open(_fgh, "w", encoding="utf-8").write(
                _fh.replace('<a class="htab" href="waitlist.html"', _fht + '<a class="htab" href="waitlist.html"', 1))
            print("- feedback htab added to hub nav")
    if os.path.exists(cns):
        ch = open(cns, encoding="utf-8").read()
        if 'ns-feedback-panel' in ch:
            import re as _re2
            ch2 = _re2.sub(r'<!-- ns-feedback-panel -->.*?</script>', '<!-- ns-feedback-moved: hub/feedback.html -->', ch, count=1, flags=_re2.S)
            open(cns, "w", encoding="utf-8").write(ch2)
            print("- legacy feedback panel stripped from the console (now its own tab)")

# ns-kpi-live: honest KPI row (actual vs plan) — console AND the Builders
# gated-site MIS (po56: same snippet, label-based selectors; refresh-on-change
# so snippet updates propagate instead of being blocked by the old marker).
kl = os.path.join(ASSETS, "kpi-live.html")
if os.path.exists(kl):
    _snippet = open(kl, encoding="utf-8").read()
    for _page in [cns, os.path.join(PUB, "hub", "full-hub-gated-site.html")]:
        if not os.path.exists(_page):
            continue
        ch = open(_page, encoding="utf-8").read()
        # strip any previous ns-kpi-live block (idempotent refresh)
        ch2 = re.sub(r"<!-- ns-kpi-live -->.*?</script>", "", ch, flags=re.S)
        if "</body>" in ch2:
            ch2 = ch2.replace("</body>", _snippet + "</body>", 1)
        else:
            ch2 = ch2 + _snippet
        if ch2 != ch:
            open(_page, "w", encoding="utf-8").write(ch2)
            print(f"- honest KPI row (actual vs plan) wired into {os.path.basename(_page)}")

# ns-mis (r12): tarjetas Access / Subscriptions / Business case con datos REALES,
# el MISMO snippet en la consola y en el Overview del gated → valores idénticos
# (petición Juanjo: "Overview and MIS values should match"). Refresh-on-change.
_misf = os.path.join(ASSETS, "mis-cards.html")
if os.path.exists(_misf):
    _mis = open(_misf, encoding="utf-8").read()
    for _page in [cns, os.path.join(PUB, "hub", "full-hub-gated-site.html")]:
        if not os.path.exists(_page):
            continue
        _s0 = open(_page, encoding="utf-8").read()
        _s = re.sub(r"<!-- ns-mis -->.*?</script>", "", _s0, flags=re.S)
        if "</body>" in _s:
            _s = _s.replace("</body>", _mis + "</body>", 1)
        else:
            _s = _s + _mis
        if _s != _s0:
            open(_page, "w", encoding="utf-8").write(_s)
            print(f"- ns-mis: tarjetas reales (access/subs/business case) en {os.path.basename(_page)}")

# ns-legal (po71): los 5 documentos legales BILINGÜES (borrador pendiente de
# validación) + índice → publish/legal/. Nuestros; los packs nunca los traen.
_lg = os.path.join(ASSETS, "legal")
if os.path.isdir(_lg):
    _lgd = os.path.join(PUB, "legal"); os.makedirs(_lgd, exist_ok=True); _n = 0
    for _f in os.listdir(_lg):
        if _f.endswith(".html"):
            shutil.copy(os.path.join(_lg, _f), os.path.join(_lgd, _f)); _n += 1
    print(f"- ns-legal: {_n} documentos legales publicados en /legal/")

# ns-legal-footer (po72): la columna LEGAL del footer de Design trae href="#"
# (saltaba arriba). Se cablea por TEXTO tras el paint del motor — solo se tocan
# anchors con href vacío/#, jamás los del payload que ya funcionan. Refresh.
# po78 · LECCIÓN: el motor RE-RENDERIZA el footer (pisando el cableado) y su
# router INTERCEPTA los clics de <a> (href correcto → igualmente "sube arriba").
# Respuesta: (1) recableo continuo vía MutationObserver 30s, (2) listener de
# clic en FASE CAPTURA con stopPropagation → navegación real pase lo que pase.
_LF = ('<script id="ns-legal-footer">(function(){'
       "var MAP=[[/derechos de datos|data rights/i,'/legal/privacy.html'],"
       "[/^privacidad|^privacy/i,'/legal/privacy.html'],"
       "[/^t\\u00e9rminos|^terminos|^terms/i,'/legal/terms.html'],"
       "[/^cookies$/i,'/legal/cookies.html'],"
       "[/^aviso legal$|^legal notice$/i,'/legal/legal-notice.html']];"
       "function dest(t){for(var i=0;i<MAP.length;i++){if(MAP[i][0].test(t))return MAP[i][1];}return null;}"
       "function wire(){var n=0;document.querySelectorAll('a').forEach(function(a){"
       "var t=(a.textContent||'').trim();if(!t)return;var d=dest(t);if(!d)return;"
       "var h=a.getAttribute('href');"
       "if(h&&h!=='#'&&!a.__nsL)return;"                      # enlace ajeno que ya funciona: ni tocarlo
       "a.setAttribute('href',d);"
       "if(!a.__nsL){a.__nsL=1;a.addEventListener('click',function(e){"
       "e.preventDefault();e.stopPropagation();window.location.href=d;},true);}"
       "n++;});return n;}"
       "function boot(){wire();"
       "var mT=null,mo=new MutationObserver(function(){clearTimeout(mT);mT=setTimeout(wire,200);});"
       "mo.observe(document.documentElement,{childList:true,subtree:true});"
       "setTimeout(function(){mo.disconnect();},30000);}"
       "if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();"
       "})();</script>")
for _pg in ("index.html",):
    _pp = os.path.join(PUB, _pg)
    if os.path.exists(_pp):
        _ps0 = open(_pp, encoding="utf-8").read()
        _ps = re.sub(r'<script id="ns-legal-footer">.*?</script>', "", _ps0, flags=re.S)
        _ps = _ps.replace("</body>", _LF + "</body>", 1)
        if _ps != _ps0:
            open(_pp, "w", encoding="utf-8").write(_ps)
            print("- ns-legal-footer: columna LEGAL del footer cableada a /legal/")


# ns-tester: public store-email capture page — ours, packs never carry it.
ts = os.path.join(ASSETS, "tester.html")
if os.path.exists(ts):
    shutil.copy(ts, os.path.join(PUB, "tester.html"))
    print("- tester capture page copied to publish/tester.html")

# ---------------------------------------------------------------------------
# ns-pilot: Pilot tool (cohorts + founder-validated invite batches + cohort
# feedback). UI snippets are plain files — no escape sequences anywhere.
# r12-b6: el piloto se parte en tres superficies — operación (pilot.html),
# PLAN semanal (pilot-planning.html) y OBSERVABILIDAD (pilot-observability.html).
# Las gráficas salen del panel Business case del MIS y viven en su pestaña.
for _f in ("pilot-charts.js", "pilot-planning.html", "pilot-observability.html", "daily-ops.html", "decisions.html", "notifications.html", "incidents.html"):
    _src = os.path.join(ASSETS, _f)
    if os.path.exists(_src):
        shutil.copy(_src, os.path.join(PUB, "hub", _f))
        print(f"- piloto: hub/{_f}")

# r12-b11: los assets NUESTROS van versionados por contenido. Un HTML nuevo con
# un .js viejo en cache mata la pagina a mitad sin dar un solo error visible.
_charts = os.path.join(PUB, "hub", "pilot-charts.js")
if os.path.exists(_charts):
    import hashlib as _h, re as _re
    _v = _h.sha1(open(_charts, "rb").read()).hexdigest()[:8]
    for _page in ("pilot-planning.html", "pilot-observability.html"):
        _pp = os.path.join(PUB, "hub", _page)
        if not os.path.exists(_pp):
            continue
        _s0 = open(_pp, encoding="utf-8").read()
        _s1 = _re.sub(r'(<script src="/hub/pilot-charts\.js)(\?v=[a-f0-9]+)?(">)',
                      r'\1?v=' + _v + r'\3', _s0)
        if _s1 != _s0:
            open(_pp, "w", encoding="utf-8").write(_s1)
    print(f"- piloto: pilot-charts.js versionado ?v={_v}")

pl = os.path.join(ASSETS, "pilot.html")
if os.path.exists(pl):
    shutil.copy(pl, os.path.join(PUB, "hub", "pilot.html"))
    print("- pilot tool copied to hub/pilot.html")
    _pidx = os.path.join(PUB, "index.html")
    _pcard = open(os.path.join(ASSETS, "pilot-card.snippet"), encoding="utf-8").read()
    if os.path.exists(_pidx):
        _ih = open(_pidx, encoding="utf-8").read()
        if 'hub/pilot.html' not in _ih and '{h:"hub/waitlist.html"' in _ih:
            open(_pidx, "w", encoding="utf-8").write(
                _ih.replace('{h:"hub/waitlist.html"', _pcard + '{h:"hub/waitlist.html"', 1))
            print("- pilot card added to founder tools")
    _pgh = os.path.join(PUB, "hub", "full-hub-gated-site.html")
    _phtab = open(os.path.join(ASSETS, "pilot-htab.snippet"), encoding="utf-8").read()
    if os.path.exists(_pgh):
        _hh = open(_pgh, encoding="utf-8").read()
        if 'pilot.html' not in _hh:
            open(_pgh, "w", encoding="utf-8").write(
                _hh.replace('<a class="htab" href="waitlist.html"', _phtab + '<a class="htab" href="waitlist.html"', 1))
            print("- pilot htab added to hub nav")

# ---------------------------------------------------------------------------
# ns-mfa: MFA enrollment page for admins (Epic K / decision 2A).
mf = os.path.join(ASSETS, "mfa.html")
if os.path.exists(mf):
    shutil.copy(mf, os.path.join(PUB, "hub", "mfa.html"))
    print("- mfa tool copied to hub/mfa.html")
    _mgh = os.path.join(PUB, "hub", "full-hub-gated-site.html")
    _mht = open(os.path.join(ASSETS, "mfa-htab.snippet"), encoding="utf-8").read()
    if os.path.exists(_mgh):
        _mh = open(_mgh, encoding="utf-8").read()
        if 'mfa.html' not in _mh:
            open(_mgh, "w", encoding="utf-8").write(
                _mh.replace('<a class="htab" href="pilot.html"', _mht + '<a class="htab" href="pilot.html"', 1))
            print("- mfa htab added to hub nav")

# ---------------------------------------------------------------------------
# ns-footer-mailto: wire footer placeholders by template key (labels are i18n vars).
fidx = os.path.join(PUB, "index.html")
if os.path.exists(fidx):
    fh = open(fidx, encoding="utf-8").read()
    if 'mailto:contact@nutrisynccollective.com' not in fh:
        import re as _re
        for _k, _t in (("ftContact", "mailto:contact@nutrisynccollective.com"),
                       ("ftCareers", "mailto:contact@nutrisynccollective.com?subject=Empleo%20NutriSync")):
            fh = _re.sub(r'href=\"#\"([^>]*>\{\{ t\.' + _k + r' \}\})', 'href=\"' + _t + '\"\1', fh)
        fh = fh.replace('href=\"#science\"', 'href=\"#platform\"')
        open(fidx, "w", encoding="utf-8").write(fh)
        print("- footer links wired (contact/careers mailto, science anchor)")

# ---------------------------------------------------------------------------
# ns-auth-redirects: signup emails always land on production (belt & braces
# with the dashboard Site URL).
ap = os.path.join(PUB, "app.html")
if os.path.exists(ap):
    ah = open(ap, encoding="utf-8").read()
    _o = "this.sb.auth.signUp({ email: st.email.trim(), password: st.password, options: { data:"
    _n = "this.sb.auth.signUp({ email: st.email.trim(), password: st.password, options: { emailRedirectTo: location.origin + '/app.html', data:"
    if _o in ah and "emailRedirectTo: location.origin" not in ah:
        open(ap, "w", encoding="utf-8").write(ah.replace(_o, _n))
        print("- auth signup redirect wired to production")



# ---------------------------------------------------------------------------
# ns-cta-script: standalone CTA interceptor (NEVER touches the engine payload).
# Captures clicks on the app CTAs, scrolls to the waitlist email + shows toast.
cix = os.path.join(PUB, "index.html")
if os.path.exists(cix):
    chh = open(cix, encoding="utf-8").read()
    if 'id="ns-cta"' not in chh:
        snip = open(os.path.join(ASSETS, "cta-script.html"), encoding="utf-8").read()
        open(cix, "w", encoding="utf-8").write(chh.replace('</body>', snip + '</body>', 1))
        print("- standalone CTA script injected")

# ---------------------------------------------------------------------------
# ns-consent-wait v2: consent shows only after first paint (semantics fixed).
cwp = os.path.join(PUB, "index.html")
if os.path.exists(cwp):
    ch = open(cwp, encoding="utf-8").read()
    _clean = "var nsShow=function(){var tries=0;var iv=setInterval(function(){var r=document.getElementById('dc-root');if((r&&r.children.length>0)||tries++>50){clearInterval(iv);build();}},200);};if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',nsShow);}else{nsShow();}"
    _orig = 'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",build);else build();'
    _broken = 'if(document.readyState==="loading")var nsShow=function(){var tries=0;var iv=setInterval(function(){var r=document.getElementById(\'dc-root\');if((r&&r.children.length>0)||tries++>50){clearInterval(iv);build();}},200);};document.addEventListener(\'DOMContentLoaded\',nsShow);if(document.readyState!==\'loading\'){nsShow();}'
    if _clean not in ch:
        ch2 = ch.replace(_orig, _clean).replace(_broken, _clean)
        if ch2 != ch:
            open(cwp, "w", encoding="utf-8").write(ch2)
            print("- consent wait-for-paint (v2)")

print("\nIntegration complete - review, then commit + push.")

# ns-hub-nav: deep-links correctos al hub (r11e). El router del gated-site usa
# rutas "#/builders"; sin hash cae en un clon del marketing y desorienta.
import glob as _glob
_gi = os.path.join(PUB, "index.html")
if os.path.exists(_gi):
    _s0 = open(_gi, encoding="utf-8").read()
    # po63: la entrada PUBLICA usa ?r=builders (la query SI sobrevive al redirect
    # de Cloudflare Access; el hash #/builders se perdia y caia en el clon)
    _s = _s0.replace('full-hub-gated-site.html#/builders', 'full-hub-gated-site.html?r=builders')
    if 'full-hub-gated-site.html?r=builders' not in _s:
        _s = _s.replace('full-hub-gated-site.html', 'full-hub-gated-site.html?r=builders')
    if _s != _s0:
        open(_gi, "w", encoding="utf-8").write(_s)
        print("- marketing Builders link → ?r=builders (sobrevive a Access)")
for _hp in _glob.glob(os.path.join(PUB, "hub", "*.html")):
    if _hp.endswith("full-hub-gated-site.html"): continue
    _s = open(_hp, encoding="utf-8").read()
    if 'full-hub-gated-site.html"' in _s and 'full-hub-gated-site.html#/builders' not in _s:
        _s = _s.replace('full-hub-gated-site.html"', 'full-hub-gated-site.html#/builders"')
        open(_hp, "w", encoding="utf-8").write(_s)
        print(f"- back-link → #/builders en {os.path.basename(_hp)}")
# mailtos huerfanos del marketing (build@/invest@ no existen en IONOS) -> contact@
_gm = os.path.join(PUB, "index.html")
if os.path.exists(_gm):
    _s = open(_gm, encoding="utf-8").read(); _o = _s
    _s = _s.replace('mailto:build@nutrisynccollective.com',
                    'mailto:contact@nutrisynccollective.com?subject=Builders%20NutriSync')
    _s = _s.replace('mailto:invest@nutrisynccollective.com',
                    'mailto:contact@nutrisynccollective.com?subject=Pitch%20NutriSync')
    # tambien el TEXTO visible del email (no solo el href)
    _s = _s.replace('>build@nutrisynccollective.com<', '>contact@nutrisynccollective.com<')
    _s = _s.replace('>invest@nutrisynccollective.com<', '>contact@nutrisynccollective.com<')
    if _s != _o:
        open(_gm, "w", encoding="utf-8").write(_s)
        print("- mailtos build@/invest@ redirigidos a contact@ (href + texto visible)")

# ns-pitch-rename: la zona "Investors" es la sala de materiales de PITCH de las
# founders (decision 3-ago: solo los 4 gmails; se queda tras Access). Rename visible.
for _pp, _reps in (
    (os.path.join(PUB, "index.html"), (('>Investors<', '>Pitch<'),)),
    (os.path.join(PUB, "hub", "full-hub-gated-site.html"),
     (('>Investors<', '>Pitch<'), ('Investor Room', 'Pitch Room'), ('Investor space', 'Sala Pitch'))),
    (os.path.join(PUB, "hub", "investors-business-case.html"),
     (('Investor Room', 'Pitch Room'), ('Investors — ', 'Pitch — '), ('Investor Business Case', 'Pitch — Business Case'))),
):
    if os.path.exists(_pp):
        _s = open(_pp, encoding="utf-8").read(); _o = _s
        for _a, _b in _reps: _s = _s.replace(_a, _b)
        if _s != _o:
            open(_pp, "w", encoding="utf-8").write(_s)
            print(f"- pitch rename en {os.path.basename(_pp)}")

# anchors muertos del footer del payload (#team/#science sin sección) → #platform
_gi2 = os.path.join(PUB, "index.html")
if os.path.exists(_gi2):
    _s = open(_gi2, encoding="utf-8").read()
    _n = 0
    for _bad in ('href=\\"#team\\"', 'href=\\"#science\\"', 'href="#team"', 'href="#science"'):
        _fixed = _bad.replace('#team', '#platform').replace('#science', '#platform')
        if _bad in _s:
            _s = _s.replace(_bad, _fixed); _n += 1
    if _n:
        open(_gi2, "w", encoding="utf-8").write(_s)
        print(f"- footer anchors muertos (#team/#science) -> #platform ({_n})")

# ns-hub-navbar (po57): barra de navegación tipo TABS en TODAS las herramientas
# del hub — atrás/adelante/inicio grandes + clasificador de secciones con la
# pestaña activa marcada. Sustituye a la pastilla flotante (que era minúscula).
# Refresh-on-change: se quita el bloque previo y se reinyecta la versión actual.
_nbf = os.path.join(ASSETS, "hub-navbar.html")
if os.path.exists(_nbf):
    _nbs = open(_nbf, encoding="utf-8").read()
    # po64: shell en TODAS las páginas del hub — incluido el gated de Builders
    # (petición Juanjo) y la documentación (hrefs ya absolutos /hub/...)
    _pages = _glob.glob(os.path.join(PUB, "hub", "*.html")) + \
             _glob.glob(os.path.join(PUB, "hub", "documentation", "*.html"))
    for _hp in _pages:
        _bn = os.path.basename(_hp)
        if _bn == "index.html" and os.path.dirname(_hp).endswith("hub"):
            continue   # la puerta /hub es un redirect puro, sin UI
        _s0 = open(_hp, encoding="utf-8").read()
        _s = re.sub(r"<!-- ns-hub-navbar -->.*?<!-- /ns-hub-navbar -->", "", _s0, flags=re.S)
        _s = re.sub(r'<a id="ns-hub-back".*?</a>', "", _s, flags=re.S)   # adiós pastilla
        _mm = re.search(r"<body[^>]*>", _s)
        if _mm:
            _s = _s[:_mm.end()] + _nbs + _s[_mm.end():]
        if _s != _s0:
            open(_hp, "w", encoding="utf-8").write(_s)
            print(f"- barra tabs de navegación hub en {_bn}")

# pastilla flotante ‹ Hub en páginas sin vuelta (ns-hub-back, idempotente)
_PILL = ('<a id="ns-hub-back" href="full-hub-gated-site.html#/builders" '
         'style="position:fixed;top:14px;left:14px;z-index:9999;background:#fff;'
         'border:1px solid #EADFD5;border-radius:999px;padding:6px 14px;'
         'font:600 13px system-ui;color:#8A7F78;text-decoration:none;'
         'box-shadow:0 2px 8px rgba(0,0,0,.08)">&#8249; Hub</a>')
import re as _re3
for _hp in _glob.glob(os.path.join(PUB, "hub", "*.html")):
    _bn = os.path.basename(_hp)
    if _bn in ("full-hub-gated-site.html", "index.html"): continue
    _s = open(_hp, encoding="utf-8").read()
    if 'full-hub-gated-site.html#/builders' in _s or 'ns-hub-back' in _s: continue
    _m = _re3.search(r'<body[^>]*>', _s)
    if _m:
        _s = _s[:_m.end()] + _PILL + _s[_m.end():]
        open(_hp, "w", encoding="utf-8").write(_s)
        print(f"- pastilla \u2039 Hub en {_bn}")

_hidx = os.path.join(ASSETS, "hub-index.html")
if os.path.exists(_hidx):
    shutil.copy(_hidx, os.path.join(PUB, "hub", "index.html"))
    print("- hub/index.html (puerta /hub) creado → #/builders")

# ---------------------------------------------------------------------------
# ns-selfhost (po74, requisito jurídico): CERO CDNs de terceros en el sitio.
# Copia fuentes variables (fontsource) y librerías UMD a /assets y reescribe
# TODAS las páginas: Google Fonts → /assets/fonts/fonts.css · esm.sh →
# window.supabase local · unpkg → react local. Corre el ÚLTIMO para barrer
# también lo que otros pasos inyectan. Idempotente + refresh-on-change.
_shd = os.path.join(ASSETS, "selfhost")
if os.path.isdir(_shd):
    _af = os.path.join(PUB, "assets", "fonts"); _av = os.path.join(PUB, "assets", "vendor")
    os.makedirs(os.path.join(_af, "files"), exist_ok=True); os.makedirs(_av, exist_ok=True)
    shutil.copy(os.path.join(_shd, "fonts", "fonts.css"), os.path.join(_af, "fonts.css"))
    for _f in os.listdir(os.path.join(_shd, "fonts", "files")):
        shutil.copy(os.path.join(_shd, "fonts", "files", _f), os.path.join(_af, "files", _f))
    for _f in os.listdir(os.path.join(_shd, "vendor")):
        shutil.copy(os.path.join(_shd, "vendor", _f), os.path.join(_av, _f))

    _pages = (_glob.glob(os.path.join(PUB, "*.html"))
              + _glob.glob(os.path.join(PUB, "hub", "*.html"))
              + _glob.glob(os.path.join(PUB, "hub", "documentation", "*.html"))
              + _glob.glob(os.path.join(PUB, "legal", "*.html")))
    _nrw = 0
    for _hp in _pages:
        _s0 = open(_hp, encoding="utf-8", errors="ignore").read(); _s = _s0
        # 1 · Google Fonts → hoja local. LECCIÓN po74: el <link> puede vivir DENTRO
        # del JSON del motor (comillas escapadas \") — el reemplazo debe respetar
        # el contexto de escape o el payload deja de parsear ("Error unpacking").
        if "fonts.googleapis.com" in _s or "fonts.gstatic.com" in _s:
            _links = re.findall(r'<link[^>]*fonts\.g(?:oogleapis|static)\.com[^>]*>', _s)
            _first = True
            for _lk in _links:
                if _first:
                    if '\\"' in _lk:   # contexto JSON-escapado
                        _rep = '<link rel=\\"stylesheet\\" href=\\"/assets/fonts/fonts.css\\">'
                    else:              # HTML crudo
                        _rep = '<link rel="stylesheet" href="/assets/fonts/fonts.css">'
                    _first = False
                else:
                    _rep = ""
                _s = _s.replace(_lk, _rep, 1)
        # 2 · esm.sh supabase-js → UMD local + global
        for _q in ("'", '"'):
            _imp = f"import {{ createClient }} from {_q}https://esm.sh/@supabase/supabase-js@2{_q};"
            if _imp in _s:
                _s = _s.replace(_imp, "const { createClient } = window.supabase;")
            # variante: import DINÁMICO dentro del payload del motor (app.html)
            _dyn = f"await import({_q}https://esm.sh/@supabase/supabase-js@2{_q})"
            if _dyn in _s:
                _s = _s.replace(_dyn, "(window.supabase)")
        if "esm.sh" not in _s and "window.supabase" in _s and "/assets/vendor/supabase.js" not in _s:
            _tag = '<script src="/assets/vendor/supabase.js"></script>'
            _s = _s.replace("</head>", _tag + "</head>", 1) if "</head>" in _s \
                 else re.sub(r"(<script type=\"module\">)", _tag + r"\1", _s, count=1)
        # 3 · unpkg react/react-dom → local
        _s = _s.replace("https://unpkg.com/react@18.3.1/umd/react.production.min.js", "/assets/vendor/react.production.min.js")
        _s = _s.replace("https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js", "/assets/vendor/react-dom.production.min.js")
        if _s != _s0:
            open(_hp, "w", encoding="utf-8").write(_s); _nrw += 1
    print(f"- ns-selfhost: fuentes+librerias locales · {_nrw} paginas reescritas sin CDNs")

# ns-assets-index (r12): galería navegable de los recursos gráficos —
# /assets/figma/ no tenía índice y el linkcheck lo cazó como enlace roto.
_afig = os.path.join(PUB, "assets", "figma")
if os.path.isdir(_afig):
    _files = sorted(f for f in os.listdir(_afig) if f.lower().endswith((".svg", ".png", ".jpg")) )
    _cards = "".join(
        '<a class="a" href="%s" target="_blank" rel="noopener"><span class="t">'
        '<img src="%s" alt="" loading="lazy"></span><span class="n">%s</span></a>' % (f, f, f)
        for f in _files)
    _idx = (
        '<!doctype html><html lang="es"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Recursos gráficos · NutriSync</title><style>'
        "body{margin:0;font-family:'Poppins',system-ui,sans-serif;background:#FFFDF8;color:#231F20;line-height:1.6}"
        ".w{max-width:1100px;margin:0 auto;padding:28px 22px 70px}"
        "h1{font-size:24px;margin:6px 0 4px}p{color:#6E655D;font-size:13.5px;margin:0 0 18px}"
        "a.back{color:#C73A20;font-size:13px;text-decoration:none;font-weight:700}"
        ".g{display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:12px}"
        ".a{display:block;background:#fff;border:1px solid #EFE3D7;border-radius:14px;padding:12px;"
        "text-decoration:none;color:#231F20}.a:hover{border-color:#F3C8B8}"
        ".t{display:flex;align-items:center;justify-content:center;height:78px;margin-bottom:8px}"
        ".t img{max-width:100%%;max-height:100%%}"
        ".n{font-size:11px;color:#6E655D;word-break:break-all;display:block;text-align:center}"
        "</style></head><body><div class=\"w\">"
        '<a class="back" href="/hub/prototypes.html">&#8249; Prototipos</a>'
        "<h1>Recursos gráficos</h1>"
        "<p>%d piezas exportadas de Figma (iconos, avatares, ilustraciones). Clic para abrir el fichero original.</p>"
        '<div class="g">%s</div></div></body></html>' % (len(_files), _cards))
    open(os.path.join(_afig, "index.html"), "w", encoding="utf-8").write(_idx)
    print(f"- ns-assets-index: galería de {len(_files)} recursos en /assets/figma/")

# ── ns-admin-door ────────────────────────────────────────────────────────────
# Tercera puerta en el pie del marketing, junto a Pitch y Builders: StartUp
# Admin (r13). Vive en OTRO dominio (admin.nutrisynccollective.com), pero la
# entrada tiene que estar donde ya está el resto: si no, nadie la encuentra.
#
# El ancla se CLONA de la de Builders en lugar de escribirse a mano: el pie vive
# dentro del payload JSON del motor y reutilizar la cadena real hereda su
# escapado exacto (lección po74).
#
# OJO con las barras: dentro de un valor de atributo van LITERALES (hub/x.html);
# solo las etiquetas de cierre llevan <\u002F. Confundirlas dejó una vez el href
# como "hub/https://..." — enlace roto. Por eso ahora se sustituye el href
# ENTERO (comilla a comilla) y se verifica el resultado antes de escribir.
_ad = os.path.join(PUB, "index.html")
if os.path.exists(_ad):
    _s0 = open(_ad, encoding="utf-8").read()
    if "ns-admin-door" in _s0:
        pass  # ya integrado — el bloque es idempotente
    else:
        _k = _s0.find("?r=builders")
        _open = _s0.rfind("<a href=", 0, _k) if _k > 0 else -1
        _close = _s0.find("<\\u002Fa>", _k) if _k > 0 else -1
        if _open < 0 or _close < 0:
            print("! ns-admin-door: no acoté el ancla de Builders — SIN TOCAR")
        else:
            _close += len("<\\u002Fa>")
            _anchor = _s0[_open:_close]
            _URL = "https://admin.nutrisynccollective.com"
            # 1) href entero, de comilla a comilla (sea cual sea el prefijo)
            _href_re = re.compile(r'href=\\"[^"\\]*full-hub-gated-site\.html\?r=builders\\"')
            _n_href = len(_href_re.findall(_anchor))
            _new = _href_re.sub('href=\\\\"%s\\\\" target=\\\\"_blank\\\\" rel=\\\\"noopener\\\\"' % _URL,
                                _anchor)
            # 2) icono propio: libro mayor
            _icon_old = '<path d=\\"M8.5 8L4.5 12l4 4M15.5 8l4 4-4 4\\"><\\u002Fpath>'
            _icon_new = ('<path d=\\"M5 4.5h11.5a2 2 0 012 2v13H7a2 2 0 01-2-2z\\"><\\u002Fpath>'
                         '<path d=\\"M8.5 9h7M8.5 12.5h7M8.5 16h4\\"><\\u002Fpath>')
            _n_icon = _new.count(_icon_old)
            _new = _new.replace(_icon_old, _icon_new)
            # 3) etiqueta visible + marca del bloque
            _n_lbl = _new.count(">Builders<")
            _new = _new.replace(">Builders<", ">StartUp Admin<")
            _new = _new.replace("<a href=", "<a data-ns=\\\"ns-admin-door\\\" href=", 1)
            # 4) el href final tiene que ser EXACTAMENTE la url absoluta
            _hrefs = re.findall(r'href=\\"([^"\\]*)\\"', _new)
            _ok = (_n_href == 1 and _n_icon == 1 and _n_lbl == 1
                   and _hrefs == [_URL] and ">StartUp Admin<" in _new)
            if not _ok:
                print("! ns-admin-door: el clon no quedó limpio (href=%r) — SIN TOCAR" % (_hrefs,))
            else:
                _s = _s0[:_close] + "\\n          " + _new + _s0[_close:]
                # C2: el payload tiene que seguir siendo JSON válido
                import json as _json2
                _bad = False
                for _m in re.finditer(r'<script type="application/json"[^>]*>(.*?)</script>', _s, re.S):
                    try:
                        _json2.loads(_m.group(1))
                    except Exception as _e:
                        _bad = True
                        print("! ns-admin-door: rompería el payload (%s) — SIN TOCAR" % _e)
                        break
                if not _bad:
                    open(_ad, "w", encoding="utf-8").write(_s)
                    print("- ns-admin-door: 3ª puerta → %s" % _URL)

# ── ns-doors-grid ────────────────────────────────────────────────────────────
# Las 3 puertas del pie en rejilla 2×2 con la tercera ocupando las dos columnas.
# Con flex-wrap cada ficha medía lo que su texto ("StartUp Admin" es más ancho
# que "Pitch") y la segunda fila quedaba descolgada. Con grid, las dos de arriba
# comparten ancho y la de abajo mide exactamente su suma — alineación garantizada
# sin depender de la longitud de las etiquetas ni del idioma.
# En una sola fila no caben: la columna de marca son 290px y tres fichas piden 400+.
_dg = os.path.join(PUB, "index.html")
if os.path.exists(_dg):
    _s0 = open(_dg, encoding="utf-8").read()
    if "ns-doors-grid" in _s0:
        pass  # idempotente
    else:
        _i = _s0.find("2FA SECURED")
        _j = _s0.rfind("<div style=", 0, _i) if _i > 0 else -1
        _end = _s0.find("\\\">", _j) + 3 if _j > 0 else -1
        if _j < 0 or _end < 3:
            print("! ns-doors-grid: no acoté el contenedor de las puertas — SIN TOCAR")
        else:
            _cont_old = _s0[_j:_end]
            if "display: flex" not in _cont_old:
                print("! ns-doors-grid: el contenedor no es el esperado — SIN TOCAR")
            else:
                _cont_new = ('<div data-ns=\\"ns-doors-grid\\" style=\\"display: grid; '
                             'grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 14px; '
                             'max-width: 340px;\\">')
                _s = _s0[:_j] + _cont_new + _s0[_end:]
                # la 3ª puerta ocupa las dos columnas
                _k = _s.find("ns-admin-door")
                _a = _s.rfind("<a ", 0, _k) if _k > 0 else -1
                _st = _s.find("style=\\\"", _a) if _a > 0 else -1
                if _st < 0:
                    print("! ns-doors-grid: no encontré el style de la 3ª puerta — SIN TOCAR")
                else:
                    _st += len("style=\\\"")
                    _s = _s[:_st] + "grid-column: 1 \\u002F -1; justify-content: center; " + _s[_st:]
                    import json as _json3
                    _bad = False
                    for _m in re.finditer(r'<script type="application/json"[^>]*>(.*?)</script>',
                                          _s, re.S):
                        try:
                            _json3.loads(_m.group(1))
                        except Exception as _e:
                            _bad = True
                            print("! ns-doors-grid: rompería el payload (%s) — SIN TOCAR" % _e)
                            break
                    if not _bad:
                        open(_dg, "w", encoding="utf-8").write(_s)
                        print("- ns-doors-grid: 3 puertas en rejilla 2×2 (la 3ª a doble ancho)")

# ── ns-footer-brand ──────────────────────────────────────────────────────────
# El QR parecía descolgado de la columna Legal, pero la causa no era que las
# columnas estuvieran demasiado a la izquierda: era que el bloque de marca es
# demasiado estrecho (290px). Con space-between, el sobrante se reparte entre
# las 4 columnas → huecos de 115px. Ensanchando la marca a 400px el sobrante
# baja y el ritmo queda UNIFORME en 78px, QR incluido. Medido a 1200px.
# Empaquetarlas a la derecha (flex-end) fue un error: cerraba el hueco del QR
# pero abría un vacío de 223px en el centro del pie.
_fb = os.path.join(PUB, "index.html")
if os.path.exists(_fb):
    _s0 = open(_fb, encoding="utf-8").read()
    _reps = [
        # columna de marca: 290 → 400 (el párrafo cabe en 2 líneas, no 3)
        ('style=\\"flex: 0 1 290px; min-width: 240px;\\"',
         'data-ns=\\"ns-footer-brand\\" style=\\"flex: 0 1 400px; min-width: 240px;\\"'),
        ('color: #B8ADA4; max-width: 290px;', 'color: #B8ADA4; max-width: 380px;'),
        # las fichas no crecen con la columna: se quedan en 340
        ('grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 14px; max-width: 340px;',
         'grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 14px; max-width: 340px;'),
    ]
    if "ns-footer-brand" in _s0:
        pass  # idempotente
    else:
        _s = _s0
        _fallos = []
        for _a, _b in _reps:
            if _a == _b:
                continue
            if _s.count(_a) != 1:
                _fallos.append((_a[:40], _s.count(_a)))
            else:
                _s = _s.replace(_a, _b)
        if _fallos:
            print("! ns-footer-brand: anclas no únicas %s — SIN TOCAR" % _fallos)
        else:
            import json as _json4
            _bad = False
            for _m in re.finditer(r'<script type="application/json"[^>]*>(.*?)</script>', _s, re.S):
                try:
                    _json4.loads(_m.group(1))
                except Exception as _e:
                    _bad = True
                    print("! ns-footer-brand: rompería el payload (%s) — SIN TOCAR" % _e)
                    break
            if not _bad:
                open(_fb, "w", encoding="utf-8").write(_s)
                print("- ns-footer-brand: columna de marca a 400px (ritmo del pie uniforme)")

# ns-pitch-deck (r13c): el deck de agosto 2026 con su historia y el enlace de
# Canva, dentro de la página del Pitch (que es de Design: el pack la trae y
# este bloque la re-decora en cada integración). El PDF pesa 28 MB — por
# encima del límite de 25 MiB de Pages — así que el enlace canónico es Canva
# y el fichero queda en inputs/ (no se sirve).
_idocs_src = os.path.join(ASSETS, "investor-docs")
_idocs_dst = os.path.join(PUB, "hub", "docs")
if os.path.isdir(_idocs_src):
    os.makedirs(_idocs_dst, exist_ok=True)
    for _f in os.listdir(_idocs_src):
        shutil.copy(os.path.join(_idocs_src, _f), os.path.join(_idocs_dst, _f))
    print(f"- investor-docs: {len(os.listdir(_idocs_src))} fichero(s) en /hub/docs/")
_ibc = os.path.join(PUB, "hub", "investors-business-case.html")
if os.path.exists(_ibc):
    _bh = open(_ibc, encoding="utf-8").read()
    _bh = re.sub(r'<div id="ns-pitch-deck">[\s\S]*?</div><!-- /ns-pitch-deck -->', '', _bh)
    _ANCLA_DOCS = '<h2 class="title" style="margin-top:14px;">Documents</h2>'
    _CARD = ('<div id="ns-pitch-deck">'
      '<div style="background:linear-gradient(135deg,#241D1A,#3A2F2A);border-radius:18px;padding:22px 24px;margin:14px 0;color:#F5EFE7">'
      '<div style="font-size:10.5px;font-weight:800;letter-spacing:.14em;color:#FFB48A;text-transform:uppercase">Pitch deck · August 2026 · updated</div>'
      '<div style="font-size:19px;font-weight:800;margin:6px 0 2px">NutriSync — Hormonal care made easy</div>'
      '<div style="font-size:12.5px;color:#D8CCC2;line-height:1.65;margin:8px 0 4px">The storyline: '
      'most nutrition was built for men — women\'s 28-day cycles were left out ("Different biology. Same nutrition?"). '
      'NutriSync turns cycle data into <b>adaptive, science-backed guidance</b> (Cycle Alignment + Cycle Stability scores) '
      'measured against each woman\'s own baseline, with privacy by design. '
      'A $5.07Bn menstrual-health market by 2030 (20.2% CAGR); Spanish beachhead €1.4Bn TAM / €168M SAM. '
      'Traction: 160 interviews (96% report cycle impacts performance), 150-women waitlist, 30k organic views, '
      'early paid events revenue, and podium finishes at IE Venture Lab, IE Entrepreneurship Summit and ESADE Shark Tank. '
      'On track to launch to 200 beta users in Q3 2026.</div>'
      '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;align-items:center">'
      '<a href="https://canva.link/0e050fpa0ewj4e4" target="_blank" rel="noopener" '
      'style="display:inline-block;background:linear-gradient(135deg,#FF7600,#FD400C);color:#fff;font-weight:800;'
      'font-size:13px;border-radius:22px;padding:10px 20px;text-decoration:none">▶ View the deck on Canva</a>'
      '<a href="/hub/docs/NutriSync-Financial-Model-2026-08.xlsx" '
      'style="display:inline-block;background:#fff;color:#241D1A;font-weight:800;font-size:13px;'
      'border-radius:22px;padding:10px 20px;text-decoration:none">📊 Financial model (Excel · Aug 2026)</a>'
      '<span style="font-size:11px;color:#B8AAA0">Deck PDF/PPTX archived internally (28 MB) · ask contact@nutrisynccollective.com</span>'
      '</div></div></div><!-- /ns-pitch-deck -->')
    if _ANCLA_DOCS in _bh:
        _bh = _bh.replace(_ANCLA_DOCS, _ANCLA_DOCS + _CARD, 1)
        open(_ibc, "w", encoding="utf-8").write(_bh)
        print("- ns-pitch-deck: deck agosto 2026 + Canva en la pagina del Pitch")
    else:
        print("- AVISO ns-pitch-deck: el ancla Documents no esta — Design la movio, revisar")

# ÚLTIMO PASO (r13c): el banner va al final — cualquier paso anterior que
# reescriba index.html desde una copia vieja lo perdería (medido, no teoría).
# ns-pilot-banner (r13c, requisito legal): franja fija al pie de la web de
# marketing — NutriSync en desarrollo, piloto interno cerrado, no comercializado.
# En línea + vigilante (po82): el re-render del motor no puede borrarla.
for _pg in ("index.html", "app.html"):
    _pp = os.path.join(PUB, _pg)
    if os.path.exists(_pp):
        _ph = open(_pp, encoding="utf-8").read()
        _ph = re.sub(r'<script id="ns-pilot-banner">.*?</script>', '', _ph, flags=re.S)
        _PB = ('<script id="ns-pilot-banner">(function(){'
          "var ES=(navigator.language||'en').toLowerCase().indexOf('es')===0;"
          "var TXT=ES?'🚧 NutriSync está en fase de desarrollo · piloto interno cerrado — aún no disponible para el público · <a href=\"mailto:contact@nutrisynccollective.com\" style=\"color:#FFB48A;text-decoration:underline\">contact@nutrisynccollective.com</a>'"
          ":'🚧 NutriSync is in development · closed internal pilot — not yet available to the public · <a href=\"mailto:contact@nutrisynccollective.com\" style=\"color:#FFB48A;text-decoration:underline\">contact@nutrisynccollective.com</a>';"
          "function put(){"
          "if(document.getElementById('ns-pilot-bar'))return;"
          "var d=document.createElement('div');d.id='ns-pilot-bar';"
          "d.style.cssText='position:fixed;left:0;right:0;bottom:0;z-index:380;background:#241D1A;color:#F5EFE7;font:600 11.5px/1.4 Poppins,system-ui,sans-serif;text-align:center;padding:8px 14px;letter-spacing:.2px;box-shadow:0 -4px 18px rgba(0,0,0,.18)';"
          "d.innerHTML=TXT;document.body.appendChild(d);}"
          "if(document.readyState!=='loading')put();else document.addEventListener('DOMContentLoaded',put);"
          "setInterval(put,1500);"
          '})();</script>')
        open(_pp, "w", encoding="utf-8").write(_ph.replace("</head>", _PB + "</head>", 1))
        print(f"- ns-pilot-banner en {_pg} (franja fija de fase de desarrollo)")
