// === Переключатель темы ===
document.addEventListener("DOMContentLoaded", () => {
        
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            document.body.classList.toggle("alt-theme");
        });
    }

    // === Live-preview для выбора цвета неона ===
    const neonInput = document.getElementById("id_neon_color");
    const profileCard = document.querySelector(".profile-card");
    if (neonInput && profileCard) {
        neonInput.addEventListener("input", () => {
            profileCard.style.borderColor = neonInput.value;
            profileCard.style.boxShadow = `0 0 20px ${neonInput.value}`;
        });
    }

    // === Валидация BIO ===
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", (e) => {
            const bio = document.getElementById("id_bio");
            if (bio && bio.value.length < 10) {
                e.preventDefault();
                alert("BIO должно содержать хотя бы 10 символов!");
            }
        });
    }
});