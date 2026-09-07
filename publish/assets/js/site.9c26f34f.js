/* NutriSync Web V2 · navegación (vanilla, sin dependencias) */
(function () {
  'use strict';
  var doc = document;
  // ── hoja del menú móvil ──
  var sheet = doc.getElementById('ns-sheet');
  function toggleSheet(open) {
    if (!sheet) return;
    var on = typeof open === 'boolean' ? open : sheet.hidden;
    sheet.hidden = !on;
    doc.body.classList.toggle('ns-sheet-open', on);
    doc.querySelectorAll('[data-sheet-toggle][aria-expanded]').forEach(function (b) { b.setAttribute('aria-expanded', String(on)); });
  }
  doc.querySelectorAll('[data-sheet-toggle]').forEach(function (b) { b.addEventListener('click', function () { toggleSheet(); }); });
  doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sheet && !sheet.hidden) toggleSheet(false); });
  doc.addEventListener('click', function (e) { if (sheet && !sheet.hidden && !sheet.contains(e.target) && !e.target.closest('[data-sheet-toggle]')) toggleSheet(false); });
  if (sheet) sheet.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { toggleSheet(false); }); });

  // ── enlace activo (URL limpia, sin .html — lección r16c) ──
  var path = location.pathname.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';
  var section = path === '/' ? (location.hash === '#how-it-works' ? 'how' : 'home') : path.indexOf('/community') === 0 ? 'community' : path.indexOf('/our-story') === 0 ? 'story' : '';
  doc.querySelectorAll('[data-nav]').forEach(function (a) {
    if (a.getAttribute('data-nav') === section) a.setAttribute('aria-current', 'page');
  });

  // ── «How it Works» = Home + scroll a «The App that knows your cycle» (prompt §4 nº 4) ──
  // Dos árboles por URL (UST-07 G2) ⇒ un id puede existir dos veces: se resuelve el VISIBLE (offsetParent),
  // nunca el primero (que en móvil es el de escritorio, display:none).
  function visibleById(id) {
    var els = doc.querySelectorAll('[id="' + id + '"]');
    for (var i = 0; i < els.length; i++) { if (els[i].offsetParent !== null || getComputedStyle(els[i]).position === 'fixed') return els[i]; }
    return els[0] || null;
  }
  function navOffset() {
    var nav = doc.querySelector('.ns-nav:not([hidden])');
    if (!nav || getComputedStyle(nav).display === 'none') return 0;
    // Ronda 5 (6-sep): la barra de escritorio bajó de 13 a 5,2 rem, así que ya no hay «banda del logo»
    // que descontar — se resta el alto ENTERO y el ancla aterriza justo debajo. El valor ABSOLUTO no
    // cambia (antes 13 rem × 0,4 = 5,2 rem; ahora 5,2 rem × 1), a cualquier anchura de ventana.
    return nav.getBoundingClientRect().height;
  }
  // Baja a un id resolviendo el árbol VISIBLE (lección 5-sep: en móvil el primer #phases del documento es el de escritorio,
  // display:none, y el salto nativo del navegador no hace nada — «los enlaces llevan a la portada»).
  function goTo(id, smooth) {
    var t = visibleById(id); if (!t) return false;
    var y = t.getBoundingClientRect().top + window.scrollY - navOffset();
    window.scrollTo({ top: Math.max(0, y), behavior: (smooth === false || matchMedia('(prefers-reduced-motion: reduce)').matches) ? 'auto' : 'smooth' });
    return true;
  }
  function scrollToHow() { return goTo('how-it-works'); }
  // Todo enlace a un ancla de ESTA página (#id o /#id estando en la Home) se resuelve aquí, nunca con el salto nativo.
  doc.querySelectorAll('a[href^="#"], a[href^="/#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var href = a.getAttribute('href'); var id = href.replace(/^\/?#/, '');
      if (!id || (href.charAt(0) === '/' && path !== '/')) return;          // /#id desde otra página: navegación normal
      if (goTo(id)) { e.preventDefault(); history.replaceState(null, '', '#' + id); }
    });
  });
  function landOnHash() { if (location.hash.length > 1) setTimeout(function () { goTo(location.hash.slice(1), false); }, 60); }
  landOnHash();

  // ── Tono de la barra (7-sep 19:2x, Juanjo): tinta sobre secciones claras, blanco sobre fotos y color ──
  // La barra no lleva fondo (decisión de la mañana). Se mira qué hay justo debajo de ella en el centro de la pantalla,
  // se sube hasta la sección (o el primer antepasado con fondo) y se decide por luminancia. Fotos, vídeos y fondos de
  // imagen cuentan como oscuros (el blanco con sombra ya funcionaba ahí). Corre en scroll/resize por rAF: barato.
  function luminancia(rgb) {
    var m = rgb && rgb.match(/[\d.]+/g); if (!m || m.length < 3) return null;
    if (m.length > 3 && parseFloat(m[3]) === 0) return null;                      // transparente: seguir subiendo
    return 0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2];
  }
  function tonoBajoLaBarra(nav) {
    var r = nav.getBoundingClientRect();
    var y = Math.min(r.bottom - 2, innerHeight - 1), x = innerWidth / 2;
    var els = doc.elementsFromPoint ? doc.elementsFromPoint(x, y) : [];
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.closest('.ns-nav, .ns-sheet')) continue;                              // lo que está bajo la barra, no la barra
      var sec = el.closest('[class*="sec-"]') || el;
      var cur = el;
      while (cur && cur !== doc.documentElement) {
        var cs = getComputedStyle(cur);
        if (cur.tagName === 'IMG' || cur.tagName === 'VIDEO' || cs.backgroundImage !== 'none') return 'dark';
        var L = luminancia(cs.backgroundColor);
        if (L !== null) return L > 180 ? 'light' : 'dark';
        if (cur === sec) break;
        cur = cur.parentElement;
      }
      var Ls = luminancia(getComputedStyle(sec).backgroundColor);
      return Ls !== null && Ls > 180 ? 'light' : 'dark';
    }
    return 'dark';
  }
  var navTonoPendiente = false;
  function pintaTono() {
    navTonoPendiente = false;
    var nav = doc.querySelector('.ns-nav:not([hidden])');
    if (!nav || getComputedStyle(nav).display === 'none') return;
    doc.documentElement.style.setProperty('--ns-nav-h', nav.getBoundingClientRect().height + 'px');   // la hoja del menú cuelga de la barra real (safe area)
    var claro = !doc.body.classList.contains('ns-sheet-open') && tonoBajoLaBarra(nav) === 'light';
    doc.documentElement.classList.toggle('ns-nav-ink', claro);
  }
  function pideTono() { if (!navTonoPendiente) { navTonoPendiente = true; requestAnimationFrame(pintaTono); } }
  addEventListener('scroll', pideTono, { passive: true });
  addEventListener('resize', pideTono);
  addEventListener('load', pideTono);
  doc.addEventListener('click', function (e) { if (e.target.closest('[data-sheet-toggle]')) setTimeout(pideTono, 0); });
  pideTono();
  window.addEventListener('hashchange', function () { goTo(location.hash.slice(1)); });

  // (7-sep: el fondo al bajar se retiró — la barra es transparente siempre, decisión de Juanjo y Lucía)


})();

