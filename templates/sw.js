// Static assets: Cache-first
if (event.request.url.includes('/static/')) {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            return cachedResponse || fetch(event.request)...
```[cite: 34]

Because it is set to **Cache-First**, the service worker intercepted your earlier image requests when the files were 404ing or missing and stored those broken responses[cite: 34]. On every normal reload, it reads directly from the cache rather than asking your server[cite: 34].

Here is the complete updated code for **`templates/sw.js`** (or your root service worker file)[cite: 34]. It bumps the cache to `'wellful-home-v4'`, purges all legacy caches immediately on activate, and switches static assets to a **Network-First** strategy with caching so you never get trapped with stale 404s again[cite: 34].

### `templates/sw.js` (Complete File)

```javascript
const CACHE_NAME = 'wellful-home-v4';
const STATIC_ASSETS = [
    '/',
    '/static/manifest.json',
    '/static/images/well_logo.jpg',
    '/static/images/pillars/well_care.jpg',
    '/static/images/pillars/well_data.jpg',
    '/static/images/pillars/well_devices.jpg',
    '/static/images/pillars/well_fit.jpg',
    '/static/images/pillars/well_food.jpg',
    '/static/images/pillars/well_san.jpg',
    '/static/images/pillars/well_sole.jpg'
];

// Install Event: Cache essential shell assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS);
        })
    );
    self.skipWaiting();
});

// Activate Event: Wipe every older cache version immediately
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch Event: Network-First across all assets to prevent stale image 404s
self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;

    event.respondWith(
        fetch(event.request)
            .then((networkResponse) => {
                // Only cache valid 200 OK responses
                if (networkResponse && networkResponse.status === 200) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return networkResponse;
            })
            .catch(() => {
                // Fallback to cache only when truly offline or disconnected
                return caches.match(event.request);
            })
    );
});