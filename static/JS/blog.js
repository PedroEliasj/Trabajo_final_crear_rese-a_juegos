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

document.addEventListener('DOMContentLoaded', function () {
    // Seleccionar elementos
    const carruselTrack = document.querySelector('.carrusel-track');
    const prevBtn = document.querySelector('.carrusel-btn.prev-btn');
    const nextBtn = document.querySelector('.carrusel-btn.next-btn');
    const filtroBotones = document.querySelectorAll('.filtro-btn');
    const tipoBotones = document.querySelectorAll('.filtro-tipo-btn');
    const filtroGrupos = document.querySelectorAll('.filtro-grupo');
    const cards = document.querySelectorAll('.card');

    // Depuración: Verificar selección de elementos
    console.log('Botones de tipo (.filtro-tipo-btn):', tipoBotones.length);
    tipoBotones.forEach((btn, i) => console.log(`Botón ${i + 1}:`, btn.dataset.tipo));
    console.log('Grupos de filtros (.filtro-grupo):', filtroGrupos.length);
    filtroGrupos.forEach((grupo, i) => console.log(`Grupo ${i + 1}:`, grupo.className));
    console.log('Botones de filtro (.filtro-btn):', filtroBotones.length);
    console.log('Cards (.card):', cards.length);

    // Manejo del carrusel
    function updateCarruselButtons() {
        const scrollLeft = carruselTrack.scrollLeft;
        const maxScroll = carruselTrack.scrollWidth - carruselTrack.clientWidth;
        prevBtn.disabled = scrollLeft <= 0;
        nextBtn.disabled = scrollLeft >= maxScroll;
        console.log('Carrusel actualizado:', { scrollLeft, maxScroll });
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
        categoria: 'all',
        fecha: null,
        comentarios: null
    };

    // Función para filtrar y ordenar las cards
    function aplicarFiltros() {
        console.log('Aplicando filtros:', filtroActivo);

        cards.forEach(card => {
            const categoria = card.querySelector('.categoria')?.textContent.trim();
            let mostrar = true;

            if (filtroActivo.categoria !== 'all' && categoria !== filtroActivo.categoria) {
                mostrar = false;
            }

            card.style.display = mostrar ? 'flex' : 'none';
        });

        let cardsVisibles = Array.from(cards).filter(card => card.style.display !== 'none');
        if (filtroActivo.fecha) {
            console.log('Ordenando por fecha:', filtroActivo.fecha);
            cardsVisibles.sort((a, b) => {
                const fechaA = new Date(a.querySelector('.fecha-post')?.textContent.trim());
                const fechaB = new Date(b.querySelector('.fecha-post')?.textContent.trim());
                if (isNaN(fechaA) || isNaN(fechaB)) {
                    console.warn('Fecha inválida:', {
                        fechaA: a.querySelector('.fecha-post')?.textContent,
                        fechaB: b.querySelector('.fecha-post')?.textContent
                    });
                    return 0;
                }
                return filtroActivo.fecha === 'reciente' ? fechaB - fechaA : fechaA - fechaB;
            });
        } else if (filtroActivo.comentarios) {
            cardsVisibles.sort((a, b) => {
                const comentariosA = parseInt(a.querySelector('.lista-com').children.length) || 0;
                const comentariosB = parseInt(b.querySelector('.lista-com').children.length) || 0;
                return filtroActivo.comentarios === 'mas' ? comentariosB - comentariosA : comentariosA - comentariosB;
            });
        }

        const blog = document.querySelector('.blog');
        cardsVisibles.forEach(card => blog.appendChild(card));
    }

    // Manejo de clics en los botones de tipo de filtro
    tipoBotones.forEach(boton => {
        boton.addEventListener('click', () => {
            console.log('Tipo seleccionado:', boton.dataset.tipo);

            // Remover clase active de todos los botones de tipo
            tipoBotones.forEach(btn => {
                btn.classList.remove('active');
                console.log('Removiendo active de:', btn.dataset.tipo);
            });
            boton.classList.add('active');
            console.log('Añadiendo active a:', boton.dataset.tipo);

            // Ocultar todos los grupos de filtros y mostrar el seleccionado
            filtroGrupos.forEach(grupo => {
                grupo.classList.remove('active');
                console.log('Ocultando grupo:', grupo.className);
            });
            const grupo = document.querySelector(`.filtro-grupo.${boton.dataset.tipo}`);
            if (grupo) {
                grupo.classList.add('active');
                console.log('Mostrando grupo:', grupo.className);
            } else {
                console.error('Grupo no encontrado para:', boton.dataset.tipo);
            }

            // Reiniciar el scroll del carrusel
            carruselTrack.scrollLeft = 0;
            updateCarruselButtons();

            // Activar el primer botón del grupo si no hay ninguno activo
            const primerBoton = grupo.querySelector('.filtro-btn');
            if (!grupo.querySelector('.filtro-btn.active')) {
                primerBoton.classList.add('active');
                console.log('Activando primer botón:', primerBoton.dataset.filtro, primerBoton.dataset.categoria || primerBoton.dataset.orden);
                const tipoFiltro = primerBoton.dataset.filtro;
                if (tipoFiltro === 'categoria') {
                    filtroActivo.categoria = primerBoton.dataset.categoria;
                    filtroActivo.fecha = null;
                    filtroActivo.comentarios = null;
                } else if (tipoFiltro === 'fecha') {
                    filtroActivo.fecha = primerBoton.dataset.orden;
                    filtroActivo.categoria = 'all';
                    filtroActivo.comentarios = null;
                } else if (tipoFiltro === 'comentarios') {
                    filtroActivo.comentarios = primerBoton.dataset.orden;
                    filtroActivo.categoria = 'all';
                    filtroActivo.fecha = null;
                }
                aplicarFiltros();
            }
        });
    });

    // Manejo de clics en los botones de filtro
    filtroBotones.forEach(boton => {
        boton.addEventListener('click', () => {
            console.log('Filtro seleccionado:', {
                filtro: boton.dataset.filtro,
                categoria: boton.dataset.categoria,
                orden: boton.dataset.orden
            });

            // Remover clase active de todos los botones del mismo grupo
            const grupo = boton.closest('.filtro-grupo');
            grupo.querySelectorAll('.filtro-btn').forEach(btn => btn.classList.remove('active'));
            boton.classList.add('active');

            // Actualizar estado del filtro
            const tipoFiltro = boton.dataset.filtro;
            if (tipoFiltro === 'categoria') {
                filtroActivo.categoria = boton.dataset.categoria;
                filtroActivo.fecha = null;
                filtroActivo.comentarios = null;
            } else if (tipoFiltro === 'fecha') {
                filtroActivo.fecha = boton.dataset.orden;
                filtroActivo.categoria = 'all';
                filtroActivo.comentarios = null;
                document.querySelector('.filtro-grupo.categoria .filtro-btn[data-categoria="all"]').classList.add('active');
            } else if (tipoFiltro === 'comentarios') {
                filtroActivo.comentarios = boton.dataset.orden;
                filtroActivo.categoria = 'all';
                filtroActivo.fecha = null;
                document.querySelector('.filtro-grupo.categoria .filtro-btn[data-categoria="all"]').classList.add('active');
            }

            aplicarFiltros();
        });
    });

    // Inicialización
    const inicialTipoBtn = document.querySelector('.filtro-tipo-btn[data-tipo="categoria"]');
    const inicialGrupo = document.querySelector('.filtro-grupo.categoria');
    const inicialFiltroBtn = document.querySelector('.filtro-btn[data-categoria="all"]');
    if (inicialTipoBtn && inicialGrupo && inicialFiltroBtn) {
        inicialTipoBtn.classList.add('active');
        inicialGrupo.classList.add('active');
        inicialFiltroBtn.classList.add('active');
        console.log('Inicialización completada');
        aplicarFiltros();
    } else {
        console.error('Error en inicialización:', {
            inicialTipoBtn: !!inicialTipoBtn,
            inicialGrupo: !!inicialGrupo,
            inicialFiltroBtn: !!inicialFiltroBtn
        });
    }
});