/* NutriSync Web V2 · idioma (UST-07 G5): EN inline (el del Figma) + data-es inyectado por build.py.
   Cambia innerHTML desde atributos, JAMÁS display (lección r16-F17). Sin JS se ve el inglés. */
(function () {
  'use strict';
  var KEY = 'ns_lang', LANGS = ['en', 'es'];
  function detect() {
    // ?lang=es|en manda (enlaces compartidos y capturas de verificación) y se recuerda
    try { var q = new URLSearchParams(location.search).get('lang'); if (q && LANGS.indexOf(q) >= 0) return q; } catch (e) {}
    try { var s = localStorage.getItem(KEY); if (s && LANGS.indexOf(s) >= 0) return s; } catch (e) {}
    var nav = (navigator.language || 'en').slice(0, 2).toLowerCase();
    return LANGS.indexOf(nav) >= 0 ? nav : 'en';
  }
  function apply(lang) {
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i]').forEach(function (el) {
      if (!el.hasAttribute('data-en')) el.setAttribute('data-en', el.innerHTML);
      var v = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-' + lang);
      if (v != null && v !== '') el.innerHTML = v;
    });
    document.querySelectorAll('[data-i-ph]').forEach(function (el) {
      if (!el.hasAttribute('data-en-ph')) el.setAttribute('data-en-ph', el.getAttribute('placeholder') || '');
      var v = lang === 'en' ? el.getAttribute('data-en-ph') : el.getAttribute('data-' + lang + '-ph');
      if (v != null && v !== '') el.setAttribute('placeholder', v);
    });
    document.querySelectorAll('[data-lang-switch]').forEach(function (b) { b.textContent = lang === 'en' ? 'ES' : 'EN'; b.setAttribute('aria-label', lang === 'en' ? 'Cambiar a español' : 'Switch to English'); });
    try { localStorage.setItem(KEY, lang); } catch (e) {}
    document.dispatchEvent(new CustomEvent('ns-lang', { detail: lang }));
  }
  var cur = detect();
  if (cur !== 'en') apply(cur); else apply('en');
  document.querySelectorAll('[data-lang-switch]').forEach(function (b) {
    b.addEventListener('click', function () { cur = cur === 'en' ? 'es' : 'en'; apply(cur); });
  });
  window.nsLang = function () { return cur; };
})();

