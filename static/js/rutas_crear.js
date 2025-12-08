// static/js/rutas_crear.js

document.addEventListener("DOMContentLoaded", function () {
    const formFiltros   = document.getElementById("form-filtros");
    const formBusqueda  = document.getElementById("form-busqueda");
    const contenedor    = document.getElementById("contenedor-tabla");
    const inputBusqueda = document.getElementById("busquedaInput");

    if (!formFiltros || !formBusqueda || !contenedor || !inputBusqueda) {
        return;
    }

    function buildParams() {
        const params = new URLSearchParams(new FormData(formFiltros));
        const busqFormData = new FormData(formBusqueda);

        for (const [k, v] of busqFormData.entries()) {
            // si viene vacío, lo eliminamos para no ensuciar la URL
            if (v === "") {
                params.delete(k);
            } else {
                params.set(k, v);
            }
        }
        params.delete("page");  // cada vez que cambio filtros/búsqueda, vuelvo a la página 1
        return params;
    }

    function cargarTablaConParams(params) {
        const url = window.location.pathname + "?" + params.toString();
        fetch(url, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(resp => resp.json())
        .then(data => {
            if (data.html) {
                contenedor.innerHTML = data.html;
            }
        })
        .catch(err => {
            // En producción podrías loguearlo; aquí lo dejamos silencioso
            console.error("Error cargando tabla de rutas:", err);
        });
    }

    // Búsqueda mientras escribe (con debounce)
    let timer = null;
    inputBusqueda.addEventListener("input", function () {
        clearTimeout(timer);
        timer = setTimeout(function () {
            const params = buildParams();
            cargarTablaConParams(params);
        }, 350);
    });

    // Paginación AJAX (delegación sobre todo el documento)
    document.addEventListener("click", function (e) {
        const link = e.target.closest(".pagination a.page-link");
        if (!link) return;

        e.preventDefault();
        const urlClick = new URL(link.href);
        const params = buildParams();
        params.set("page", urlClick.searchParams.get("page") || "1");
        cargarTablaConParams(params);
    });

    // Rellenar fecha desde botones con data-fill-date (si los hay en la tabla)
    document.addEventListener("click", function (e) {
        const btn = e.target.closest("[data-fill-date]");
        if (!btn) return;

        const fila = btn.closest("tr");
        if (!fila) return;

        const inputFecha = fila.querySelector('input[type="date"]');
        if (inputFecha) {
            inputFecha.value = btn.dataset.fillDate;
        }
    });
});