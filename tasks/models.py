from django.db import models
from django.contrib.auth.models import User

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


class Material(models.Model):
    TIPOS_MATERIAL = [
        ('Video', 'Video'),
        ('Archivo', 'Archivo'),
        ('Presentación', 'Presentación'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS_MATERIAL)
    enlace = models.URLField()
    contenido_material = models.TextField()  # Aquí se almacena el contenido del material

    temas = models.ManyToManyField(Tema)  # Relación muchos a muchos con Tema
    def __str__(self):
        return f"{self.tipo} - {self.enlace}"


class Practica(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    fecha_practica = models.DateTimeField()
    puntaje = models.IntegerField()

    def __str__(self):
        return f"Práctica del estudiante: {self.estudiante} - Puntaje: {self.puntaje}"