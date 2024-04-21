// frontend\prueba\sw.js

/* TRABAJADOR DE SERVICIO PARA PWA */

/* ************************************************************************
Valores de configuración */
let versionCacheActual;
let clavePublicaServidor;
let urlServidorSuscribir;
let contenidoEnCache = [];

/* ************************************************************************
Funciones y políticas para Caches */
const cachePrimero = (evento) => {
    evento.respondWith(
        caches.match(evento.request).then((cacheResponse) => {
            return cacheResponse || fetch(evento.request).then(async (networkResponse) => {
                const cache = await caches.open(versionCacheActual);
                await cache.put(evento.request, networkResponse.clone());
                return networkResponse;
            })
        })
    );
};
const redPrimero = (evento) => {
    evento.respondWith(
        fetch(evento.request)
        .then(async (networkResponse) => {
            const cache = await caches.open(versionCacheActual);
            await cache.put(evento.request, networkResponse.clone());
            return networkResponse;
        })
        .catch(() => {
            return caches.match(evento.request);
        })
    );
};
const redSolamente = (evento) => {
    evento.respondWith(fetch(evento.request));
};
const debeRevalidarse = (evento) => {
    evento.respondWith(
        caches.match(evento.request).then((cacheResponse) => {
            if (cacheResponse) {
                fetch(evento.request).then(async (networkResponse) => {
                    const cache = await caches.open(versionCacheActual);
                    await cache.put(evento.request, networkResponse.clone());
                    return networkResponse;
                });
                return cacheResponse;
            } else {
                return fetch(evento.request).then((networkResponse) => {
                    return caches.open(versionCacheActual).then(async (cache) => {
                        await cache.put(evento.request, networkResponse.clone());
                        return networkResponse;
                    })
                });
            }
        })
    );
};
const metodoCache = {
    cachePrimero, redPrimero, redSolamente, debeRevalidarse
};
let enrutadorCache = {
	find: (url) => enrutadorCache.reglas.find(it => url.match(it.url)),
	reglas: []
};

/* ************************************************************************
Oyentes y manejadores de eventos del Service Worker + Manejo de Caches */
self.addEventListener('install', evento => {
    //console.log('Service Worker instalado');
    evento.waitUntil(
        Promise.all([
            // Cargar configuración de Caches desde JSON
            fetch('./cache.json')
            .then(response => response.json())
            .then(config => {
                versionCacheActual = config.versionCache;
                contenidoEnCache = config.contenidoEnCache;
                enrutadorCache.reglas = config.reglasCache.map(regla => {
                    return { url: regla.url, handle: metodoCache[regla.handle] };
                });
            }),
            // Abrir y configurar el Cache
            caches.open(versionCacheActual)
            .then(cache => cache.addAll(contenidoEnCache))
        ]).then(() => self.skipWaiting())
    );
});
self.addEventListener( 'activate', (evento) => {
    //console.log('Service Worker activado');
	evento.waitUntil(
		caches.keys().then(cacheNames => Promise.all(
			cacheNames
			.filter(cacheName => cacheName !== versionCacheActual)
			.map(cacheName => caches.delete(cacheName))
		))
        .then(self.clients.claim())
	);
});
self.addEventListener( 'fetch', (evento) => {
	const encontrada = enrutadorCache.find(evento.request.url);
	if (encontrada) encontrada.handle(evento);
});

/* ************************************************************************
Oyentes y manejadores de eventos para Notificaciones push */
self.addEventListener('push', async (evento) => {
    if (evento.data) {
        const datosNotificacion = evento.data.json();
        const opciones = {
            body: datosNotificacion.body,
            icon: datosNotificacion.icon,
            data: { "url": datosNotificacion.url } // Paso de url para usarla en notificationclick
        };
        self.clients.matchAll().then(clients => {
            clients.forEach(client => {
                client.postMessage({
                    type: 'NOTIFICATION_RECEIVED',
                    data: datosNotificacion
                });
            });
        });
        evento.waitUntil(self.registration.showNotification(datosNotificacion.title, opciones));
    }
});
self.addEventListener('notificationclick', (evento) => {
    //console.log('Notificación recibida');
    evento.notification.close();
    // Recupera url recibida en push/evento.data
    const url = evento.notification.data["url"];
    if (url) evento.waitUntil(self.clients.openWindow(url));
});
self.addEventListener('pushsubscriptionchange', async (evento) => {
    //console.log('Suscripción cambiada. Obteniendo nueva suscripción...');
    try {
        const nuevaSuscripcion = await self.registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: clavePublicaServidor
        });
        await fetch(urlServidorSuscribir, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(nuevaSuscripcion)
        });
        //console.log('Nueva suscripción enviada al servidor.');
    } catch (error) {
        console.error('Error al manejar el cambio de suscripción:', error);
    }
});
self.addEventListener('message', evento => {
    if (evento.data && evento.data.clavePublicaServidor && evento.data.urlServidorSuscribir) {
        clavePublicaServidor = evento.data.clavePublicaServidor;
        urlServidorSuscribir = evento.data.urlServidorSuscribir;
    }
});
