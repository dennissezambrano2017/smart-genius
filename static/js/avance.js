function cargarContenidos() {
  const unidadSelect = document.getElementById("unidad-select");
  const contenidoSelect = document.getElementById("contenido-select");

  const unidadId = unidadSelect.value;

  if (unidadId) {
    fetch(`/obtener_contenidos/?unidad_id=${unidadId}`)
      .then((response) => response.json())
      .then((data) => {
        contenidoSelect.innerHTML =
          "<option selected>Selecciona un contenido</option>";
        data.forEach((contenido) => {
          contenidoSelect.innerHTML += `<option value="${contenido.id}">${contenido.nombre}</option>`;
        });
      });
  } else {
    contenidoSelect.innerHTML =
      "<option selected>Selecciona un contenido</option>";
  }
}

function cargarTemas() {
  const contenidoSelect = document.getElementById("contenido-select");
  const temaSelect = document.getElementById("tema-select");

  const contenidoId = contenidoSelect.value;

  if (contenidoId) {
    fetch(`/obtener_temas_contenido/?contenido_id=${contenidoId}`)
      .then((response) => response.json())
      .then((data) => {
        temaSelect.innerHTML = "<option selected>Selecciona un tema</option>";
        data.forEach((tema) => {
          temaSelect.innerHTML += `<option value="${tema.id}">${tema.nombre}</option>`;
        });
      });
  } else {
    temaSelect.innerHTML = "<option selected>Selecciona un tema</option>";
  }
}
function cargarMateriales() {
  const ejercicioSelect = document.getElementById("ejercicio-select");
  const temaSelect = document.getElementById("tema-select");
  const temaId = temaSelect.value;
  fetch(`/obtener_materiales/?tema_id=${temaId}`)
    .then(async (response) => await response.json())
    .then(async (data) => {
      data.forEach((material) => {
        if (material.id) {
          return fetch(`/obtener_ejercicios/?material_id=${material.id}`)
            .then((response) => response.json())
            .then((data) => {
              let optionsHTML =
                "<option selected>Selecciona un ejercicio</option>";
              data.forEach((ejercicio) => {
                optionsHTML += `<option value="${ejercicio.id}">${ejercicio.enunciado}</option>`;
              });
              ejercicioSelect.innerHTML = optionsHTML;
            });
        }
      });
    });
}

function filtrarPuntuacion() {
  const ejercicioSelect = document.getElementById("ejercicio-select");
  const ejercicioId = ejercicioSelect.value;
  if (ejercicioId > 0) {
    const url = `/visualizar_puntuacion_filtrada/?ejercicio_id=${ejercicioId}`;
    window.location.href = url;
  } else {
    ejercicioId = 0;
    const url = `/visualizar_puntuacion_filtrada/?ejercicio_id=${ejercicioId}`;
    window.location.href = url;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const btnsViewMaterial = document.querySelectorAll(
    "#btn_visualizar_ejercicio"
  );
  btnsViewMaterial.forEach((btn) => {
    btn.addEventListener("click", function () {
      const vid = this.getAttribute("data-vid");
      visualizarPuntuacion(vid);
    });
  });
});

function visualizarPuntuacion(idPuntuacion) {
  fetch(`/visualizar_ejercicio_user/?ejercicio_id=${idPuntuacion}`)
    .then(async (response) => await response.json())
    .then(async (data) => {
      const ejercicio = data[0];

      document.getElementById("enunciado").value = ejercicio.enunciado;

      const opcionesInput = document.getElementById("opciones");
      opcionesInput.value = ejercicio.opciones.join(", "); // Unimos las opciones en un string

      const respuestaInput = document.getElementById("respuesta");
      const respuestaSeleccionada = ejercicio.respuesta_correcta;
      respuestaInput.value = ejercicio.opciones[respuestaSeleccionada - 1];

      const modal = new bootstrap.Modal(
        document.getElementById("modalView-material")
      );
      modal.show();
    });
}
