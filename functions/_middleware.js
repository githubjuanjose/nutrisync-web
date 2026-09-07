/* NutriSync · Pages Function.
   r26-c (5-sep): el host *.pages.dev del proyecto NO pasa por Cloudflare Access (Access cuelga del dominio propio), así
   que /hub/* —incluidos los PDF confidenciales de compliance y las UST— se servían en abierto en
   nutrisync-collective.pages.dev (medido con curl: 200 + application/pdf). Aquí cualquier petición a /hub en un host
   pages.dev se manda al dominio propio, donde SÍ está la puerta.
   UST-10 (7-sep): la raíz es la Web V2 y la v1 vive en /v1/. Las salas con PIN (Builders · Pitch) están en el index de la
   v1 y por WhatsApp circulan enlaces antiguos nutrisynccollective.com/?sala=pitch: se redirigen a /v1/?sala=pitch.
   publish/_routes.json limita la Function a «/», /hub y /hub/*. */
export const onRequest = async ({ request, next }) => {
  const url = new URL(request.url);
  if (url.hostname.endsWith('.pages.dev') && (url.pathname === '/hub' || url.pathname.startsWith('/hub/'))) {
    return Response.redirect('https://nutrisynccollective.com' + url.pathname + url.search, 301);
  }
  if (url.pathname === '/' && url.searchParams.has('sala')) {
    return Response.redirect(url.origin + '/v1/' + url.search, 302);
  }
  return next();
};
