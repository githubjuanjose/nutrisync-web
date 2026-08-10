/* NutriSync · entrega.js — CÓMO se entrega algo, en UN solo sitio (r17, 11-ago)
 *
 * POR QUÉ EXISTE
 * Hasta hoy había DOS verdades sobre lo mismo:
 *   · 🚢 Releases lo DEDUCÍA del número de versión (regla Juanjo, 10-ago).
 *   · 🗂 Sprint Planning lo PREGUNTABA con un desplegable manual (r16-F18,
 *     escrito el 8-ago, dos días antes de que existiera la regla).
 * Dos fuentes para el mismo dato siempre acaban discrepando: un item podía
 * decir «OTA» con la release 0.22.0 (que es nativa) y nadie se enteraba. Es la
 * lección r12-b10 otra vez — si el dato ya existe, se lee, no se copia.
 *
 * Y el desplegable no sabía decir WEB, que es donde vive la mitad del trabajo.
 *
 * LA REGLA, ENTERA
 *   0.N.x con x>0 → 🔄 OTA      · JS puro, mismo día, sin tiendas
 *   0.N.0         → 📦 nativa   · deps/permisos, build + revisión de Apple
 *   WEB           → 🌐 continua · el carril del deploy web, nunca «se publica»
 *   GA            → 🏁 GA       · el hito, no un vehículo
 *   —             → sin release · aún no comprometido a nada (no es un «por ver»:
 *                                 es que todavía no se ha decidido cuándo entra)
 */
(function () {
  function como(v) {
    var s = String(v == null ? '' : v).trim();
    if (s === '' || s === '—' || s === '-')
      return { ico: '·', txt: 'sin release', cls: 'd-none', nota: 'aún no comprometido a una entrega' };
    if (s === 'WEB') return { ico: '🌐', txt: 'web · continua', cls: 'd-web', nota: 'sale con el deploy web, sin tiendas' };
    if (s === 'GA')  return { ico: '🏁', txt: 'GA', cls: 'd-ga', nota: 'lanzamiento general' };
    var m = s.match(/^(\d+)\.(\d+)\.(\d+)$/);
    if (!m) return { ico: '?', txt: s, cls: 'd-raro', nota: 'número de release no reconocido' };
    return +m[3] > 0
      ? { ico: '🔄', txt: 'OTA', cls: 'd-ota', nota: 'parche JS: llega el mismo día, sin tiendas' }
      : { ico: '📦', txt: 'nativa', cls: 'd-nat', nota: 'build nativo: tiendas y revisión de Apple' };
  }
  /* Las opciones del desplegable de release, AGRUPADAS POR VEHÍCULO.
   *
   * Petición Juanjo (11-ago): «OTA y Nativa se han quedado fijas, debería poder
   * seleccionarlas». Cierto — pero un selector de vehículo APARTE del de release
   * es justo la segunda verdad que acabamos de retirar (podría decir OTA con la
   * 0.22.0). Con un solo desplegable agrupado se elige «📦 Nativa → 0.22.0» y
   * con eso queda dicho todo: el vehículo se ve al elegir y no puede mentir.
   *
   * `rels` = [{version, estado}]. Las publicadas salen deshabilitadas (no se
   * mete trabajo nuevo en algo que ya está en las tiendas) salvo que sea la que
   * el item ya tiene — si no, la fila mentiría sobre dónde está.
   */
  function opciones(rels, actual) {
    var act = (actual == null || actual === '') ? '—' : String(actual);
    var lista = (rels || []).slice();
    if (act !== '—' && !lista.some(function (r) { return r.version === act; }))
      lista.push({ version: act, estado: 'planificada' });   // huérfana: se ve, no se esconde

    var GRUPOS = [
      ['d-web', '🌐 Web · sale con el deploy, sin tiendas'],
      ['d-ota', '🔄 OTA · parche JS, el mismo día'],
      ['d-nat', '📦 Nativa · build y revisión de Apple'],
      ['d-ga',  '🏁 GA'],
      ['d-raro','?  sin clasificar']
    ];
    var html = '<option value="—"' + (act === '—' ? ' selected' : '') + '>— sin decidir</option>';
    GRUPOS.forEach(function (g) {
      var dentro = lista.filter(function (r) { return como(r.version).cls === g[0]; });
      if (!dentro.length) return;
      html += '<optgroup label="' + g[1] + '">';
      dentro.forEach(function (r) {
        var pub = r.estado === 'en_tiendas' || r.estado === 'ga';
        var sel = r.version === act;
        html += '<option value="' + r.version + '"' + (sel ? ' selected' : '')
             + (pub && !sel ? ' disabled' : '') + '>' + r.version
             + (r.nombre ? ' · ' + r.nombre : '') + (pub ? ' · publicada' : '') + '</option>';
      });
      html += '</optgroup>';
    });
    return html;
  }

  window.NSEntrega = { como: como, opciones: opciones };
})();
