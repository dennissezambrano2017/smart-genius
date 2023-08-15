from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Unidad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Contenido(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion= models.TextField(blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Tema(models.Model):
    nombre = models.CharField(max_length=100)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Ejercicio(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    enunciado = models.TextField()
    opciones = models.JSONField()  # Almacena las opciones de respuesta como un JSON
    respuesta_correcta = models.IntegerField()  # Respuesta correcta en el campo 'opciones'
    def __str__(self):
        return f"{self.enunciado}"

def validate_pdf_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("El archivo debe ser un PDF.")

def validate_pdf_size(value):
    if value.size > 10 * 1024 * 1024:  # Límite de tamaño: 10 MB
        raise ValidationError("El tamaño máximo del archivo es 10 MB.")

class Material(models.Model):
    enlace = models.URLField()
    archivo_pdf = models.FileField(upload_to='pdfs/', validators=[validate_pdf_extension, validate_pdf_size],
                                   default='default.pdf')
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)  # Relación de uno a muchos con Tema
    ejercicios = models.ManyToManyField(Ejercicio)  # Relación muchos a muchos con Ejercicio

    def __str__(self):
        return f"Material - {self.tema.nombre}"


class Puntuacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2)