/* NutriSync Web V2 · formularios: waitlist (misma tabla que la web viva) y Community leads (Edge community-lead). */
(function () {
  'use strict';
  var SB = 'https://nebkqncvapelrarruyqb.supabase.co';
  var ANON = 'sb_publishable_GYj7DKlcWZ2cxdwv-GkyHQ_WBbQWHau';   // pública por diseño (RLS manda)
  var T = {
    en: { ok: '✓ You’re in! Check your inbox.', dup: '✓ You’re already on the list.', bad: 'Please enter a valid email.', consent: 'Please tick the consent box first.', err: 'Something went wrong. Please try again.', sending: 'Sending…', file: 'CV must be a PDF/DOC under 5 MB.' },
    es: { ok: '✓ ¡Dentro! Mira tu correo.', dup: '✓ Ya estás en la lista.', bad: 'Escribe un email válido.', consent: 'Marca primero la casilla de consentimiento.', err: 'Algo ha fallado. Inténtalo otra vez.', sending: 'Enviando…', file: 'El CV debe ser PDF/DOC de menos de 5 MB.' }
  };
  function t(k) { var l = (window.nsLang && window.nsLang()) || 'en'; return (T[l] || T.en)[k]; }
  function valid(e) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e); }
  function msg(form, text, isErr) {
    var m = form.parentElement.querySelector('.ns-msg') || form.querySelector('.ns-msg');
    if (!m) return;
    m.hidden = false; m.textContent = text; m.classList.toggle('is-error', !!isErr);
  }

  // ── waitlist ──
  document.querySelectorAll('form.ns-wait').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = (form.email.value || '').trim().toLowerCase();
      var consent = form.parentElement.querySelector('input[name="consent"]') || form.querySelector('input[name="consent"]');
      if (!valid(email)) { msg(form, t('bad'), true); form.email.focus(); return; }
      if (consent && !consent.checked) { msg(form, t('consent'), true); consent.focus(); return; }
      form.classList.add('is-busy'); msg(form, t('sending'));
      fetch(SB + '/rest/v1/waitlist', { method: 'POST', headers: { apikey: ANON, Authorization: 'Bearer ' + ANON, 'Content-Type': 'application/json', Prefer: 'return=minimal' },
        body: JSON.stringify({ email: email, source: 'web2' }) })
        .then(function (r) {
          form.classList.remove('is-busy');
          if (r.status === 201) { msg(form, t('ok')); form.email.value = ''; var b = form.querySelector('button p, button'); if (b) b.textContent = '✓'; }
          else if (r.status === 409) { msg(form, t('dup')); }
          else { msg(form, t('err'), true); }
        }).catch(function () { form.classList.remove('is-busy'); msg(form, t('err'), true); });
    });
  });

  // ── nada falla en silencio (r26-g) ──
  // Si un campo obligatorio no pasa la validación del navegador, el evento `submit` NUNCA se dispara:
  // nuestro código no se entera y la persona ve un botón que no hace nada (le pasó a Pilar con el CV).
  // Interceptamos el clic del botón: pedimos al navegador que enseñe el motivo Y lo escribimos en la
  // línea de mensajes del formulario, que siempre se ve.
  document.querySelectorAll('form.ns-wait, form.ns-lead').forEach(function (form) {
    var btn = form.querySelector('button[type="submit"], button:not([type])');
    if (!btn) return;
    btn.addEventListener('click', function () {
      if (form.checkValidity()) return;
      var malo = null;
      Array.prototype.some.call(form.elements, function (el) { if (el.willValidate && !el.checkValidity()) { malo = el; return true; } return false; });
      if (malo) {
        msg(form, malo.validationMessage || t('err'), true);
        if (typeof form.reportValidity === 'function') form.reportValidity();
        try { malo.focus({ preventScroll: false }); } catch (_) { malo.focus(); }
      }
    });
  });

  // ── Community leads ──
  document.querySelectorAll('form.ns-lead').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = (form.email && form.email.value || '').trim().toLowerCase();
      if (!valid(email)) { msg(form, t('bad'), true); form.email && form.email.focus(); return; }
      var cv = form.querySelector('input[type="file"]');
      if (cv && cv.files && cv.files[0]) {
        var f = cv.files[0];
        if (f.size > 5 * 1024 * 1024 || !/\.(pdf|docx?)$/i.test(f.name)) { msg(form, t('file'), true); return; }
      }
      var fd = new FormData(form);
      fd.set('lang', (window.nsLang && window.nsLang()) || 'en');
      fd.set('source', 'web2');
      form.classList.add('is-busy'); msg(form, t('sending'));
      fetch(form.action, { method: 'POST', headers: { apikey: ANON, Authorization: 'Bearer ' + ANON, 'X-NS-Fetch': '1' }, body: fd })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          form.classList.remove('is-busy');
          if (res.ok) { var next = form.querySelector('input[name="next"]'); location.href = (next && next.value) || '/'; }
          else { msg(form, (res.j && res.j.motivo) || t('err'), true); }
        }).catch(function () { form.classList.remove('is-busy'); msg(form, t('err'), true); });
    });
  });

  // ── pestañas Individual | Business (/community/join/): cada <form class="ns-lead ns-tab-panel"> es un panel
  //    (data-lead community = Individual · workplace = Business); las pestañas viven dentro de cada panel.
  var MAP = { individual: 'community', business: 'workplace' };
  function showTab(scope, which) {
    scope.querySelectorAll('.ns-tab-panel').forEach(function (p) { p.hidden = p.getAttribute('data-lead') !== MAP[which]; });
  }
  document.querySelectorAll('[data-tab]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var scope = btn.closest('.vp-d, .vp-m') || document;
      showTab(scope, btn.getAttribute('data-tab'));
      var first = scope.querySelector('.ns-tab-panel:not([hidden]) input:not([type=hidden])'); if (first) first.focus();
    });
  });
  document.querySelectorAll('.vp-d, .vp-m').forEach(function (scope) { if (scope.querySelector('.ns-tab-panel')) showTab(scope, 'individual'); });

  // ── zona de arrastre del CV ──
  document.querySelectorAll('.ns-upload').forEach(function (zone) {
    var input = zone.querySelector('input[type="file"]'); if (!input) return;
    ['dragenter', 'dragover'].forEach(function (ev) { zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add('is-over'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove('is-over'); }); });
    zone.addEventListener('drop', function (e) { if (e.dataTransfer && e.dataTransfer.files.length) { input.files = e.dataTransfer.files; input.dispatchEvent(new Event('change')); } });
    input.addEventListener('change', function () { var n = zone.querySelector('[data-file-name]'); if (n && input.files[0]) n.textContent = input.files[0].name; });
  });
})();

