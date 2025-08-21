document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registro-form");
    const passwordInput = document.getElementById("password");
    const confirmInput = document.getElementById("confirmar_password");

    const reqLength    = document.getElementById("req-length");
    const reqUppercase = document.getElementById("req-uppercase");
    const reqNumber    = document.getElementById("req-number");
    const reqSpecial   = document.getElementById("req-special");
    const reqMatch     = document.getElementById("req-match");
    const errorDiv     = document.getElementById("password-error");

    function validar() {
        const pass = passwordInput.value;
        const confirm = confirmInput.value;

        // Mínimo 8 caracteres
        pass.length >= 8 ? reqLength.classList.add("ok") : reqLength.classList.remove("ok");

        // Al menos una mayúscula
        /[A-Z]/.test(pass) ? reqUppercase.classList.add("ok") : reqUppercase.classList.remove("ok");

        // Al menos un número
        /\d/.test(pass) ? reqNumber.classList.add("ok") : reqNumber.classList.remove("ok");

        // Al menos un carácter especial
        /[!@#$%&*]/.test(pass) ? reqSpecial.classList.add("ok") : reqSpecial.classList.remove("ok");

        // Confirmar contraseña igual
        (pass.length > 0 && pass === confirm) ? reqMatch.classList.add("ok") : reqMatch.classList.remove("ok");
    }

    // Validar en tiempo real
    passwordInput.addEventListener("input", validar);
    confirmInput.addEventListener("input", validar);

    // Bloquear envío si falta algo
    form.addEventListener("submit", (e) => {
        validar(); // último chequeo

        const requisitos = [
            { el: reqLength, msg: "mínimo 8 caracteres" },
            { el: reqUppercase, msg: "al menos una letra mayúscula" },
            { el: reqNumber, msg: "al menos un número" },
            { el: reqSpecial, msg: "al menos un carácter especial (!@#$%&*)" },
            { el: reqMatch, msg: "que las contraseñas coincidan" }
        ];

        const faltan = requisitos.filter(req => !req.el.classList.contains("ok"));

        if (faltan.length > 0) {
            e.preventDefault();
            errorDiv.style.display = "block";
            errorDiv.innerHTML = "⚠️ Faltan los siguientes requisitos:<br> - " + faltan.map(f => f.msg).join("<br> - ");
        } else {
            errorDiv.style.display = "none"; // ocultar si todo está ok
        }
    });
});