// Búsqueda
document.addEventListener('DOMContentLoaded', function () {
    // Seleccionar elementos
    const searchInput = document.querySelector('#search-input');
    const searchBtn = document.querySelector('.search-btn');
    const cards = document.querySelectorAll('.card');

    // Depuración: Verificar selección de elementos
    console.log('Search input (#search-input):', !!searchInput);
    console.log('Search button (.search-btn):', !!searchBtn);
    console.log('Cards (.card):', cards.length);
    cards.forEach((card, i) => {
        const usuario = card.querySelector('.post-usuario span')?.textContent?.trim();
        const titulo = card.querySelector('.text-content h3')?.textContent?.trim();
        console.log(`Card ${i + 1}:`, { id: card.id, usuario, titulo });
    });

    // Verificar existencia de elementos clave
    if (!searchInput || !searchBtn || !cards.length) {
        console.error('Error: Elementos de búsqueda faltantes', {
            searchInput: !!searchInput,
            searchBtn: !!searchBtn,
            cards: cards.length
        });
        return;
    }

    // Estado de la búsqueda
    let busquedaActiva = '';

    // Función para aplicar búsqueda
    function aplicarBusqueda() {
        console.log('Aplicando búsqueda:', busquedaActiva);

        cards.forEach(card => {
            const usuario = card.querySelector('.post-usuario span')?.textContent?.trim();
            const titulo = card.querySelector('.text-content h3')?.textContent?.trim();
            let mostrar = true;

            if (busquedaActiva) {
                const busquedaLower = busquedaActiva.toLowerCase();
                const textoCompleto = `${usuario || ''} ${titulo || ''}`.toLowerCase();
                if (!textoCompleto.includes(busquedaLower)) {
                    mostrar = false;
                }
            }

            card.style.display = mostrar ? 'flex' : 'none';
            console.log('Card (búsqueda):', { id: card.id, usuario, titulo, mostrar });
        });

        const cardsVisibles = Array.from(cards).filter(card => card.style.display === 'flex');
        console.log('Cards visibles (búsqueda):', cardsVisibles.map(card => card.id));

        // Mostrar mensaje si no hay resultados
        const blog = document.querySelector('.blog');
        const existingMessage = blog.querySelector('.no-results');
        if (existingMessage) existingMessage.remove();
        if (cardsVisibles.length === 0) {
            const noResults = document.createElement('p');
            noResults.className = 'no-results';
            noResults.textContent = 'No se encontraron resultados.';
            noResults.style.color = '#15f4ee';
            noResults.style.textShadow = '0 0 5px #15f4ee';
            noResults.style.textAlign = 'center';
            noResults.style.margin = '20px 0';
            blog.appendChild(noResults);
        }
    }

    // Manejo de la barra de búsqueda
    searchInput.addEventListener('input', () => {
        busquedaActiva = searchInput.value.trim();
        console.log('Búsqueda actualizada:', busquedaActiva);
        aplicarBusqueda();
    });

    // Limpiar búsqueda al hacer clic en el botón
    searchBtn.addEventListener('click', () => {
        if (busquedaActiva) {
            searchInput.value = '';
            busquedaActiva = '';
            console.log('Búsqueda limpiada');
            aplicarBusqueda();
        }
    });

    // Inicializar búsqueda
    aplicarBusqueda();
});