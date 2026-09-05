# -*- coding: utf-8 -*-
"""r12 · Genera _integration/prototypes.html — "NutriSync Concept in Visuals".
Storytelling + recursos gráficos + 4 superficies (marketing · app · web-app ·
builders&pitch), cada una con explicación, prototipo, customer journey y
pantallas. Bilingüe ES/EN con toggle (regla: nunca etiquetas mezcladas).
Editar aquí y ejecutar: python3 _integration/gen_prototypes.py"""
import os, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prototypes.html')

# ── Enlaces de Figma (pendientes de que Design/Lucía los compartan) ──────────
FIGMA = [
    # (etiqueta ES, etiqueta EN, url o '' si aún no la tenemos)
    ("Sistema de diseño (tokens, componentes)", "Design system (tokens, components)", ""),
    ("Web marketing — maquetas", "Marketing site — mockups", ""),
    ("Prototipo MVP — wireframes navegables", "MVP prototype — clickable wireframes",
     "https://www.figma.com/proto/WO6e1uPGMyy20h0bnv3UE0/NutriSync-MVP-Wireframe?node-id=0-1&t=nys25tnI4uI7zTzg-1"),
    ("Trends / Cycle Intelligence (en curso)", "Trends / Cycle Intelligence (WIP)", ""),
]

ASSETS = [
    ("Logo y marca", "Logo & brand", "/assets/figma/", "SVG · wordmark, isotipo, alas"),
    ("Iconografía", "Iconography", "/assets/figma/", "SVG · navegación, fases, síntomas"),
    ("Paleta y tipografía", "Palette & type", "/legal/", "Coral #E8472A · Poppins + Inter"),
    ("Deck de inversión", "Investor deck", "/hub/assets/NutriSync-deck.pdf", "PDF"),
    ("Dataroom", "Data room", "/hub/investors-business-case.html", "Modelo financiero · benchmarks"),
]

