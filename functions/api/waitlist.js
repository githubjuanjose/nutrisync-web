/* NutriSync · Pages Function POST /api/waitlist (UST-19 entrega A, 26-sep) — LA puerta pública del alta.
   Es el «API gateway» de la lista de espera: el formulario (web2 raíz, /v1/, m.) habla SOLO con esta ruta,
   en nuestro dominio, detrás del WAF y de la regla de rate limiting de Cloudflare (10/10 s por IP, D6).
   Aquí no hay lógica de negocio: se reenvía el alta a la Edge `waitlist-join` con DOS cabeceras que
   solo esta Function puede poner —x-ns-gateway (secreto compartido, variable NS_GATEWAY del proyecto
   Pages) y x-ns-ip (cf-connecting-ip, la IP real que Cloudflare ya conoce)— y se traduce la respuesta:
     · fetch con JS (cabecera X-NS-Fetch) → el JSON de la Edge tal cual, con su código HTTP;
     · POST de un <form> sin JS → 303 a la Home con ?waitlist=<resultado>#ns-live-waitlist.
   La anon key deja de vivir en el JS de la web (D2). Sin NS_GATEWAY configurada, la puerta responde 503
   y lo dice: nunca un silencio (r12-b9). publish/_routes.json incluye /api/* para que esta ruta exista.
   Nunca guarda nada ni lee la IP en claro más allá de reenviarla: el hash lo hace la Edge. */
const EDGE = 'https://nebkqncvapelrarruyqb.supabase.co/functions/v1/waitlist-join';
const ANON = 'sb_publishable_GYj7DKlcWZ2cxdwv-GkyHQ_WBbQWHau';   // pública por diseño: el gateway de Supabase la exige (r12-b7)

export function traduce(resultadoJson, esFetch, origen) {
  // PURA: decide qué le llega a la persona a partir del JSON de la Edge
  const motivo = (resultadoJson && resultadoJson.motivo) || (resultadoJson && resultadoJson.ok ? 'ok' : 'err');
  if (esFetch) return { tipo: 'json' };
  const q = resultadoJson && resultadoJson.ok ? 'ok' : encodeURIComponent(motivo);
  return { tipo: 'redirect', location: `${origen}/?waitlist=${q}#ns-live-waitlist` };
}

export async function onRequestPost({ request, env }) {
  const url = new URL(request.url);
  const origen = url.origin;
  const esFetch = !!request.headers.get('x-ns-fetch');
  const gateway = env && env.NS_GATEWAY;
  const fallo = (status, motivo) => esFetch
    ? new Response(JSON.stringify({ ok: false, motivo }), { status, headers: { 'content-type': 'application/json' } })
    : Response.redirect(`${origen}/?waitlist=${encodeURIComponent(motivo)}#ns-live-waitlist`, 303);
  if (!gateway) return fallo(503, 'gateway-unconfigured');

  const ct = request.headers.get('content-type') || '';
  const body = await request.text();
  const r = await fetch(EDGE, {
    method: 'POST',
    headers: {
      'content-type': ct || 'application/x-www-form-urlencoded',
      'apikey': ANON,
      'authorization': 'Bearer ' + ANON,
      'x-ns-gateway': gateway,
      'x-ns-ip': request.headers.get('cf-connecting-ip') || '',
      'x-ns-origin': request.headers.get('origin') || '',
    },
    body,
  }).catch(() => null);
  if (!r) return fallo(502, 'edge-unreachable');
  const texto = await r.text();
  let j = null; try { j = JSON.parse(texto); } catch { j = null; }
  if (!j) return fallo(502, 'edge-bad-response');
  const t = traduce(j, esFetch, origen);
  if (t.tipo === 'json') return new Response(JSON.stringify(j), { status: r.status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
  return Response.redirect(t.location, 303);
}

export async function onRequest({ request }) {
  // solo POST (el GET de un curioso no es un alta)
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: { 'allow': 'POST' } });
  return new Response(JSON.stringify({ ok: false, motivo: 'method' }), { status: 405, headers: { 'content-type': 'application/json', 'allow': 'POST' } });
}
