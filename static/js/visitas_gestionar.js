/* ============================================================
    JS — Gestionar Visitas Médicas
    Funciones:
    1) Filtro local del buscador (máximo 10 resultados visibles)
    2) Apertura del modal de prescripciones vía AJAX (fetch)
============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    /* ============================================
       🔎 1. FILTRO LOCAL DE DOCTORES
    ============================================ */
    const inputFiltro = document.getElementById("filtroDoctor");
    const tabla = document.getElementById("tablaDoctores");
    const filas = tabla ? Array.from(tabla.querySelectorAll("tbody tr")) : [];

    function aplicarFiltro() {
        const texto = (inputFiltro.value || "").toLowerCase();
        let visibles = 0;

        filas.forEach(tr => {
            const contenido = tr.textContent.toLowerCase();
            const mostrar = contenido.includes(texto) && visibles < 10;

            tr.style.display = mostrar ? "" : "none";
            if (mostrar) visibles++;
        });
    }

    if (inputFiltro) {
        aplicarFiltro();
        inputFiltro.addEventListener("input", aplicarFiltro);
    }

    /* ============================================
       📄 2. MODAL DE PRESCRIPCIONES (AJAX)
    ============================================ */
    const modalEl = document.getElementById("prescModal");
    const modalBody = document.getElementById("prescModalBody");
    let modalInstance = null;

    function getModal() {
        if (!modalInstance) modalInstance = new bootstrap.Modal(modalEl);
        return modalInstance;
    }

    async function cargarPrescripciones(doctorId) {
        modalBody.innerHTML = `
            <div class="text-center text-muted py-5">Cargando…</div>
        `;
        getModal().show();

        try {
            const resp = await fetch(`/doctores/prescripciones/${doctorId}/`, {
                credentials: "same-origin"
            });

            if (!resp.ok) throw new Error(`Error ${resp.status}`);

            modalBody.innerHTML = await resp.text();

        } catch (err) {
            modalBody.innerHTML = `
                <div class="alert alert-danger">
                    No se pudo cargar la información. ${err.message}
                </div>
            `;
        }
    }

    /* Evento delegado para botones */
    document.addEventListener("click", (ev) => {
        const btn = ev.target.closest("[data-action='open-presc']");
        if (!btn) return;

        ev.preventDefault();
        const doctorId = btn.getAttribute("data-doctor-id");

        if (doctorId) cargarPrescripciones(doctorId);
    });

});