SECTIONS = [
    dict(
        n="1", key="marketing",
        t_es="Prototipo · Web de marketing", t_en="Prototype · Marketing site",
        d_es="La puerta de entrada pública: explica el problema (la medicina se construyó para la biología "
             "masculina), la propuesta de NutriSync y capta la lista de espera. Es la superficie que ven "
             "inversoras, prensa y las primeras usuarias.",
        d_en="The public front door: it frames the problem (medicine was built for male biology), presents "
             "the NutriSync proposition and captures the waiting list. This is the surface investors, press "
             "and first users see.",
        cta="https://nutrisynccollective.com/", cta_es="Abrir la web", cta_en="Open the site",
        journey_es=["Llega desde redes o boca a boca", "Entiende el problema en 15 segundos",
                    "Ve cómo funciona por fases del ciclo", "Consulta la ciencia y el equipo",
                    "Se apunta a la lista de espera", "Recibe su invitación al piloto"],
        journey_en=["Arrives from social or word of mouth", "Gets the problem in 15 seconds",
                    "Sees how it works across cycle phases", "Checks the science and the team",
                    "Joins the waiting list", "Receives a pilot invitation"],
        screens=[("Portada y problema", "Hero & problem", "https://nutrisynccollective.com/"),
                 ("Plataforma", "Platform", "https://nutrisynccollective.com/#platform"),
                 ("Pantallas de la app", "App screens", "https://nutrisynccollective.com/#screens"),
                 ("Precios", "Pricing", "https://nutrisynccollective.com/#pricing"),
                 ("Documentos legales", "Legal documents", "/legal/")],
    ),
    dict(
        n="2", key="app",
        t_es="Prototipo · App móvil", t_en="Prototype · Mobile app",
        d_es="El producto diario. Una sola base de código React Native se publica en <b>tres superficies</b>: "
             "iOS (TestFlight → App Store), Android (Google Play) y la <b>PWA</b> en m.nutrisynccollective.com, "
             "que sirve como prototipo navegable sin instalar nada. Lo que ves en la PWA es literalmente la app.",
        d_en="The daily product. A single React Native codebase ships to <b>three surfaces</b>: iOS "
             "(TestFlight → App Store), Android (Google Play) and the <b>PWA</b> at m.nutrisynccollective.com, "
             "which doubles as an install-free navigable prototype. What you see in the PWA is literally the app.",
        cta="https://m.nutrisynccollective.com/", cta_es="Abrir la PWA (app real)", cta_en="Open the PWA (real app)",
        journey_es=["Instala o abre la PWA", "Crea cuenta con correo, Google o Apple",
                    "Onboarding: ciclo, cuerpo, objetivos", "Check-in diario de ánimo y energía",
                    "Home: anillo del ciclo y fase de hoy", "Registra comida y movimiento",
                    "Progress: Cycle Alignment y estabilidad", "Calendario y Tendencias del ciclo"],
        journey_en=["Installs or opens the PWA", "Signs up with email, Google or Apple",
                    "Onboarding: cycle, body, goals", "Daily mood & energy check-in",
                    "Home: cycle ring and today's phase", "Logs food and movement",
                    "Progress: Cycle Alignment and stability", "Calendar and cycle Trends"],
        screens=[("Inicio de sesión", "Log in", "https://m.nutrisynccollective.com/"),
                 ("Onboarding", "Onboarding", "https://m.nutrisynccollective.com/"),
                 ("Home · anillo del ciclo", "Home · cycle ring", "https://m.nutrisynccollective.com/"),
                 ("NutriLog", "NutriLog", "https://m.nutrisynccollective.com/"),
                 ("Movimiento", "Movement", "https://m.nutrisynccollective.com/"),
                 ("Progress", "Progress", "https://m.nutrisynccollective.com/"),
                 ("Calendario y Tendencias", "Calendar & Trends", "https://m.nutrisynccollective.com/"),
                 ("Ajustes y privacidad", "Settings & privacy", "https://m.nutrisynccollective.com/")],
        note_es="iOS y Android reciben exactamente estas pantallas; las diferencias son de sistema operativo "
                "(biometría, notificaciones, tiendas), no de producto.",
        note_en="iOS and Android get exactly these screens; differences are OS-level (biometrics, notifications, "
                "stores), not product-level.",
    ),
    dict(
        n="3", key="webapp",
        t_es="Prototipo · Web-app", t_en="Prototype · Web app",
        d_es="La misma experiencia en navegador de escritorio, pensada para quien prefiere teclado y pantalla "
             "grande, y para demos. Se abre en <b>modo prototipo</b> con datos de ejemplo: navegación completa, "
             "sin cuenta y sin escribir en la base de datos real.",
        d_en="The same experience in a desktop browser, for people who prefer keyboard and big screen, and for "
             "demos. It opens in <b>prototype mode</b> with sample data: full navigation, no account, nothing "
             "written to the real database.",
        cta="/webapp.html#demo", cta_es="Abrir el prototipo web", cta_en="Open the web prototype",
        journey_es=["Alta y acceso", "Onboarding guiado", "Uso diario", "Seguimiento y ajustes"],
        journey_en=["Sign-up and access", "Guided onboarding", "Daily use", "Tracking and settings"],
        groups=[("Alta y acceso", "Sign-up & access",
                 [("login", "Iniciar sesión", "Log in"), ("signup", "Crear cuenta", "Create account"),
                  ("onboarding", "Asistente de onboarding", "Onboarding wizard"), ("allset", "Todo listo", "All set")]),
                ("Experiencia diaria", "Daily experience",
                 [("gate", "Check-in diario", "Daily check-in"), ("home", "Home · Cycle Alignment", "Home · Cycle Alignment"),
                  ("nutrilog", "NutriLog", "NutriLog"), ("movement", "Movimiento", "Movement")]),
                ("Seguimiento", "Tracking",
                 [("editperiod", "Editar período", "Edit period"), ("edithealth", "Editar salud", "Edit health"),
                  ("progress", "Progress", "Progress"), ("calendar", "Calendario", "Calendar")]),
                ("Cuenta y privacidad", "Account & privacy",
                 [("settings", "Ajustes", "Settings"), ("connections", "Conexiones", "Connections"),
                  ("privacy", "Privacidad", "Privacy"), ("security", "Seguridad", "Security")])],
    ),
    dict(
        n="4", key="builders",
        t_es="Prototipo · Builders &amp; Pitch", t_en="Prototype · Builders &amp; Pitch",
        d_es="La trastienda: el hub donde el equipo gobierna el producto (MIS, finanzas, piloto, feedback, "
             "traducciones, documentación) y la sala de Pitch con los materiales de inversión. Protegido por "
             "dos capas: Cloudflare Access y sesión de administradora con doble factor.",
        d_en="The back office: the hub where the team runs the product (MIS, finance, pilot, feedback, "
             "translations, documentation) and the Pitch room with investment materials. Protected by two "
             "layers: Cloudflare Access and an admin session with two-factor.",
        cta="/hub/full-hub-gated-site.html?r=builders", cta_es="Abrir el hub", cta_en="Open the hub",
        journey_es=["Acceso con correo autorizado y PIN", "Sesión de administradora con MFA",
                    "Overview: KPIs y business case", "Operar: piloto, feedback, finanzas",
                    "Consultar documentación viva", "Pitch: deck y dataroom"],
        journey_en=["Access with an allow-listed email and PIN", "Admin session with MFA",
                    "Overview: KPIs and business case", "Operate: pilot, feedback, finance",
                    "Browse living documentation", "Pitch: deck and data room"],
        screens=[("Overview", "Overview", "/hub/full-hub-gated-site.html?r=builders"),
                 ("MIS · KPIs y business case", "MIS · KPIs & business case", "/hub/admin-mis-console.html"),
                 ("Finanzas", "Finance", "/hub/finance.html"),
                 ("Piloto", "Pilot", "/hub/pilot.html"),
                 ("Feedback", "Feedback", "/hub/feedback.html"),
                 ("Documentación", "Documentation", "/hub/documentation/index.html"),
                 ("Pitch · business case", "Pitch · business case", "/hub/investors-business-case.html")],
    ),
]

