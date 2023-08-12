from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import UnidadForm
from .models import Unidad, Contenido, Material, Tema
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Register User
                user = User.objects.create_user(
                    username=request.POST['username'], email=request.POST['email'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('perfil')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Contraseña no coinciden'
        })


def profile(request):
    return render(request, 'profile.html')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    error = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('perfil')
            else:
                error = 'Usuario o Contraseña es incorrecto'
        else:
            error = 'Por favor, ingrese un nombre de usuario y contraseña válidos'
    else:
        form = AuthenticationForm()

    return render(request, 'signin.html', {
        'form': form,
        'error': error,
    })


def contenido(request):
    return render(request, 'contenido.html')


def inicio(request):
    return render(request, 'inicio.html')
# Vista que renderiza la plantilla que lista los unidades registrados

@login_required
def vwUnidad(request):
    
    if request.method == 'GET':
        try:
            unidades = Unidad.objects.all()  # Obtener todos los registros de unidades
            return render(request, 'create_unidad.html', {'unidad': unidades,
                                                          'btnUnidad': 'activado'})
        except Exception as e:
            return render(request, 'create_unidad.html', {'btnUnidad': 'activado'})


def create_unidad(request):
    if request.method == 'POST':
        try:
            unUnidad = Unidad()
            unUnidad.nombre = request.POST['nombre']
            unUnidad.save()
            return JsonResponse({'result': '1'})
        except Exception as e:
            return JsonResponse({'result': '0'})


# Vista que modifica los datos de un administrador
def edit_unidad(request):
    if request.method == 'POST':
        try:
            unUnidad = Unidad.objects.get(pk=request.POST['txtIdUnidad'])
            unUnidad.nombre = request.POST['txtEdUnidadNombre']
            unUnidad.save()
            messages.success(
                request, 'El administrador se modificó exitosamente.')
            return JsonResponse({'result': '1'})
        except Exception as e:
            return JsonResponse({'result': '0'})

# Vista que busca a los administradores de forma filtrada
def vwBuscarUnidad(request):
    if request.method == 'POST':
        try:
            buscarUnidad = request.POST['txtBuscarunidad']
            # Se obtienen los adminsitradores que si se pueden eliminar
            unidades_filtradas = Unidad.objects.filter(nombre__icontains=buscarUnidad)
            return render(request, 'administradores.html', {
                'unidades_filtradas': unidades_filtradas,
                'txtBuscarunidad': buscarUnidad,
                'btnBuscarunidad': 'activado'
            })
        except Exception as e:
            return redirect('unidad')


# Vista que obtiene un datos de un unidad mediante un id


def vwGetUnidad(request):
    if request.method == 'GET':
        try:
            idUnidad = request.GET['idUnidad']
            unUnidad = Unidad.objects.get(pk=idUnidad)
            return JsonResponse({'result': '1', 'nombre': unUnidad.nombre, 'id': unUnidad.pk})
        except Exception as e:
            return JsonResponse({'result': '0'})


def create_contenido(request):
    return render(request, 'create_contenido.html', {
        'form': UnidadForm
    })
