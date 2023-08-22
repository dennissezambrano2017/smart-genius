// cargarContenidos.js
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
function cargarEjercicios() {
  const materialSelect = document.getElementById("material-select");
  const ejercicioSelect = document.getElementById("ejercicio-select");

  const materialId = materialSelect.value;

  if (materialId) {
    fetch(`/obtener_ejercicios/?material_id=${materialId}`)
      .then((response) => response.json())
      .then((data) => {
        ejercicioSelect.innerHTML =
          "<option selected>Selecciona un ejercicio</option>";
        data.forEach((ejercicio) => {
          ejercicioSelect.innerHTML += `<option value="${ejercicio.id}">${ejercicio.enunciado}</option>`;
        });
      });
  } else {
    ejercicioSelect.innerHTML =
      "<option selected>Selecciona un ejercicio</option>";
  }
}
function cargarMateriales() {
  const temaSelect = document.getElementById("tema-select");
  const materialSelect = document.getElementById("material-select");

  const temaId = temaSelect.value;

  if (temaId) {
    fetch(`/obtener_materiales/?tema_id=${temaId}`)
      .then((response) => response.json())
      .then((data) => {
        materialSelect.innerHTML =
          "<option selected>Selecciona un material</option>";
        data.forEach((material) => {
          materialSelect.innerHTML += `<option value="${material.id}">${material.enlace}</option>`;
        });
      });
  } else {
    materialSelect.innerHTML =
      "<option selected>Selecciona un material</option>";
  }
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
