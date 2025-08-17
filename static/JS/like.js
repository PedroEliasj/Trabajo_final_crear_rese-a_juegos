document.addEventListener("DOMContentLoaded", () => {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    document.querySelectorAll(".like-label").forEach(label => {
        label.addEventListener("click", function (e) {
            e.preventDefault();
            const checkbox = this.previousElementSibling;
            const postId = checkbox.id.split("-")[1];

            fetch(`/like/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => response.json())
            .then(data => {
                const countEl = document.getElementById(`like-count-${postId}`);
                if (countEl) {
                    countEl.textContent = data.total_likes;
                }

                if (data.liked) {
                    checkbox.checked = true;
                    this.querySelector("i").classList.add("liked");
                } else {
                    checkbox.checked = false;
                    this.querySelector("i").classList.remove("liked");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
