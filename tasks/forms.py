from django.forms import ModelForm
from .models import Unidad,Contenido,Tema,Material

class UnidadForm(ModelForm):
    class Meta:
        model = Unidad
        fields = ['nombre']
