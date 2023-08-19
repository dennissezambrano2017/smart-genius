var idMaterial = 0;
var opcionesDetalle = []
var botonAgregado = false;
autosize($('#preguntaOpciones'));
$(".btnViewMaterial").click(function () {
    var csrftoken = getCookie('csrftoken');
    var materialId = $(this).attr("vid");
    idMaterial = materialId;
    $.ajax({
        url: '/material_seleccionada/',
        type: 'GET',
        data: {
            "idMaterial": materialId,
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json',
    }).done(function (d) {
        if (d.result == '1') {
            if (!botonAgregado) {
                // Código de evento aquí (si es necesario)
                // Crea un nuevo botón
                var nuevoBoton = document.createElement("button");
                nuevoBoton.type = "button";
                nuevoBoton.className = "btn btn-sm btn-success";
                nuevoBoton.dataset.bsToggle = "modal";
                nuevoBoton.dataset.bsTarget = "#modalRegist-ejercicio";
                nuevoBoton.textContent = "Agregar Ejercicios";
                nuevoBoton.setAttribute("vid", materialId);

                // Encuentra el elemento <div> donde deseas agregar el botón
                var contenedor = document.getElementById("miDiv");

                // Agrega el botón al <div>
                contenedor.appendChild(nuevoBoton);

                // Marca el botón como agregado
                botonAgregado = true;
            }
            // Mostrar el nombre del archivo PDF seleccionado
            var pdfFileName = d.pdf.split('/').pop();
            $("#pdfFileView").val(pdfFileName);

            // Actualizar el valor del enlace
            $("#nombreEnlace").val(d.enlace);

            // Obtener el select por su ID
            var selectUnidad = $("#selectViewMaterial");

            // Limpiar las opciones previas (si las hay)
            selectUnidad.empty();

            // Recorrer los temas y agregarlos como opciones al select
            d.temas.forEach(function (tema) {
                // Crear la opción y establecer los atributos
                var option = $('<option>', {
                    value: tema.id,
                    text: tema.nombre
                });
                // Si la unidad actual es la preseleccionada, establecer el atributo "selected"
                if (tema.id === d.material_id) {
                    option.prop("selected", true);
                }

                // Agregar la opción al select
                selectUnidad.append(option);
            });


            // Actualizar la tabla de ejercicios (si es necesario)
            var tablaEjercicios = $("#tablaEjercicios");
            tablaEjercicios.empty();
            //var viewButtonCell = $(`<td style="text-align: center;">`).html();

            if (d.ejercicios.length > 0) {
                d.ejercicios.forEach(function (ejercicio) {
                    // Crear una nueva fila y celdas para la tabla de ejercicios
                    var newRow = $("<tr>");
                    var idCell = $("<td>").text(ejercicio.id);
                    var enunciadoCell = $("<td>").text(ejercicio.enunciado);
                    // Crear botones
                    var viewButton = $("<a>").addClass("btn btn-secondary")
                        .attr("href", "javascript:btnViewEjercicio(" + ejercicio.id + ");")
                        .html('<i class="fa-solid fa-eye" aria-hidden="true"></i>');

                    var deleteButton = $("<a>").addClass("btn btn-danger")
                        .attr("href", "javascript:confi_delet_ejercicio(" + ejercicio.id + ");")
                        .html('<i class="fa-solid fa-trash" aria-hidden="true"></i>');

                    var viewButtonCell = $("<td>").css("text-align", "center")
                        .append(viewButton, deleteButton);



                    // Agregar las celdas a la fila
                    newRow.append(idCell, enunciadoCell, viewButtonCell);

                    // Agregar la fila a la tabla de ejercicios
                    tablaEjercicios.append(newRow);
                });
            } else {
                //console.log(materialId)
                tablaEjercicios.append('<p>No se encontraron ejercicios registrados.</p>');


            }


        } else {
            console.log('Error en la obtención de datos');
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log('Error en la solicitud AJAX');
    });
});
$(document).ready(function () {
    // Obtener el elemento select
    var selectUnidad = $('#selectViewTema-ma');

    // Lógica para cargar los datos de unidades en el select
    $.ajax({
        url: '/obtener_temas/',
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
        mostrarAlerta("Se registro el contenido correctamente.", "success", "#alertMessage");

        // Remover el parámetro de la URL para que no se acumule
        history.replaceState({}, document.title, window.location.pathname);
    }



});
function confi_delet_ejercicio(id) {
    // Obtener una referencia al modal
    var modal = $('#modalDelet');
    // Activar el modal
    modal.modal('show');
    idElim = id;
}
// función para eliminar un contenido luego de haberse confirmado la acción
function delete_ejercicio() {
    var csrftoken = getCookie('csrftoken');
    console.log(idElim)
    $.ajax({
        url: '/eliminar_ejercicio/', 
        type: 'POST',
        data: {"idEjercicio": idElim,
        csrfmiddlewaretoken: csrftoken },
        dataType: 'json',
    }).done(function (d) {
        if(d.result == '1'){
            mostrarAlerta(d.message, "danger","#alertMessage");
        }else{
            mostrarAlerta(d.message, "danger","#alertMessag");
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        mostrarAlerta(d.message,"danger","#alertMessage")
    }).always(function (data) {
    });
    
}
function btnViewEjercicio(id) {
    $("#preguntaOpciones").prop('disabled', true);
    // Obtener una referencia al modal
    var modal = $('#modalViewRespue-material');
    // Activar el modal
    modal.modal('show');
    var csrftoken = getCookie('csrftoken');
    console.log("si entyre")
    $.ajax({
        url: '/ejercicio_material/',
        type: 'GET',
        data: {
            "ejercicioId": id,
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json',
    }).done(function (d) {
        //console.log(d)
        if (d.result == '1') {
            $("#ejercicioEnunciado").val(d.enunciado);
            // console.log(d.opciones);
            if (d.opciones.length > 0) {
                var opcionesText = ""; // Variable para almacenar el texto de las opciones

                d.opciones.forEach(function (opcion, index) {
                    opcionesText += (index + 1) + ".- " + opcion + "\n";
                });

                var textarea = $("#ejercicioOpciones");
                var respuestaCorrectaInput = $("#respuestaCorrecta");
                // Insertar el texto en el textarea
                textarea.val(opcionesText);

                // Ajustar el número de filas del textarea según la cantidad de opciones
                textarea.attr("rows", d.opciones.length);

                // Insertar la respuesta correcta en el input correspondiente
                respuestaCorrectaInput.val((d.resp_correct + 1) + ".- " + d.opciones[d.resp_correct]);
            }

        } else {
            console.log('Error en la obtención de datos');
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log('Error en la solicitud AJAX');
    });
}
$(document).on('submit', '#formRgMaterial', function (e) {
    e.preventDefault();

    var enlace = $('#nombreEnlaceReg').val();
    var archivoInput = document.getElementById('inputGroupFile01');
    var archivo = archivoInput.files[0];
    var tema_id = $('#selectViewTema-ma').val();

    var formData = new FormData(); // Usar FormData para enviar archivos
    formData.append('enlace', enlace);
    formData.append('archivo_pdf', archivo); // Cambiar 'archivo' por 'archivo_pdf'
    formData.append('tema_id', tema_id);
    formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());

    $.ajax({
        type: 'POST',
        url: '/create_material/',
        data: formData, // Usar formData en lugar de un objeto plano
        processData: false, // Evitar procesamiento automático de datos
        contentType: false, // Evitar configuración automática de contenido
        dataType: 'json',
        success: function (data) {
            if (data.result === 'success') {
                // Mostrar la alerta de éxito después de completar la redirección
                window.location.search = '?showAlert=true'; // Redirigir sin cambiar toda la URL
                // Obtener la URL actual sin parámetros
                var currentUrl = window.location.href.split('?')[0];

                // Redirigir la página con el parámetro en la URL
                window.location.href = currentUrl + "?showAlert=true";
                // Obtener el valor del parámetro en la URL
                var params = new URLSearchParams(window.location.search);
                var showAlert = params.get('showAlert');

                if (showAlert === 'true') {
                    // Mostrar la alerta de éxito
                    mostrarAlerta("Se registro el material correctamente.", "success", "#alertMessage");

                    // Remover el parámetro de la URL para que no se acumule
                    history.replaceState({}, document.title, window.location.pathname);
                }
            } else {
                mostrarAlerta(data.message, "danger", "#alertMessageRegister");
            }
        },
        error: function () {
            console.log("data.message");
            // mostrarAlerta(data.message, "danger", "#alertMessageRegister")
        }
    });
});
$(document).on('submit', '#formRgejercicio', function (e) {
    e.preventDefault();
    var csrftoken = getCookie('csrftoken');
    var enunciado = $('#preguntaEnunciado').val();
    var respuesta = $('#preguntaCorrecta').val();

    var opci = JSON.stringify(opcionesDetalle);
    console.log(enunciado, opci)
    $.ajax({
        type: 'POST',
        url: '/create_ejercicio/',
        data: {
            "enunciado": enunciado,
            "opciones": opci,
            "respuesta": respuesta,
            "material_id": idMaterial,
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json',
        success: function (data) {
            if (data.result === 'success') {
                // Mostrar la alerta de éxito después de completar la redirección
                window.location.search = '?showAlert=true'; // Redirigir sin cambiar toda la URL
                // Obtener la URL actual sin parámetros
                var currentUrl = window.location.href.split('?')[0];

                // Redirigir la página con el parámetro en la URL
                window.location.href = currentUrl + "?showAlert=true";
                // Obtener el valor del parámetro en la URL
                var params = new URLSearchParams(window.location.search);
                var showAlert = params.get('showAlert');

                if (showAlert === 'true') {
                    // Mostrar la alerta de éxito
                    mostrarAlerta("Se registro el material correctamente.", "success", "#alertMessage");

                    // Remover el parámetro de la URL para que no se acumule
                    history.replaceState({}, document.title, window.location.pathname);
                }
            } else {
                mostrarAlerta(data.message, "danger", "#alertMessageRegister");
            }
        },
        error: function () {
            console.log("data.message");
            // mostrarAlerta(data.message, "danger", "#alertMessageRegister")
        }
    });
});

$(".btnAñadirOpciones").click(function () {
    var opcion = $('#preguntaOpcion').val();
    if (opcion.trim() !== '') {
        opcionesDetalle.push(opcion);
        actualizarOpcionesMostradas();
        $('#preguntaOpcion').val("");
        autosize.update($('#preguntaOpciones'));
    }
});

function actualizarOpcionesMostradas() {
    var listaOpciones = opcionesDetalle.map(function (opcion, index) {
        return (index + 1) + '.- ' + opcion;
    }).join('\n'); // Unir las opciones con saltos de línea

    $('#preguntaOpciones').val(listaOpciones); // Usar .val() en lugar de .html()
    $('#preguntaOpciones').prop('disabled', true); // Deshabilitar el textarea después de actualizar
}
function restablecer() {
    console.log("Restableciendo campos...")
    // Restablecer los valores de los campos a sus valores iniciales
    $("#preguntaEnunciado").val('');
    $("#preguntaOpcion").val('');
    $("#preguntaOpciones").val('');
    $("#preguntaCorrecta").val('');
    opcionesDetalle = [];
    // Si estás usando el atributo 'disabled', habilita el campo de opciones

}