def bi(es, en):
    """span bilingüe: data-es / data-en (el toggle los intercambia)"""
    return '<span data-es="%s" data-en="%s">%s</span>' % (
        html.escape(es, quote=True), html.escape(en, quote=True), es)

CSS = """
:root{--coral:#E8472A;--coral2:#FF7600;--ink:#231F20;--muted:#6E655D;--line:#EFE3D7;--bg:#FFFDF8}
*{box-sizing:border-box}body{margin:0;font-family:'Poppins',system-ui,sans-serif;color:var(--ink);
background:radial-gradient(circle at 25% 12%,#FDE2D6 0%,#FBEFE6 34%,#FFF8F1 60%,#F9D7BD 100%);min-height:100vh;line-height:1.6}
.wrap{max-width:960px;margin:0 auto;padding:26px 22px 80px}
.top{display:flex;justify-content:space-between;align-items:center;gap:10px}
.lsw{font-size:12.5px;color:var(--muted);cursor:pointer;text-decoration:underline;background:none;border:none;font-family:inherit}
.label{font-size:12px;letter-spacing:.16em;font-weight:800;color:var(--coral)}
h1{font-size:clamp(28px,4.4vw,42px);margin:8px 0 6px;line-height:1.08}
.lead{color:#4A433D;font-size:15.5px;max-width:680px;margin:0 0 6px}
.story{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px 22px;margin:18px 0 8px;box-shadow:0 10px 30px -22px rgba(0,0,0,.5)}
.story p{margin:0 0 10px;font-size:14.5px;color:#4A433D}.story p:last-child{margin:0}
h2{font-size:13px;letter-spacing:.14em;font-weight:800;color:var(--muted);margin:34px 0 12px;text-transform:uppercase}
.res{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:10px}
.rcard{display:block;background:#fff;border:1px solid var(--line);border-radius:13px;padding:13px 15px;text-decoration:none;color:var(--ink)}
.rcard:hover{border-color:#F3C8B8;background:#FFFDF9}
.rname{font-weight:700;font-size:13.5px}.rsub{font-size:11.5px;color:var(--muted)}
.fig{display:flex;flex-wrap:wrap;gap:8px}
.figl{display:inline-flex;align-items:center;gap:7px;background:#fff;border:1px solid var(--line);border-radius:999px;padding:9px 15px;font-size:13px;font-weight:600;text-decoration:none;color:var(--ink)}
.figl.pending{opacity:.55;border-style:dashed;cursor:default}
.sec{background:#fff;border:1px solid var(--line);border-radius:20px;padding:22px 24px;margin:16px 0;box-shadow:0 14px 36px -28px rgba(0,0,0,.55)}
.snum{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:8px;
background:linear-gradient(135deg,var(--coral2),var(--coral));color:#fff;font-weight:800;font-size:13px;margin-right:9px}
.stitle{font-size:19px;font-weight:800;margin:0 0 8px;display:flex;align-items:center}
.sdesc{font-size:14px;color:#4A433D;margin:0 0 14px}
.enter{display:inline-flex;align-items:center;gap:8px;background:linear-gradient(135deg,#EA5740,#F4876F);color:#fff;
text-decoration:none;font-weight:700;font-size:14.5px;padding:12px 20px;border-radius:100px;box-shadow:0 12px 26px -14px rgba(234,87,64,.7)}
.jt{font-size:11.5px;letter-spacing:.12em;font-weight:800;color:var(--muted);margin:20px 0 8px}
.journey{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.jstep{display:inline-flex;align-items:center;gap:7px;background:#FFF6EF;border:1px solid #F3E2D5;border-radius:999px;padding:7px 13px;font-size:12.5px}
.jn{width:18px;height:18px;border-radius:50%;background:var(--coral);color:#fff;font-size:10px;font-weight:800;display:inline-flex;align-items:center;justify-content:center}
.jarrow{color:#D8C9BC;font-weight:800}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:9px}
.pcard{display:flex;align-items:center;gap:10px;background:#FFFDFA;border:1px solid var(--line);border-radius:12px;
padding:12px 14px;text-decoration:none;color:var(--ink)}
.pcard:hover{border-color:#F3C8B8;transform:translateY(-1px)}
.pdot{width:8px;height:8px;border-radius:50%;background:var(--coral);flex:none}
.plabel{font-weight:600;font-size:13.5px;flex:1}.parrow{color:var(--muted);font-weight:700}
.gt{font-size:11.5px;font-weight:800;color:var(--muted);margin:14px 0 7px}
.note{font-size:12.5px;color:var(--muted);margin-top:14px;background:#FFF8EF;border:1px dashed #E8B072;border-radius:12px;padding:10px 13px}
.foot{margin-top:34px;color:var(--muted);font-size:12.5px}
"""

