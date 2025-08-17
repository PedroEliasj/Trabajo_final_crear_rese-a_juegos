document.addEventListener("DOMContentLoaded", () => {
    const csrftoken = window.csrfToken;

    document.querySelectorAll(".like-checkbox").forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            const postId = this.dataset.id;

            fetch(`/like/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => {
                if (!response.ok) throw new Error("Error en la petición AJAX");
                return response.json();
            })
            .then(data => {
                // Actualizar contador
                const countEl = document.getElementById(`like-count-${postId}`);
                if (countEl) {
                    countEl.textContent = data.total_likes;
                }

                // Cambiar estado del corazón
                const label = document.querySelector(`label[for='like-${postId}'] i`);
                if (data.liked) {
                    this.checked = true;
                    if (label) label.classList.add("liked");
                } else {
                    this.checked = false;
                    if (label) label.classList.remove("liked");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
