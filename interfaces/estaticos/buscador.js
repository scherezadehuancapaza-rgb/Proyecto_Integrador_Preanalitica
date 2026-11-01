document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('input-busqueda');
    const sugerencias = document.getElementById('sugerencias');
    const listaSeleccionados = document.getElementById('lista-seleccionados');
    let seleccionados = [];

    // Evento para buscar mientras se escribe
    input.addEventListener('input', async () => {
        const texto = input.value;
        if (texto.length < 2) {
            sugerencias.innerHTML = '';
            return;
        }
        
        try {
            const respuesta = await fetch(`/api/buscar?q=${texto}`);
            const datos = await respuesta.json();
            
            sugerencias.innerHTML = '';
            
            if (datos.length === 0) {
                sugerencias.innerHTML = '<li>No se encontraron exámenes</li>';
                return;
            }

            datos.forEach(ex => {
                const li = document.createElement('li');
                li.innerText = `${ex.nombre_examen} (${ex.seccion})`;
                li.onclick = () => agregarExamen(ex);
                sugerencias.appendChild(li);
            });
        } catch (error) {
            console.error("Error en la búsqueda:", error);
            sugerencias.innerHTML = '<li>Error al buscar.</li>';
        }
    });

    // Función para agregar un examen a la lista
    window.agregarExamen = function(examen) {
        if (seleccionados.find(e => e.id_examen === examen.id_examen)) return;
        
        seleccionados.push(examen);
        sugerencias.innerHTML = '';
        input.value = '';
        actualizarLista();
    };

    // Función para quitar un examen de la lista
    window.quitarExamen = function(id) {
        seleccionados = seleccionados.filter(e => e.id_examen !== id);
        actualizarLista();
    };

    // Función que dibuja la lista de exámenes seleccionados en pantalla
    function actualizarLista() {
        listaSeleccionados.innerHTML = '';
        
        // Limpiar inputs hidden anteriores
        document.querySelectorAll('input[name="examenes[]"]').forEach(e => e.remove());

        seleccionados.forEach(ex => {
            const li = document.createElement('li');
            li.className = 'examen-seleccionado';

            // Estructura con el nombre a la izquierda y el botón a la derecha
            li.innerHTML = `
                <div class="examen-info">
                    <strong>${ex.nombre_examen}</strong><br>
                    <small style="color: #666;">Sección: ${ex.seccion}</small>
                </div>
                <button type="button" class="btn-eliminar" onclick="quitarExamen('${ex.id_examen}')">
                    Eliminar Examen
                </button>
            `;
            listaSeleccionados.appendChild(li);

            // Input oculto para enviar los datos a Flask
            const hidden = document.createElement('input');
            hidden.type = 'hidden';
            hidden.name = 'examenes[]';
            hidden.value = ex.id_examen;
            listaSeleccionados.appendChild(hidden);
        });
    }
});