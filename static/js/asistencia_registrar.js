// static/js/asistencia_registrar.js

document.addEventListener('DOMContentLoaded', function () {
    const ubicacionTexto = document.getElementById('ubicacionTexto');
    const ubicacionInput = document.getElementById('ubicacionInput');
    const linkUbicacion = document.getElementById('linkUbicacion');
    const ubicacionError = document.getElementById('ubicacionError');

    if (!ubicacionTexto || !ubicacionInput) {
        return;  // Por si se reutiliza el JS en otra vista
    }

    // Verificar soporte de geolocalización
    if (!navigator.geolocation) {
        ubicacionTexto.textContent = 'No disponible en este navegador.';
        if (ubicacionError) {
            ubicacionError.textContent = 'Este navegador no soporta geolocalización.';
            ubicacionError.style.display = 'block';
        }
        return;
    }

    // Obtener ubicación
    navigator.geolocation.getCurrentPosition(
        function (position) {
            const lat = position.coords.latitude.toFixed(6);
            const lon = position.coords.longitude.toFixed(6);
            const coords = `${lat}, ${lon}`;

            // Ocultamos coordenadas directas para elegancia
            ubicacionTexto.textContent = "Ubicación detectada";

            const ubicacionGeneral = document.getElementById("ubicacionGeneral");
            if (ubicacionGeneral) ubicacionGeneral.style.display = "block";

            ubicacionInput.value = coords;

            if (linkUbicacion) {
                linkUbicacion.href = `https://www.google.com/maps?q=${coords}`;
                linkUbicacion.style.display = 'inline-block';
            }
        },
        function (error) {
            let mensaje;
            switch (error.code) {
                case 1:
                    mensaje = 'Permiso denegado para acceder a la ubicación.';
                    break;
                case 2:
                    mensaje = 'La ubicación no está disponible en este momento.';
                    break;
                case 3:
                    mensaje = 'La solicitud de ubicación ha expirado.';
                    break;
                default:
                    mensaje = 'Ocurrió un error al obtener la ubicación.';
            }

            ubicacionTexto.textContent = 'No disponible';
            if (ubicacionError) {
                ubicacionError.textContent = `⚠️ ${mensaje}`;
                ubicacionError.style.display = 'block';
            }
        },
        {
            enableHighAccuracy: false,
            timeout: 10000,
            maximumAge: 0
        }
    );
});