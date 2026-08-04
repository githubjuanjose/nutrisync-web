/* NutriSync · r12-b6 — gráficas del piloto (SVG puro, sin librerías ni CDNs).
   Compartidas por hub/pilot-planning.html y hub/pilot-observability.html: una
   sola fuente, para que las dos pestañas no se separen con el tiempo.
   Todo son funciones PURAS → cubiertas por tools/web-tests.mjs. */
(function (g) {
  var C = { ink: '#231F20', muted: '#8A7F78', line: '#EFE3D7', coral: '#E8472A',
            coral2: '#FF7600', plan: '#B9AFA6', good: '#0F9B57' };

  /** índice del último periodo con datos reales (-1 si aún no hay ninguno) */
  function lastPast(rows) {
    var k = -1;
    for (var i = 0; i < rows.length; i++) if (rows[i].is_past) k = i;
    return k;
  }
  /** camino de una serie; `upTo` la corta en el presente (nada de futuro inventado) */
  function linePath(rows, key, X, Y, upTo) {
    var end = (upTo == null ? rows.length - 1 : Math.min(upTo, rows.length - 1)), d = '', i;
    for (i = 0; i <= end; i++) d += (i ? ' L ' : 'M ') + X(i) + ' ' + Y(rows[i][key]);
    return d;
  }
  /** series = [[clave, color, discontinua, soloPasado]] · scale fija el techo del eje Y */
  function lineChart(rows, series, labelKey, every, scale) {
    var W = 620, H = 170, pad = 28, i, max = +scale || 1;
    rows.forEach(function (r) { series.forEach(function (se) { max = Math.max(max, +r[se[0]] || 0); }); });
    var X = function (i) { return pad + (i / Math.max(1, rows.length - 1)) * (W - pad * 2); };
    var Y = function (v) { return H - ((+v || 0) / max) * (H - 16); };
    var cut = lastPast(rows);
    var s = '<svg viewBox="0 0 ' + W + ' ' + (H + 26) + '" style="width:100%;height:auto">';
    [0, 0.25, 0.5, 0.75, 1].forEach(function (f) {
      var y = H - f * (H - 16);
      s += '<line x1="' + pad + '" y1="' + y + '" x2="' + (W - pad) + '" y2="' + y + '" stroke="' + C.line + '" stroke-width="1"/>';
      s += '<text x="' + (pad - 5) + '" y="' + (y + 3) + '" font-size="9" fill="' + C.muted + '" text-anchor="end">' + Math.round(max * f) + '</text>';
    });
    series.forEach(function (se) {
      if (se[3] && cut < 0) return;                       // sin datos reales todavía
      s += '<path d="' + linePath(rows, se[0], X, Y, se[3] ? cut : null) + '" fill="none" stroke="' + se[1] +
           '" stroke-width="' + (se[2] ? 2 : 2.5) + '"' + (se[2] ? ' stroke-dasharray="5 4"' : '') + '/>';
    });
    var step = every || Math.ceil(rows.length / 6);
    for (i = 0; i < rows.length; i += step) {
      s += '<text x="' + X(i) + '" y="' + (H + 16) + '" font-size="9" fill="' + C.muted + '" text-anchor="middle">' + rows[i][labelKey] + '</text>';
    }
    return s + '</svg>';
  }
  function legend(items) {
    return '<div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:8px;font-size:11.5px;color:' + C.muted + '">' +
      items.map(function (it) {
        return '<span style="display:inline-flex;align-items:center;gap:6px">' +
          '<span style="width:14px;height:3px;border-radius:2px;background:' + it[1] + ';' + (it[2] ? 'opacity:.6;' : '') + '"></span>' + it[0] + '</span>';
      }).join('') + '</div>';
  }
  function kpi(label, value, sub) {
    return '<div class="kpi"><div class="l">' + label + '</div><div class="v">' + value + '</div>' +
           '<div class="l" style="text-transform:none;letter-spacing:0;margin-top:2px">' + (sub || '') + '</div></div>';
  }
  /* gráficas concretas — mismas claves que devuelve admin_pilot_weekly() */
  function platformChart(weeks, scale) {
    return lineChart(weeks, [['testers_plan', C.plan, 1, 0], ['ios', C.coral, 0, 1], ['android', C.good, 0, 1]], 'label', 2, scale);
  }
  function statesChart(weeks, scale) {
    return lineChart(weeks, [['invited', C.muted, 0, 1], ['assigned', C.coral2, 0, 1],
                             ['installed', C.coral, 0, 1], ['pending', C.plan, 1, 1]], 'label', 2, scale);
  }
  function activeChart(weeks, scale) {
    return lineChart(weeks, [['active_plan', C.plan, 1, 0], ['active', C.coral, 0, 1]], 'label', 2, scale);
  }
  g.NSPilot = { C: C, lastPast: lastPast, linePath: linePath, lineChart: lineChart,
                legend: legend, kpi: kpi,
                platformChart: platformChart, statesChart: statesChart, activeChart: activeChart };
})(window);
