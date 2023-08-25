
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
                var shortLink=enlace.substring(32);
                var pdf = data.pdf;
                dataPregunta = data.preguntas;
                
                // Ajustar la ruta para que coincida con la estructura de carpetas
               //pdfurl = pdf.replace('/pdfs/pdfs/', '/pdfs/'); 

                //pdfViewer.setDocument(pdf);
                // Actualizar la URL del visor de PDF
                $('#pdfViewer').attr('src', pdf);
                $('#videoViewer').attr('src', 'https://www.youtube.com/embed/' + shortLink);
            } else {
                console.log('Material no encontrado para el tema dado');
            }
        },
        error: function () {
            console.log('Error en la solicitud AJAX');
        }
    });

    // Colocar el nombre del tema
    var name_tema = $(this).text();
    $('#viewText').empty();
    $('#viewText').append("<h4 style='font-weight: bold; color: #fdb128;'>" + name_tema + "</h4>");
});

