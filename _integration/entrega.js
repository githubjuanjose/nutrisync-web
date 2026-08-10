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
  window.NSEntrega = { como: como };
})();
