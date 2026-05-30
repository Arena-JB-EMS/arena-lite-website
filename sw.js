// Arena Lite — Service Worker v1.0.0
// Caches the landing site shell for offline/fast load.
// GAS portal calls are always network-only (never cached here).
// thearenahub.com only — not the GAS portal itself.

const CACHE_NAME    = 'arena-lite-site-v1.0.0';
const NETWORK_ONLY  = ['script.google.com', 'run.app', 'stripe.com', 'fonts.googleapis.com'];

const PRECACHE = [
  './',
  './index.html',
  './signup.html',
  './dpa.html',
  './manifest.json',
  './assets/arena-icon-192.png',
  './assets/arena-icon-512.png'
];

// ── Install: pre-cache shell ────────────────────────────────────────────────
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        // addAll — fail silently on individual asset misses (optional assets)
        return Promise.allSettled(PRECACHE.map(function(url) {
          return cache.add(url).catch(function() {});
        }));
      })
      .then(function() { return self.skipWaiting(); })
  );
});

// ── Activate: clear old caches ──────────────────────────────────────────────
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) { return k !== CACHE_NAME; })
            .map(function(k) { return caches.delete(k); })
      );
    }).then(function() { return self.clients.claim(); })
  );
});

// ── Fetch: smart routing ────────────────────────────────────────────────────
self.addEventListener('fetch', function(event) {
  var url = event.request.url;

  // Always network-only for GAS, Cloud Run, Stripe, Google Fonts
  var isNetworkOnly = NETWORK_ONLY.some(function(host) {
    return url.indexOf(host) !== -1;
  });
  if (isNetworkOnly) return; // let browser handle normally

  // Non-GET: passthrough
  if (event.request.method !== 'GET') return;

  event.respondWith(
    // Network-first: try live, fall back to cache, last resort = offline shell
    fetch(event.request)
      .then(function(response) {
        if (response.ok) {
          var clone = response.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(event.request, clone);
          });
        }
        return response;
      })
      .catch(function() {
        return caches.match(event.request)
          .then(function(cached) {
            if (cached) return cached;
            // Fallback for navigate requests
            if (event.request.mode === 'navigate') {
              return caches.match('./index.html');
            }
            return new Response('', { status: 503 });
          });
      })
  );
});
