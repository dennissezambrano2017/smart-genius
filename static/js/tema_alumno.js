$(".btn-tema").click(function (e) { 
    e.preventDefault();
    var id_tema = $(this).attr('id');
    $.ajax({
        type: 'GET',
        url: '/getcontenido_alumno/',
        data: { tema_id: id_tema },  // Reemplaza tu_id_de_tema con el ID de tema deseado
        dataType: 'json',
        success: function (data) {
            if (data.result === '1') {
                var enlace = data.enlace;
                var pdf = data.pdf;
                var preguntas = data.preguntas;
                // Ajustar la ruta para que coincida con la estructura de carpetas
               //pdfurl = pdf.replace('/pdfs/pdfs/', '/pdfs/'); 

               //pdfViewer.setDocument(pdf);
                // Actualizar la URL del visor de PDF
                $('#pdfViewer').attr('src', pdf);
                $('#youView').attr('src', enlace);
                console.log(enlace,pdf,preguntas);
            } else {
                console.log('Material no encontrado para el tema dado');
            }
        },
        error: function () {
            console.log('Error en la solicitud AJAX');
        }
    });
    
});

$(document).ready(function (e) { 
    $('.enlace').click(function() {
        // Desactivar la clase "active" en todos los enlaces
        $('.enlace').removeClass('active');

        // Activar la clase "active" en el enlace seleccionado
        $(this).addClass('active');
    });
});