def section_html(s):
    h = ['<div class="sec" id="p%s">' % s['key']]
    h.append('<div class="stitle"><span class="snum">%s</span>%s</div>' % (s['n'], bi(s['t_es'], s['t_en'])))
    h.append('<p class="sdesc">%s</p>' % bi(s['d_es'], s['d_en']))
    h.append('<a class="enter" href="%s" target="_top">%s →</a>' % (s['cta'], bi(s['cta_es'], s['cta_en'])))
    # customer journey
    steps = []
    for i, (a, b) in enumerate(zip(s['journey_es'], s['journey_en'])):
        if i: steps.append('<span class="jarrow">›</span>')
        steps.append('<span class="jstep"><span class="jn">%d</span>%s</span>' % (i + 1, bi(a, b)))
    h.append('<div class="jt">%s</div><div class="journey">%s</div>' % (bi('CUSTOMER JOURNEY', 'CUSTOMER JOURNEY'), ''.join(steps)))
    # pantallas
    h.append('<div class="jt">%s</div>' % bi('PANTALLAS', 'SCREENS'))
    if s.get('groups'):
        for g_es, g_en, items in s['groups']:
            h.append('<div class="gt">%s</div><div class="pgrid">' % bi(g_es, g_en))
            for route, l_es, l_en in items:
                h.append('<a class="pcard" href="/webapp.html#demo-%s" target="_top"><span class="pdot"></span>'
                         '<span class="plabel">%s</span><span class="parrow">→</span></a>' % (route, bi(l_es, l_en)))
            h.append('</div>')
    else:
        h.append('<div class="pgrid">')
        for l_es, l_en, url in s['screens']:
            h.append('<a class="pcard" href="%s" target="_top"><span class="pdot"></span>'
                     '<span class="plabel">%s</span><span class="parrow">→</span></a>' % (url, bi(l_es, l_en)))
        h.append('</div>')
    if s.get('note_es'):
        h.append('<div class="note">%s</div>' % bi(s['note_es'], s['note_en']))
    h.append('</div>')
    return ''.join(h)

