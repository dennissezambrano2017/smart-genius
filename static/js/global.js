// Función para mostrar un modal en función de los datos recibidos
function show_modal(md_titulo, md_mensaje, md_opcHeader, md_opcFooter) {
    $('#ventana_modal').modal({backdrop: 'static', keyboard: false})
    document.querySelector("#md_titulo").innerHTML = "<strong>" + md_titulo + "</strong>";
    document.querySelector("#md_mensaje").innerHTML = md_mensaje;
    document.querySelector("#md_opcHeader").innerHTML = md_opcHeader;
    document.querySelector("#md_opcFooter").innerHTML = md_opcFooter;
    $('#ventana_modal').modal('show');
}
// Función para crear una llave de seguridad "crsftoken" y poder realizar una petición ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}