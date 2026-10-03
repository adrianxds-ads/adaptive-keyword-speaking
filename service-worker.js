self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(Promise.all([self.registration.unregister(),caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith('keyword-speaking')).map(k=>caches.delete(k))))]).then(()=>self.clients.claim())));
self.addEventListener('fetch',()=>{});
