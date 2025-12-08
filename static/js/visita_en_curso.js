// static/js/visita_en_curso.js

// Copia la ubicación a ambos formularios y actualiza la UI
function setUbicacionCampos(textoVisible, valorCoords) {
  const txt  = document.getElementById("ubicacionTexto");
  const ok   = document.getElementById("ubicacionGeneral");
  const err  = document.getElementById("ubicacionError");
  const link = document.getElementById("linkUbicacion");
  const input1 = document.getElementById("ubicacionInput");
  const input2 = document.getElementById("ubicacionInputFooter");

  if (txt) txt.textContent = textoVisible;
  if (ok) ok.style.display = "block";
  if (err) err.style.display = "none";

  if (input1) input1.value = valorCoords;
  if (input2) input2.value = valorCoords;

  if (link) {
    link.href = "https://www.google.com/maps?q=" + encodeURIComponent(valorCoords);
    link.style.display = "inline";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (!navigator.geolocation) {
    const err = document.getElementById("ubicacionError");
    const txt = document.getElementById("ubicacionTexto");
    if (txt) txt.textContent = "No disponible";
    if (err) {
      err.textContent = "La geolocalización no es compatible con este navegador.";
      err.style.display = "block";
    }
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude.toFixed(6);
      const lon = position.coords.longitude.toFixed(6);
      const coords = `${lat}, ${lon}`;
      setUbicacionCampos("Ubicación detectada", coords);
    },
    (error) => {
      const mensajes = {
        1: "Permiso denegado para acceder a la ubicación.",
        2: "La ubicación no está disponible.",
        3: "La solicitud de ubicación ha expirado."
      };
      const msg = mensajes[error.code] || "Error desconocido al obtener la ubicación.";

      const txt = document.getElementById("ubicacionTexto");
      const err = document.getElementById("ubicacionError");
      if (txt) txt.textContent = "No disponible";
      if (err) {
        err.textContent = "⚠ " + msg;
        err.style.display = "block";
      }
    }
  );
});