// sobrescritura del submit del formulario registrar unidad
$(document).on('submit', '#formRgContenido', function (e) {
    e.preventDefault();

    var nombre = $('#nombreContenido').val();
    var descripcion = $('#descripcionContenido').val();
    var unidad_id = $('#selectUnidad').val();

    $.ajax({
        type: 'POST',
        url: '/create_contenido/',  // Ruta para registrar el contenido (ajusta según tu proyecto)
        data: {
            'nombre': nombre,
            'descripcion': descripcion,
            'unidad_id': unidad_id,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        success: function (data) {
            if (data.result === 'success') {
                // Obtener la URL actual sin parámetros
                var currentUrl = window.location.href.split('?')[0];

                // Redirigir la página con el parámetro en la URL
                window.location.href = currentUrl + "?showAlert=true";
            } else {
                alert(data.message);
            }
        },
        error: function () {
            mostrarAlerta(d.message,"danger","#alertMessage")
        }
    });
});
//$(".btnObtenerContenido").click(function ());


$(document).ready(function () {
    // Obtener el elemento select
    var selectUnidad = $('#selectUnidad');

    // Lógica para cargar los datos de unidades en el select
    $.ajax({
        url: '/obtener_unidades/',  // Ruta para obtener los datos de unidades (ajusta según tu proyecto)
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // Iterar a través de los datos y agregar opciones al select
            $.each(data, function (index, unidad) {
                selectUnidad.append($('<option>', {
                    value: unidad.id,
                    text: unidad.nombre
                }));
            });
        },
        error: function () {
            console.log('Error al cargar los datos de unidades.');
        }
    });

    // Obtener el valor del parámetro en la URL
    var params = new URLSearchParams(window.location.search);
    var showAlert = params.get('showAlert');

    if (showAlert === 'true') {
        // Mostrar la alerta de éxito
        mostrarAlerta("Se registro el contenido correctamente.", "success","#alertMessage");

        // Remover el parámetro de la URL para que no se acumule
        history.replaceState({}, document.title, window.location.pathname);
    }
});
