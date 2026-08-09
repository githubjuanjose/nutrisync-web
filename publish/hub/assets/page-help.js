/* NutriSync · page-help (r16-F16) — la ayuda de cada pestaña, en UN solo sitio.
   Se inyecta en todas las páginas del hub desde integrate.py. Cada página saca
   su bloque por el nombre del fichero; si no está en el diccionario, no pinta
   nada (así una página nueva nunca revienta por falta de texto).
   Bilingüe ES/EN a dos columnas — las founders leen en los dos idiomas.
   Plegado por defecto: quien ya lo sabe no lo sufre. La preferencia se recuerda
   por navegador (localStorage), como el idioma y el orden de pestañas (r14e). */
(function () {
  var H = {
    'admin-mis-console.html': {
      t: ['📊 MIS · el cuadro de mando', '📊 MIS · the dashboard'],
      q: ['La foto del negocio: usuarias reales frente al plan, ingresos, gastos y KPIs del piloto.',
          'Business snapshot: actuals vs plan, revenue, costs and pilot KPIs.'],
      c: ['Se mira, no se rellena — todo se calcula solo desde la base de datos y los dos libros.',
          'Read-only: everything is computed from the database and the two ledgers.']
    },
    'finance.html': {
      t: ['💶 Finanzas · el libro de caja', '💶 Finance · cash book'],
      q: ['Entradas y salidas reales de dinero, y la hoja de costes de SaaS con el % imputado al proyecto.',
          'Real money in and out, plus the SaaS cost sheet with the % charged to the project.'],
      c: ['La contabilidad del build (partida doble) vive aparte, en StartUp Admin: son dos cosas a propósito.',
          'The double-entry build ledger lives separately in StartUp Admin — deliberately two things.']
    },
    'investors-business-case.html': {
      t: ['🎯 Pitch · la sala de inversores', '🎯 Pitch · investor room'],
      q: ['El business case presentable: mercado, modelo, escenarios, equipo y data room.',
          'The investor-facing case: market, model, scenarios, team and data room.'],
      c: ['Cada descarga del data room queda registrada.', 'Every data-room download is logged.']
    },
    'competitive.html': {
      t: ['🥊 Competencia · quién hace ya qué', '🥊 Competitive · who already does what'],
      q: ['El informe v1.1: matrices de capacidades, el update de registro de comidas por IA (28 y Aluna) y el hueco que queda libre.',
          'The v1.1 report: capability matrices, the AI meal-logging update (28 and Aluna) and the remaining whitespace.'],
      c: ['Regla de estilo: siempre «sin evidencia pública», nunca «no lo tienen».',
          'Style rule: always “not publicly evidenced”, never “they don’t have it”.']
    },
    'launch-plan.html': {
      t: ['🗺 Plan 8-oct · el camino al lanzamiento', '🗺 Launch plan · road to 8-Oct'],
      q: ['Los hitos hasta el lanzamiento y las dependencias que bloquean a las demás.',
          'Milestones to launch and the dependencies that block the rest.'],
      c: ['Lo que está en el camino crítico manda sobre lo que apetece.',
          'What sits on the critical path beats what feels urgent.']
    },
    'daily-ops.html': {
      t: ['📋 Operación · la salud diaria', '📋 Ops · daily health'],
      q: ['Si los automatismos han corrido bien esta noche (TestFlight, correos, notificaciones) y qué toca hoy.',
          'Whether last night’s automations ran (TestFlight, emails, notifications) and what’s due today.'],
      c: ['Un vistazo por la mañana. Si algo sale en rojo, lo mira ingeniería.',
          'A morning glance. Anything red goes to engineering.']
    },
    'incidents.html': {
      t: ['🎫 Incidencias · el corazón del piloto', '🎫 Incidents · the heart of the pilot'],
      q: ['Cada problema con su ficha: qué pasó, quién lo lleva, prioridad P0-P3 y qué le hemos contado a la usuaria.',
          'One ticket per issue: what happened, who owns it, P0-P3 priority and what we told the user.'],
      c: ['El SOP completo está al pie de esta página. Los bugs entran solos en 🗂 Sprint Planning.',
          'The full SOP is at the bottom of this page. Bugs land automatically in 🗂 Sprint Planning.']
    },
    'feedback.html': {
      t: ['💬 Feedback · la bandeja de entrada', '💬 Feedback · the inbox'],
      q: ['Todo lo que dicen las testers (app y TestFlight 🍎) con sus capturas y crash logs.',
          'Everything testers say (app and TestFlight 🍎) with their screenshots and crash logs.'],
      c: ['Clasifica cada mensaje: 🐞 incidencia · 🔧 mejora · 💡 idea. Al hacerlo sale de la bandeja. Bandeja a cero = todo revisado.',
          'Triage each message: 🐞 incident · 🔧 improvement · 💡 idea. It then leaves the inbox. Empty inbox = all reviewed.']
    },
    'decisions.html': {
      t: ['🗳 Decisiones · lo que bloquea a ingeniería', '🗳 Decisions · what blocks engineering'],
      q: ['Preguntas que solo pueden responder las founders, con opciones cerradas en vez de texto libre.',
          'Questions only founders can answer, with fixed options instead of free text.'],
      c: ['Mientras una decisión siga abierta, algo está parado — el correo diario las recuerda.',
          'While a decision stays open, something is stalled — the daily email chases it.']
    },
    'notifications.html': {
      t: ['🔔 Notificaciones · lo que la app le dice a la usuaria', '🔔 Notifications · what the app tells her'],
      q: ['El catálogo de mensajes push con su texto ES/EN y si están activos.',
          'The push message catalogue with ES/EN copy and on/off state.'],
      c: ['Se revisa el tono (que suene a nosotras, no a robot) y se activa o desactiva cada mensaje.',
          'Review the tone (sound like us, not a robot) and switch each message on or off.']
    },
    'pilot.html': {
      t: ['🧪 Piloto · la operación', '🧪 Pilot · operations'],
      q: ['Invitar, aprobar por lotes, casar cuentas y mandar recordatorios a las testers.',
          'Invite, approve in batches, match accounts and send reminders to testers.'],
      c: ['El plan semanal está en 🗓 Plan piloto y el uso real en 📡 Obs. piloto.',
          'Weekly targets live in 🗓 Pilot plan; real usage in 📡 Pilot obs.']
    },
    'pilot-planning.html': {
      t: ['🗓 Plan piloto · objetivo vs real', '🗓 Pilot plan · target vs actual'],
      q: ['El objetivo de cada semana del piloto y cómo va lo real frente a él.',
          'The weekly pilot target and how reality compares.'],
      c: ['El objetivo es editable: es una decisión, no una profecía.',
          'The target is editable — it’s a decision, not a prophecy.']
    },
    'pilot-observability.html': {
      t: ['📡 Obs. piloto · qué pasa de verdad', '📡 Pilot obs · what really happens'],
      q: ['Quién ha instalado, quién usa la app de verdad, el embudo y el feedback recibido.',
          'Who installed, who actually uses the app, the funnel and the feedback received.'],
      c: ['Instalar no es usar: aquí se ve la diferencia.', 'Installing isn’t using — here you see the gap.']
    },
    'waitlist.html': {
      t: ['📬 Waitlist · quién quiere entrar', '📬 Waitlist · who wants in'],
      q: ['Las personas que se apuntaron en la web. De aquí salen las invitadas al piloto.',
          'People who signed up on the website. Pilot invitations come from here.'],
      c: ['Son datos personales: solo tras el candado del hub, nunca a sitios públicos.',
          'Personal data: behind the hub gate only, never anywhere public.']
    },
    'backlog-dev.html': {
      t: ['🗂 Sprint Planning · el trabajo de desarrollo', '🗂 Sprint Planning · the dev work'],
      q: ['Todo lo que hay que construir — arreglos, mejoras, features y capacidades — agrupado por sprint.',
          'Everything to build — fixes, improvements, features, capabilities — grouped by sprint.'],
      c: ['Los bugs entran solos desde 🎫 con su prioridad. Lo que decides aquí: prioridad, sprint y sobre todo la release.',
          'Bugs arrive automatically from 🎫 with their priority. You decide: priority, sprint and above all the release.']
    },
    'release-plan.html': {
      t: ['🚢 Releases · qué lleva cada versión', '🚢 Releases · what ships in each version'],
      q: ['Cada versión con su contenido en tres carriles: 🐞 arreglos · 🔧 mejoras · 🚀 capacidades.',
          'Each version and its content in three lanes: 🐞 fixes · 🔧 improvements · 🚀 capabilities.'],
      c: ['Arriba está lo que aún no tiene release — eso espera tu decisión. Las notas de tienda ES/EN viven aquí: son la única fuente.',
          'Unassigned items sit on top — they await your call. ES/EN store notes live here as the single source.']
    },
    'compliance.html': {
      t: ['🛡 Compliance · protección de datos y financiación', '🛡 Compliance · data protection and funding'],
      q: ['Los documentos del DPD y la EIPD (RGPD) y los acuerdos de financiación pública.',
          'DPO and DPIA (GDPR) documents plus the public-funding agreements.'],
      c: ['Confidenciales: se sirven solo dentro del hub y no se reenvían.',
          'Confidential: served inside the hub only, never forwarded.']
    },
    'translations.html': {
      t: ['🌍 Traducciones · los 14 idiomas', '🌍 Translations · the 14 languages'],
      q: ['Qué textos de la app están traducidos y cuáles faltan.',
          'Which app strings are translated and which are missing.'],
      c: ['Toda cadena nueva nace en los 14 catálogos a la vez.',
          'Every new string is born in all 14 catalogues at once.']
    },
    'review.html': {
      t: ['🔎 Review · repaso de calidad', '🔎 Review · quality pass'],
      q: ['Revisión antes de publicar: que lo que sale esté a la altura.',
          'A pass before publishing: make sure what ships is up to standard.'],
      c: ['', '']
    },
    'prototypes.html': {
      t: ['🧩 Prototipos · diseño para mirar', '🧩 Prototypes · design to look at'],
      q: ['Pantallas de diseño para revisar sin tocar producción.',
          'Design screens to review without touching production.'],
      c: ['', '']
    },
    'access.html': {
      t: ['🔑 Access · quién puede entrar', '🔑 Access · who can get in'],
      q: ['La lista de correos que pasan la primera puerta del hub.',
          'The list of emails that pass the hub’s first gate.'],
      c: ['Esta página es informativa: la lista que manda vive en Cloudflare Access.',
          'This page is a snapshot: the live list is the Cloudflare Access policy.']
    },
    'mfa.html': {
      t: ['🔐 MFA · segundo factor', '🔐 MFA · second factor'],
      q: ['Quién tiene el segundo factor activado.', 'Who has the second factor switched on.'],
      c: ['El hub perdona a quien no lo tiene; StartUp Admin (contabilidad) no.',
          'The hub tolerates its absence; StartUp Admin (accounting) does not.']
    }
  };

  /* r14e: el idioma lo manda el conmutador 🌐 de la barra (ns_lang + evento
     ns-lang). Un solo idioma a la vista, como el resto del hub. */
  function en() { return (localStorage.getItem('ns_lang') || 'ES').toUpperCase() === 'EN'; }

  function cuerpo(h) {
    var i = en() ? 1 : 0;
    return '<b>' + h.t[i] + '</b><br>' + h.q[i] +
      (h.c[i] ? '<br><span style="color:#8A7F78">' + h.c[i] + '</span>' : '') +
      '<div style="margin-top:8px"><a href="/hub/user-guide.html" style="color:#C05621;font-weight:700">' +
      (en() ? '📖 Full ERP user guide →' : '📖 Guía completa del ERP →') + '</a></div>';
  }
  function etiqueta(ab) {
    return ab ? (en() ? '▾ hide' : '▾ ocultar')
              : (en() ? '▸ what is this page?' : '▸ ¿qué es esta página?');
  }

  function pinta() {
    var f = (location.pathname.split('/').pop() || '').toLowerCase();
    var h = H[f];
    if (!h) return;
    var ya = document.getElementById('ns-help');
    var abierto = localStorage.getItem('ns_help_open') === '1';
    if (ya) {                                   // repintado al cambiar idioma
      ya.querySelector('#ns-help-t').innerHTML = '📖 ' + h.t[en() ? 1 : 0];
      ya.querySelector('#ns-help-b').innerHTML = cuerpo(h);
      ya.querySelector('#ns-help-x').textContent = etiqueta(ya.querySelector('#ns-help-b').style.display !== 'none');
      return;
    }
    var d = document.createElement('div');
    d.id = 'ns-help';
    d.style.cssText = 'max-width:1080px;margin:14px auto 0;padding:0 20px;font-family:Poppins,system-ui,sans-serif';
    d.innerHTML =
      '<div style="background:#FBF6EF;border:1px solid #EFE3D7;border-radius:12px;padding:11px 15px">' +
      '<div id="ns-help-h" style="cursor:pointer;display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700">' +
      '<span id="ns-help-t">📖 ' + h.t[en() ? 1 : 0] + '</span>' +
      '<span id="ns-help-x" style="margin-left:auto;font-weight:400;color:#8A7F78;font-size:12px">' +
      etiqueta(abierto) + '</span></div>' +
      '<div id="ns-help-b" style="display:' + (abierto ? 'block' : 'none') +
      ';margin-top:9px;font-size:12.7px;line-height:1.62;max-width:720px">' + cuerpo(h) + '</div></div>';
    var nav = document.querySelector('.nsnb-wrap, #ns-hub-navbar');
    if (nav && nav.parentNode) nav.parentNode.insertBefore(d, nav.nextSibling);
    else document.body.insertBefore(d, document.body.firstChild);
    document.getElementById('ns-help-h').addEventListener('click', function () {
      var b = document.getElementById('ns-help-b');
      var ab = b.style.display === 'none';
      b.style.display = ab ? 'block' : 'none';
      localStorage.setItem('ns_help_open', ab ? '1' : '0');
      document.getElementById('ns-help-x').textContent = etiqueta(ab);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', pinta);
  else pinta();
  window.addEventListener('ns-lang', pinta);
})();
