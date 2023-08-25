
var response;
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
                // Ajustar la ruta para que coincida con la estructura de carpetas
               //pdfurl = pdf.replace('/pdfs/pdfs/', '/pdfs/'); 

                //pdfViewer.setDocument(pdf);
                // Actualizar la URL del visor de PDF
                $('#pdfViewer').attr('src', pdf);
                $('#videoViewer').attr('src', 'https://www.youtube.com/embed/' + shortLink);
                escogerPreguntaAleatoria(data.preguntas)

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

let preguntas_aleatorias = true;
let mostrar_pantalla_juego_términado = true;
let reiniciar_puntos_al_reiniciar_el_juego = true;

let pregunta;
let posibles_respuestas;
btn_correspondiente = [
    $("#btn1"),
    $("#btn2"),
    $("#btn3"),
    $("#btn4")
];
let npreguntas = [];

let preguntas_hechas = 0;
let preguntas_correctas = 0;

function escogerPreguntaAleatoria(interprete_bp) {
    console.log(interprete_bp)
    let n;
    if (preguntas_aleatorias) {
        n = Math.floor(Math.random() * interprete_bp.length);
        console.log(n)
    } else {
        n = 0;
    }

    while (npreguntas.includes(n)) {
        n++;
        if (n >= interprete_bp.length) {
            n = 0;
        }
        if (npreguntas.length == interprete_bp.length) {
            if (mostrar_pantalla_juego_términado) {
                swal.fire({
                    title: "Juego finalizado",
                    text: "Puntuación: " + preguntas_correctas + "/" + (preguntas_hechas - 1),
                    icon: "success"
                });
            }
            if (reiniciar_puntos_al_reiniciar_el_juego) {
                preguntas_correctas = 0
                preguntas_hechas = 0
            }
                npreguntas = [];
        }
    }
    npreguntas.push(n);
    console.log(npreguntas)
    preguntas_hechas++;
    console.log(preguntas_hechas)

    escogerPregunta(interprete_bp, n);
}

function escogerPregunta(params, n) {
    pregunta = params[n];
    console.log(pregunta)
    $("#pregunta").html(pregunta.enunciado);
    $("#numero").html(n);
    let pc = preguntas_correctas;
    if (preguntas_hechas > 1) {
    $("#puntaje").html(pc + "/" + (preguntas_hechas - 1));
    } else {
    $("#puntaje").html("");
    }

    desordenarRespuestas(pregunta);
}

function desordenarRespuestas(pregunta) {
    console.log(pregunta)
    posibles_respuestas = [
        pregunta.opciones[0], //respuesta incorrecta
        pregunta.opciones[1], //respuesta incorrecta
        pregunta.opciones[2], //respuesta incorrecta
        pregunta.opciones[pregunta.resp_correcta] //respuesta correcta
    ];
    posibles_respuestas.sort(function () {
        return Math.random() - 0.5;
    });

    $("#btn1").html(posibles_respuestas[0]);
    $("#btn2").html(posibles_respuestas[1]);
    $("#btn3").html(posibles_respuestas[2]);
    $("#btn4").html(posibles_respuestas[3]);
}

let suspender_botones = false;

function oprimir_btn(i) {
    if (suspender_botones) {
        return;
    }
    suspender_botones = true;
    if (posibles_respuestas[i] == pregunta.opciones[pregunta.resp_correcta]) {
        preguntas_correctas++;
        btn_correspondiente[i].css("background", "lightgreen");
    } else {
        btn_correspondiente[i].css("background", "pink");
    }
    for (let j = 0; j < 4; j++) {
        if (posibles_respuestas[j] == pregunta.opciones[pregunta.resp_correcta]) {
            btn_correspondiente[j].css("background", "lightgreen");
            break;
        }
    }
    setTimeout(function () {
    reiniciar();
    suspender_botones = false;
    }, 3000);
}

// function reiniciar() {
//   for (const btn of btn_correspondiente) {
//     btn.css("background", "white");
//   }
//   escogerPreguntaAleatoria(preguntas);
// }