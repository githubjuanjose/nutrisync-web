/* NutriSync · Pages Function (5-sep, r26-c): el host *.pages.dev del proyecto NO pasa por Cloudflare Access (Access cuelga
   del dominio propio), así que /hub/* —incluidos los PDF confidenciales de compliance y las UST— se servían en abierto en
   nutrisync-collective.pages.dev (medido con curl: 200 + application/pdf). Aquí cualquier petición a /hub en un host pages.dev
   se manda al dominio propio, donde SÍ está la puerta. publish/_routes.json limita la Function a /hub y /hub/*. */
export const onRequest = async ({ request, next }) => {
  const url = new URL(request.url);
  if (url.hostname.endsWith('.pages.dev') && (url.pathname === '/hub' || url.pathname.startsWith('/hub/'))) {
    return Response.redirect('https://nutrisynccollective.com' + url.pathname + url.search, 301);
  }
  return next();
};
