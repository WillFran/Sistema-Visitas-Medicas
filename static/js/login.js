// static/js/login.js

document.addEventListener('DOMContentLoaded', function () {

    const toggleBtn = document.querySelector('.btn-password-toggle');
    const input = document.querySelector('.password-wrapper input');

    if (!toggleBtn || !input) return;

    const eye = `
        <svg class="icon-eye" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"
                  stroke="currentColor" stroke-width="2" fill="none" />
            <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" fill="none" />
        </svg>
    `;

    const eyeOff = `
        <svg class="icon-eye-off" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M1 1l22 22" stroke="currentColor" stroke-width="2"/>
            <path d="M10.6 10.6a3 3 0 004.8 4.8" stroke="currentColor" stroke-width="2"/>
            <path d="M4.5 4.5C2.5 6.3 1 8.9 1 12c0 0 4 7 11 7 2.4 0 4.5-.7 6.3-1.8"
                  stroke="currentColor" stroke-width="2"/>
            <path d="M22.9 13.2c.1-.4.1-.8.1-1.2 0 0-4-7-11-7-1.4 0-2.7.2-3.9.7"
                  stroke="currentColor" stroke-width="2"/>
        </svg>
    `;

    // Ícono inicial
    toggleBtn.innerHTML = eye;

    // Evento de mostrar/ocultar contraseña
    toggleBtn.addEventListener('click', () => {

        const isPassword = input.type === "password";

        input.type = isPassword ? "text" : "password";
        toggleBtn.innerHTML = isPassword ? eyeOff : eye;
    });
});