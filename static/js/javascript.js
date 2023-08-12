// sobrescritura del submit del formulario registrar unidad
$(document).on('submit', '#formRgUnidad', function (e) {
    var data = new FormData(this);
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/create_unidad/',
        data: data,
        contentType: false,
        processData: false,
    }).done(function (d) {
        if (d.result === '1') {
            $("#nombre").val("");
            $("#modalRegister-Unidad").modal('hide');
            show_modal("Mensaje informativo", "Unidad registrado exitosamente.", '<a class="close" href="/unidad/"><span aria-hidden="true">&times;</span></a>', '<a class="btn btn-sm btn-primary text-white" href="/unidad/">Aceptar</a>');
        }else{
            show_modal("Mensaje informativo", "Error al registrar la unidad, por favor intente nuevamente.", '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>', '<button type="button" class="btn btn-sm btn-primary text-white" data-dismiss="modal">Aceptar</button>');
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        show_modal("Mensaje informativo", "Error al registrar la unidad, por favor intente nuevamente.", '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>', '<button type="button" class="btn btn-sm btn-primary text-white" data-dismiss="modal">Aceptar</button>');
    }).always(function (data) {
    });
});

$(".btnObtenerUnidad").click(function () {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/obtener_unidad/',  // Asegúrate de tener la URL correcta para obtener la unidad
        type: 'GET',
        data: {
            "idUnidad": $(this).attr("vid"),
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json',
    }).done(function (d) {
        if (d.result == '1') {
            $("#txtEdUnidadNombre").val(d.nombre);  // Ajusta el selector para el campo de nombre
            $("#txtIdUnidad").val(d.id);  // Ajusta el selector para el campo de ID de unidad
        } else {
            show_modal("Mensaje informativo", 
            "Error al obtener la unidad, por favor intente nuevamente.", 
            '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>', 
            '<button type="button" class="btn btn-sm btn-primary text-white" data-dismiss="modal">Aceptar</button>');
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
    }).always(function (data) {
    });
});


// sobrescritura del submit del formulario modificar administrador
$(document).on('submit', '#formModUnidad', function (e) {
    console.log('si');
    var data = new FormData(this);
    console.log('data');
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/edit_unidad/',
        data: data,
        contentType: false,
        processData: false,
    }).done(function (d) {
        if (d.result === '1') {
            $("#modalEdit-Unidad").modal('hide');
            window.location.reload();
        }else{
            show_modal("Mensaje informativo", "Error al modificar la unidad, por favor intente nuevamente.", '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>', '<button type="button" class="btn btn-sm btn-primary text-white" data-dismiss="modal">Aceptar</button>');
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        show_modal("Mensaje informativo", "Error al modificar la, por favor intente nuevamente.", '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>', '<button type="button" class="btn btn-sm btn-primary text-white" data-dismiss="modal">Aceptar</button>');
    }).always(function (data) {
    });
});