/* NutriSync Web V2 · service worker (UST-07 G6): shell + fuentes precacheados, páginas network-first con respaldo,
   imágenes cache-first al vuelo, /offline/ cuando no hay red. La versión = sello del build: cada deploy limpia lo viejo. */
const V = 'ns-web2-0709-222725';
const SHELL = ['/', '/offline/', '/manifest.webmanifest', '/assets/css/site.57e8d30c.css', '/assets/js/site.e555a65a.js',
  '/assets/fonts/files/poppins-400-latin.woff2', '/assets/fonts/files/poppins-600-latin.woff2', '/assets/fonts/files/poppins-700-latin.woff2',
  '/assets/fonts/files/instrument-sans-latin.woff2', '/assets/img/logo-swirl.webp', '/assets/icons/icon-192.png'];
self.addEventListener('install', (e) => { e.waitUntil(caches.open(V).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== V).map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
/* UST-10 D4 · en producción el SW vive en la raíz de nutrisynccollective.com, junto al hub (Cloudflare Access), las
   legales, la puerta de testers, reset, el prototipo /webapp, la v1 archivada y el redirect /app. Nada de eso es de la
   V2: el SW NO lo toca (ni respondWith ni caché) — van siempre a la red, como si el SW no existiera. */
const FUERA = /^\/(hub|legal|tester|reset|webapp|app|v1|i18n|support\.js)(\/|\.|$)/;
self.addEventListener('fetch', (e) => {
  const req = e.request; if (req.method !== 'GET') return;
  const url = new URL(req.url); if (url.origin !== location.origin) return;
  if (FUERA.test(url.pathname)) return;
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then((r) => { const copy = r.clone(); caches.open(V).then((c) => c.put(req, copy)); return r; })
      .catch(() => caches.match(req).then((r) => r || caches.match('/offline/'))));
    return;
  }
  if (/\/assets\/(img|fonts|icons|css|js|i18n)\//.test(url.pathname)) {   // i18n: catálogos perezosos ca/gl/eu (UST-12), versionados por ?v=build
    e.respondWith(caches.match(req).then((r) => r || fetch(req).then((res) => { const copy = res.clone(); caches.open(V).then((c) => c.put(req, copy)); return res; })));
  }
});
