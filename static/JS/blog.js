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
document.addEventListener('DOMContentLoaded', function () {
    // Seleccionar elementos
    const carruselTrack = document.querySelector('.carrusel-track');
    const prevBtn = document.querySelector('.carrusel-btn.prev-btn');
    const nextBtn = document.querySelector('.carrusel-btn.next-btn');
    const filtroBotones = document.querySelectorAll('.filtro-btn');
    const cards = document.querySelectorAll('.card');

    // Manejo del carrusel
    function updateCarruselButtons() {
        const scrollLeft = carruselTrack.scrollLeft;
        const maxScroll = carruselTrack.scrollWidth - carruselTrack.clientWidth;

        prevBtn.disabled = scrollLeft <= 0;
        nextBtn.disabled = scrollLeft >= maxScroll;
    }

    prevBtn.addEventListener('click', () => {
        carruselTrack.scrollBy({ left: -100, behavior: 'smooth' });
        updateCarruselButtons();
    });

    nextBtn.addEventListener('click', () => {
        carruselTrack.scrollBy({ left: 100, behavior: 'smooth' });
        updateCarruselButtons();
    });

    carruselTrack.addEventListener('scroll', updateCarruselButtons);
    updateCarruselButtons();

    // Estado de los filtros
    let filtroActivo = {
        categoria: 'all', // Categoría seleccionada
        fecha: null,      // Orden por fecha (reciente o antiguo)
        comentarios: null // Orden por comentarios (mas o menos)
    };

    // Función para filtrar y ordenar las cards
    function aplicarFiltros() {
        // Obtener todas las cards
        cards.forEach(card => {
            const categoria = card.querySelector('.categoria').textContent.trim();
            let mostrar = true;

            // Filtrar por categoría
            if (filtroActivo.categoria !== 'all' && categoria !== filtroActivo.categoria) {
                mostrar = false;
            }

            // Mostrar u ocultar la card
            card.style.display = mostrar ? 'flex' : 'none';
        });

        // Ordenar las cards visibles
        let cardsVisibles = Array.from(cards).filter(card => card.style.display !== 'none');
        if (filtroActivo.fecha) {
            cardsVisibles.sort((a, b) => {
                const fechaA = new Date(a.querySelector('.fecha-post').textContent.trim());
                const fechaB = new Date(b.querySelector('.fecha-post').textContent.trim());
                return filtroActivo.fecha === 'reciente' ? fechaB - fechaA : fechaA - fechaB;
            });
        } else if (filtroActivo.comentarios) {
            cardsVisibles.sort((a, b) => {
                const comentariosA = parseInt(a.querySelector('.lista-com').children.length) || 0;
                const comentariosB = parseInt(b.querySelector('.lista-com').children.length) || 0;
                return filtroActivo.comentarios === 'mas' ? comentariosB - comentariosA : comentariosA - comentariosB;
            });
        }

        // Reordenar las cards en el DOM
        const blog = document.querySelector('.blog');
        cardsVisibles.forEach(card => blog.appendChild(card));
    }

    // Manejo de clics en los botones de filtro
    filtroBotones.forEach(boton => {
        boton.addEventListener('click', () => {
            // Remover clase active de todos los botones del mismo tipo
            const tipoFiltro = boton.dataset.filtro;
            document.querySelectorAll(`.filtro-btn[data-filtro="${tipoFiltro}"]`).forEach(btn => {
                btn.classList.remove('active');
            });

            // Agregar clase active al botón clicado
            boton.classList.add('active');

            // Actualizar estado del filtro
            if (tipoFiltro === 'categoria') {
                filtroActivo.categoria = boton.dataset.categoria;
            } else if (tipoFiltro === 'fecha') {
                filtroActivo.fecha = boton.dataset.orden;
                filtroActivo.comentarios = null; // Desactivar filtro de comentarios
                document.querySelectorAll('.filtro-btn[data-filtro="comentarios"]').forEach(btn => {
                    btn.classList.remove('active');
                });
            } else if (tipoFiltro === 'comentarios') {
                filtroActivo.comentarios = boton.dataset.orden;
                filtroActivo.fecha = null; // Desactivar filtro de fecha
                document.querySelectorAll('.filtro-btn[data-filtro="fecha"]').forEach(btn => {
                    btn.classList.remove('active');
                });
            }

            // Aplicar filtros y ordenamiento
            aplicarFiltros();
        });
    });

    // Establecer el filtro "Todos" como activo por defecto
    document.querySelector('.filtro-btn[data-categoria="all"]').classList.add('active');
    aplicarFiltros();
});