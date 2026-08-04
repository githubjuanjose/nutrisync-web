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
    var W = 620, H = 170, pad = 28, padR = 44, i, max = +scale || 1;
    rows.forEach(function (r) { series.forEach(function (se) { max = Math.max(max, +r[se[0]] || 0); }); });
    var X = function (i) { return pad + (i / Math.max(1, rows.length - 1)) * (W - pad - padR); };
    var Y = function (v) { return H - ((+v || 0) / max) * (H - 16); };
    var cut = lastPast(rows);
    var s = '<svg viewBox="0 0 ' + W + ' ' + (H + 26) + '" style="width:100%;height:auto">';
    [0, 0.25, 0.5, 0.75, 1].forEach(function (f) {
      var y = H - f * (H - 16);
      s += '<line x1="' + pad + '" y1="' + y + '" x2="' + (W - padR) + '" y2="' + y + '" stroke="' + C.line + '" stroke-width="1"/>';
      s += '<text x="' + (pad - 5) + '" y="' + (y + 3) + '" font-size="9" fill="' + C.muted + '" text-anchor="end">' + Math.round(max * f) + '</text>';
    });
    /* r12-b7 (Juanjo): la línea sola no dice CUÁNTOS. Cada serie termina en un
       punto con su cifra, para leer de un vistazo iOS vs Android sin contar
       píxeles. Se apilan si coinciden en el mismo valor. */
    var used = [];
    series.forEach(function (se) {
      if (se[3] && cut < 0) return;                       // sin datos reales todavía
      var end = se[3] ? cut : rows.length - 1;
      s += '<path d="' + linePath(rows, se[0], X, Y, se[3] ? cut : null) + '" fill="none" stroke="' + se[1] +
           '" stroke-width="' + (se[2] ? 2 : 2.5) + '"' + (se[2] ? ' stroke-dasharray="5 4"' : '') + '/>';
      var v = +rows[end][se[0]] || 0, x = X(end), y = Y(v);
      while (used.some(function (u) { return Math.abs(u - y) < 11; })) y -= 11;
      used.push(y);
      s += '<circle cx="' + x + '" cy="' + Y(v) + '" r="3.5" fill="' + se[1] + '"/>';
      s += '<rect x="' + (x + 5) + '" y="' + (y - 8) + '" width="' + (String(v).length * 7 + 10) + '" height="15" rx="7.5" fill="' + se[1] + '" opacity="0.12"/>';
      s += '<text x="' + (x + 10) + '" y="' + (y + 3.5) + '" font-size="10.5" font-weight="700" fill="' + se[1] + '">' + v + '</text>';
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
  /** r12-b7: tarjetas por GRUPO DE TEST (founders / advisory / wave-1…) con las
   *  cifras que se miran para saber si una ola arrancó. */
  function cohortCards(list, L) {
    if (!list || !list.length) return '';
    return '<div style="display:flex;gap:8px;flex-wrap:wrap">' + list.map(function (c) {
      var chip = function (n, lbl, col) {
        return '<span style="display:inline-flex;align-items:center;gap:4px;background:#F8F3EC;border-radius:8px;padding:3px 8px;margin:2px 3px 0 0">' +
          '<b style="font-size:13px;color:' + (col || C.ink) + '">' + (n || 0) + '</b>' +
          '<span style="font-size:10.5px;color:' + C.muted + '">' + lbl + '</span></span>';
      };
      return '<div style="flex:1;min-width:230px;border:1px solid ' + C.line + ';border-radius:12px;padding:10px 12px">' +
        '<b style="font-size:13px">' + c.cohort + '</b>' +
        '<div style="margin-top:4px">' +
        chip(c.invited, L.lInv) + chip(c.assigned, L.lAsg, C.coral2) + chip(c.installed, L.lIns, C.coral) +
        chip(c.ios, 'iOS', C.coral) + chip(c.android, 'Android', C.good) + chip(c.active7, L.lAct, C.good) +
        '</div></div>';
    }).join('') + '</div>';
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
                legend: legend, kpi: kpi, cohortCards: cohortCards,
                platformChart: platformChart, statesChart: statesChart, activeChart: activeChart };
})(window);
