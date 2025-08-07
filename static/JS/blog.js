// BOTON IR ARRIBA
document.addEventListener('DOMContentLoaded', function () {
    const label = document.querySelector('.ir');
    const checkbox = document.querySelector('.toggle-neon');

    if (!label || !checkbox) {
        console.error('Error: No se encontró .ir o .toggle-neon. Verifica el HTML.');
        return;
    }

    // Evento de clic para encender el neón y subir
    label.addEventListener('click', function () {
        checkbox.checked = true; // Enciende el neón
        console.log('Clic en el botón, neón encendido, checked:', checkbox.checked);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Manejador de scroll
    window.addEventListener('scroll', function () {
        try {
            if (window.scrollY > 100) {
                label.style.display = 'block';
                //checkbox.checked = false; // Apaga el neón al reaparecer//estuve toda la tarde viendo cual era el error del encendido del neon y era esta linea que hace que el neon se apague cuando soltas el click!
                console.log('Scroll > 100: Botón mostrado, neón apagado, checked:', checkbox.checked);
            } else if (window.scrollY <= 100) {
                label.style.display = 'none';
                checkbox.checked = false; // Apaga el neón al ocultar
                console.log('Scroll <= 100: Botón oculto, neón apagado, checked:', checkbox.checked);
            }
        } catch (error) {
            console.error('Error en el manejador de scroll:', error);
        }
    });
});


//FILTRO

// Carrusel
const track = document.querySelector('.carrusel-track');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const filtroButtons = document.querySelectorAll('.filtro-btn');

function updateButtons() {
    const scrollLeft = track.scrollLeft;
    const maxScroll = track.scrollWidth - track.clientWidth;
    
    prevBtn.disabled = scrollLeft <= 0;
    nextBtn.disabled = scrollLeft >= maxScroll;
}

prevBtn.addEventListener('click', () => {
    track.scrollBy({ left: -150, behavior: 'smooth' });
    setTimeout(updateButtons, 300);
});

nextBtn.addEventListener('click', () => {
    track.scrollBy({ left: 150, behavior: 'smooth' });
    setTimeout(updateButtons, 300);
});

track.addEventListener('scroll', updateButtons);
updateButtons(); // Inicializa estado de botones

// Filtrado
filtroButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remover clase active de todos los botones
        filtroButtons.forEach(b => b.classList.remove('active'));
        // Agregar clase active al botón clicado
        btn.classList.add('active');
        
        const categoria = btn.getAttribute('data-categoria');
        document.querySelectorAll('.card').forEach(card => {
            const cardCategoria = card.querySelector('.categoria').textContent;
            card.style.display = categoria === 'all' || cardCategoria === categoria ? 'block' : 'none';
        });
    });
});

// Marcar "Todos" como activo por defecto
document.querySelector('.filtro-btn[data-categoria="all"]').classList.add('active');