figma = []
for l_es, l_en, url in FIGMA:
    if url:
        figma.append('<a class="figl" href="%s" target="_blank" rel="noopener">🎨 %s ↗</a>' % (url, bi(l_es, l_en)))
    else:
        figma.append('<span class="figl pending">🎨 %s · %s</span>' % (bi(l_es, l_en), bi('enlace pendiente', 'link pending')))

resources = ''.join(
    '<a class="rcard" href="%s" target="_top"><div class="rname">%s</div><div class="rsub">%s</div></a>' % (u, bi(a, b), sub)
    for a, b, u, sub in ASSETS)

HTML = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prototipos · NutriSync</title><style>%s</style></head><body><div class="wrap">
<div class="top"><div class="label">PROTOTIPOS</div><button class="lsw" id="lsw" onclick="nsSwap()">EN</button></div>
<h1>%s</h1>
<p class="lead">%s</p>

<div class="story">
<p>%s</p>
<p>%s</p>
<p>%s</p>
</div>

<h2>%s</h2>
<div class="fig">%s</div>

<h2>%s</h2>
<div class="res">%s</div>

<h2>%s</h2>
%s

<p class="foot">%s</p>
</div>
<script>
var NSL=(navigator.language||'en').toLowerCase().indexOf('es')===0?'es':'en';
function nsApply(){document.querySelectorAll('[data-es]').forEach(function(n){n.innerHTML=n.dataset[NSL];});
document.getElementById('lsw').textContent=NSL==='es'?'EN':'ES';document.documentElement.lang=NSL;}
function nsSwap(){NSL=NSL==='es'?'en':'es';nsApply();}
nsApply();
</script></body></html>""" % (
    CSS,
    bi('NutriSync en imágenes', 'NutriSync in visuals'),
    bi('Cuatro superficies, un solo producto. Recorre cada prototipo, su customer journey y sus pantallas.',
       'Four surfaces, one product. Walk through each prototype, its customer journey and its screens.'),
    bi('Durante décadas la medicina y la nutrición se han diseñado sobre un cuerpo de referencia masculino, con un '
       'ciclo hormonal de 24 horas. El cuerpo de la mitad de la población funciona con un ciclo de unos 28 días y '
       'cuatro fases muy distintas — y esa diferencia se ha ignorado.',
       'For decades medicine and nutrition were designed around a male reference body running a 24-hour hormonal '
       'cycle. Half the population runs on a ~28-day cycle with four very different phases — and that difference '
       'has been ignored.'),
    bi('NutriSync existe para cerrar esa brecha: sincroniza nutrición, movimiento y descanso con la fase del ciclo '
       'de cada mujer, aprende de lo que registra y le devuelve pautas concretas para el día de hoy. No diagnostica '
       'ni sustituye a un profesional sanitario: detecta patrones y los explica con claridad.',
       'NutriSync exists to close that gap: it syncs nutrition, movement and rest with each woman\\u2019s cycle phase, '
       'learns from what she logs and hands back concrete guidance for today. It does not diagnose or replace a '
       'health professional: it finds patterns and explains them clearly.'),
    bi('El producto vive en cuatro superficies que comparten un mismo backend y un mismo lenguaje visual: la web '
       'de marketing, la app móvil (iOS, Android y PWA), la web-app de escritorio y el hub interno de Builders con '
       'la sala de Pitch. Abajo puedes recorrerlas una a una.',
       'The product lives on four surfaces sharing one backend and one visual language: the marketing site, the '
       'mobile app (iOS, Android and PWA), the desktop web app, and the internal Builders hub with the Pitch room. '
       'You can walk through each of them below.'),
    bi('Diseño en Figma', 'Design in Figma'), ''.join(figma),
    bi('Recursos gráficos', 'Graphic resources'), resources,
    bi('Las cuatro superficies', 'The four surfaces'),
    ''.join(section_html(s) for s in SECTIONS),
    bi('Los prototipos corren con datos de ejemplo en tu navegador — nada de lo que hagas aquí escribe en una cuenta '
       'real. Página interna del equipo; no se enlaza desde la web pública.',
       'Prototypes run on sample data in your browser — nothing here writes to a real account. Internal team page; '
       'not linked from the public site.'),
)

open(OUT, 'w', encoding='utf-8').write(HTML)
print('prototypes.html generado:', len(HTML) // 1024, 'KB')