/* NutriSync Web V2 · PWA (UST-07 G6): service worker + barra «Añadir a inicio» (solo móvil, desde la 2ª visita, descartable). */
(function () {
  'use strict';
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', function () { navigator.serviceWorker.register('/sw.js').catch(function () {}); });
  }
  var bar = document.getElementById('ns-install'); if (!bar) return;
  var isMobile = matchMedia('(max-width: 767px)').matches;
  var standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  var visits = 0, dismissed = false;
  try { visits = (+localStorage.getItem('ns_visits') || 0) + 1; localStorage.setItem('ns_visits', String(visits)); dismissed = localStorage.getItem('ns_install_x') === '1'; } catch (e) {}
  if (!isMobile || standalone || dismissed || visits < 2) return;
  var deferred = null, isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent) && !window.MSStream;
  function show() { bar.classList.add('is-on'); }
  window.addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); deferred = e; show(); });
  if (isIOS) { bar.classList.add('is-ios'); show(); }
  bar.querySelector('[data-install]').addEventListener('click', function () {
    if (deferred) { deferred.prompt(); deferred.userChoice.then(function () { bar.classList.remove('is-on'); }); }
    else { bar.classList.add('is-hint'); }
  });
  bar.querySelector('[data-install-x]').addEventListener('click', function () { bar.classList.remove('is-on'); try { localStorage.setItem('ns_install_x', '1'); } catch (e) {} });
})();

