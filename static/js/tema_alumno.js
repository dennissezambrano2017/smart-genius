$(".btn-tema").click(function (e) { 
    e.preventDefault();
    var id_tema = $(this).attr('id');
    console.log("Button id: " + id_tema);
});

$(document).ready(function (e) { 
    $('.enlace').click(function() {
        // Desactivar la clase "active" en todos los enlaces
        $('.enlace').removeClass('active');

        // Activar la clase "active" en el enlace seleccionado
        $(this).addClass('active');
    });
});