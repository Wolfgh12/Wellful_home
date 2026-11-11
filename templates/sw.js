const CACHE_NAME = 'wellful-home-v7';
const STATIC_ASSETS = [
    '/',
    '/manifest.json',
    '/static/images/Wellful_logo.jpg',
    '/static/images/Wellful_logo_192.png',
    '/static/images/Wellful_logo_512.png',
    '/static/images/pillars/well_care.jpg',
    '/static/images/pillars/well_data.jpg',
    '/static/images/pillars/well_devices.jpg',
    '/static/images/pillars/well_fit.jpg',
    '/static/images/pillars/well_food.jpg',
    '/static/images/pillars/well_san.jpg',
    '/static/images/pillars/well_sole.jpg'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) =>
            Promise.allSettled(STATIC_ASSETS.map((url) => cache.add(url)))
        )
    );
    self.skipWaiting();
});

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

self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;

    event.respondWith(
        fetch(event.request)
            .then((networkResponse) => {
                if (networkResponse && networkResponse.status === 200) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return networkResponse;
            })
            .catch(() => caches.match(event.request))
    );
});