/* NutriSync Web V2 · «Muy pronto» (Juanjo 5-sep): todo enlace [data-soon] (Descargar · Get App · I want it! · tiendas del pie)
   abre el aviso con la previsualización web; sin JS el enlace lleva directo a m.nutrisynccollective.com. */
(function () {
  'use strict';
  var box = document.getElementById('ns-soon'); if (!box) return;
  var last = null;
  function open(e) { e.preventDefault(); last = e.currentTarget; box.hidden = false; document.body.classList.add('ns-sheet-open'); var b = box.querySelector('.ns-soon-go'); if (b) b.focus(); }
  function close() { box.hidden = true; document.body.classList.remove('ns-sheet-open'); if (last && last.focus) last.focus(); }
  document.querySelectorAll('[data-soon]').forEach(function (a) { a.addEventListener('click', open); });
  // Descargar / Get App / I want it! (Juanjo 5-sep): directo al campo de la lista de espera con el foco puesto
  function joinVisible() { var v = null; document.querySelectorAll('#join').forEach(function (el) { if (el.offsetParent !== null) v = el; }); return v; }
  function goJoin(e) {
    var vis = joinVisible(); if (!vis) return;            // otra página: el enlace /#join navega y al cargar se enfoca (abajo)
    e.preventDefault(); close();
    document.body.classList.remove('ns-sheet-open'); var sh = document.getElementById('ns-sheet'); if (sh && !sh.hidden) { sh.hidden = true; document.querySelectorAll('[data-sheet-toggle]').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); }); }
    vis.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    var i = vis.querySelector('input[type=email]'); if (i) setTimeout(function () { i.focus({ preventScroll: true }); }, 600);
  }
  document.querySelectorAll('[data-join]').forEach(function (a) { a.addEventListener('click', goJoin); });
  if (location.hash === '#join') { window.addEventListener('load', function () { var vis = joinVisible(); var i = vis && vis.querySelector('input[type=email]'); if (i) setTimeout(function () { i.focus({ preventScroll: true }); }, 400); }); }
  box.querySelectorAll('[data-soon-close]').forEach(function (b) { b.addEventListener('click', close); });
  // «Únete a la lista de espera»: en la Home baja al formulario (#join) y enfoca el email; en otra página navega a /#join
  var join = box.querySelector('[data-soon-join]');
  if (join) join.addEventListener('click', function (e) { if (joinVisible()) goJoin(e); else close(); });
  box.addEventListener('click', function (e) { if (e.target === box) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) close(); });
})();

/* NutriSync Web V2 · el montaje de Our Story: bucle silencioso + botón de sonido (ronda 5, Lucía).
   Un vídeo con sonido NO puede arrancar solo en ningún navegador moderno; con `muted` sí. Así que
   arranca callado y quien quiera oírlo pulsa el botón. Si el navegador se niega igualmente a
   reproducir (ahorro de batería, «reducir movimiento»), se queda el póster, que es la misma imagen
   que había antes: la banda nunca se ve rota.

   El fichero se engancha DESPUÉS del load de la página (el HTML trae data-src, no src). Dos razones:
   los 2,4 MB no retrasan la carga de Our Story, y la auditoría de textos —Chrome headless con reloj
   virtual, que no avanza mientras hay media cargando— deja de colgarse (r26-g, la noche del deploy). */
