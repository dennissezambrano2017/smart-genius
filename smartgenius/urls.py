"""
URL configuration for smartgenius project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='Registro'),
    path('profile/', views.profile, name='perfil'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('inicio/', views.inicio, name='inicio'),

    # Sección unidad
    path('unidad/', views.vwUnidad, name='unidad'),
    path('create_unidad/', views.create_unidad, name='create_unidad'),
    path('edit_unidad/', views.edit_unidad, name='editar_unidad'),
    path('obtener_unidad/', views.vwGetUnidad, name='obtener_unidad'),
    path('buscar_unidad/', views.vwBuscarUnidad, name='buscar_unidad'),
    path('eliminar_unidad/', views.vwEliminarUnidad, name='eliminar_unidad'),

    # Sección contenido
    path('contenido/', views.vwcontenido, name='contenido'),
    path('obtener_unidades/', views.vwObtener_Unidad, name='unidad_contenido'),
    path('create_contenido/', views.create_contenido, name='create_contenido'),
    path('unidad_seleccionada/', views.vwGetUnidad_Contenido, name='unidad_seleccionada'),
    path('edit_contenido/', views.vwEditar_Contenido, name='editar_contenido'),
    path('eliminar_contenido/', views.vwEliminarContenido, name='eliminar_contenido'),

    # Sección contenido
    path('temas/', views.vwTemas, name='temas'),
    path('obtener_contenido/', views.vwObtener_Contenido, name='contenido_tema'),
    path('create_tema/', views.vwCreate_tema, name='create_tema'),
    path('contenido_seleccionada/', views.vwGetContenido_Tema, name='contenido_seleccionada'),
    path('edit_tema/', views.vwEditar_Tema, name='editar_tema'),
    path('eliminar_tema/', views.vwEliminarTema, name='eliminar_tema'),

    # Sección contenido - Alumno
    path('contenido_alumno/', views.vwContenidoAlumno, name='contenido_alu'),
    # Sección material
    path('material/', views.vwMaterial, name='material'),

    # Sección reportes
    path('inicio/create/', views.create_unidad, name='create_unidad'),
    path('reporte/', views.visualizar_reporte, name='visualizar_reporte'),
    path('aula/', views.visualizar_contenido, name='aula_documento'),
    path('imprimir_unidad/<int:unidad_id>/', views.generar_unidad_pdf, name='imprimir_unidad'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