(function () {
  'use strict';
  var T = {
    en: { on: 'Turn sound on', off: 'Turn sound off' },
    es: { on: 'Activar el sonido', off: 'Quitar el sonido' }
  };
  function t(k) { var l = (window.nsLang && window.nsLang()) || 'en'; return (T[l] || T.en)[k]; }

  var enAuditoria = /[?&]audit=1\b/.test(location.search);
  var quieto = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('[data-ns-sound]').forEach(function (btn) {
    var sec = btn.closest('.sec') || document;
    var v = sec.querySelector('video');
    if (!v) { btn.hidden = true; return; }

    function pinta() {
      var suena = !v.muted;
      btn.setAttribute('aria-pressed', suena ? 'true' : 'false');
      var etiqueta = t(suena ? 'off' : 'on');
      btn.setAttribute('aria-label', etiqueta); btn.setAttribute('title', etiqueta);
    }

    function arranca() {
      var src = v.getAttribute('data-src');
      if (!src || v.src) return;
      v.src = src;
      var p = v.play();
      if (p && p.catch) p.catch(function () { /* el navegador dijo que no: se queda el póster */ });
    }

    btn.addEventListener('click', function () {
      arranca();                       // por si alguien pulsa antes de que el vídeo esté enganchado
      v.muted = !v.muted;
      if (!v.muted && v.paused) { var p = v.play(); if (p && p.catch) p.catch(function () { v.muted = true; pinta(); }); }
      pinta();
    });
    window.addEventListener('ns-lang', pinta);
    pinta();

    // En la auditoría no se pide el fichero; con «reducir movimiento» tampoco: se ve el póster y ya.
    if (enAuditoria) { btn.hidden = true; return; }
    if (quieto) return;
    if (document.readyState === 'complete') arranca();
    else window.addEventListener('load', arranca);
  });
})();

/* NutriSync Web V2 · «nada de datos en HTML» (regla de oro): año del ©, recuento vivo de la waitlist, asteriscos. */
(function () {
  'use strict';
  var SB = 'https://nebkqncvapelrarruyqb.supabase.co';
  var ANON = 'sb_publishable_GYj7DKlcWZ2cxdwv-GkyHQ_WBbQWHau';
  // © año
  var y = String(new Date().getFullYear());
  document.querySelectorAll('[data-year]').forEach(function (el) {
    var fix = function () { el.innerHTML = el.innerHTML.replace(/©\s*\d{4}/, '© ' + y); };
    fix(); document.addEventListener('ns-lang', fix);
  });
  // «150+ en la lista de espera»: recuento REAL redondeado a la decena por abajo (respaldo: el texto del diseño).
  // 6-sep: redondeaba a la CENTENA y con 158 personas de verdad pintaba «100+» — el dato automático estaba
  // quedándose corto en 58 personas, y Pilar pidió «150+» precisamente porque el que se veía mentía a la baja.
  // A la decena dice la verdad hoy (150+) y sigue diciéndola sola cuando la lista crezca.
  var wl = document.querySelectorAll('[data-count="waitlist"]');
  if (wl.length) {
    fetch(SB + '/rest/v1/rpc/waitlist_count', { method: 'POST', headers: { apikey: ANON, Authorization: 'Bearer ' + ANON, 'Content-Type': 'application/json' }, body: '{}' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (n) {
        n = typeof n === 'number' ? n : (n && (n.count || n.n));
        if (!n || n < 20) return;          // por debajo de 20 no se presume de comunidad: se deja el texto del diseño
        var txt = Math.floor(n / 10) * 10 + '+';
        wl.forEach(function (el) { var f = function () { el.innerHTML = el.innerHTML.replace(/\d+\+/, txt); }; f(); document.addEventListener('ns-lang', f); });
      }).catch(function () {});
  }
  // (*) en precios y reclamos → barra de aviso (UST-07 G11, decisión Juanjo)
  document.querySelectorAll('[data-ast]').forEach(function (el) {
    if (el.querySelector('.ns-ast')) return;
    var a = document.createElement('a'); a.className = 'ns-ast'; a.href = '#ns-disclaimer'; a.textContent = '*'; a.setAttribute('aria-label', 'Illustrative only — see notice');
    el.appendChild(a);
  });
})();
