from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import UnidadForm
from .models import Unidad, Contenido, Material, Tema
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


def inicio(request):
    return render(request, 'inicio.html')
# Vista que renderiza la plantilla que lista los unidades registrados


@login_required
def vwUnidad(request):
    unidades_list = Unidad.objects.all()  # Obtener todos los registros de unidades

    # Configuración del paginador para mostrar 5 unidades por página
    paginator = Paginator(unidades_list, 5)

    page = request.GET.get('page')  # Obtener el número de página de la URL

    try:
        unidades = paginator.page(page)
    except PageNotAnInteger:
        # Si el número de página no es un número, mostrar la primera página
        unidades = paginator.page(1)
    except EmptyPage:
        # Si el número de página está fuera de rango, mostrar la última página
        unidades = paginator.page(paginator.num_pages)

    return render(request, 'create_unidad.html', {'unidad': unidades, 'btnUnidad': 'activado'})


def create_unidad(request):
    if request.method == 'POST':
        nombre_unidad = request.POST.get('nombre')
        if not nombre_unidad:
            return JsonResponse({'result': '0', 'message': 'Por favor ingrese un nombre para la unidad.'})
        try:
            unUnidad = Unidad()
            unUnidad.nombre = request.POST['nombre']
            unUnidad.save()
            return JsonResponse({'result': '1'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al modificar la unidad, por favor intente nuevamente.'})

# Vista que modifica los datos de un administrador


def edit_unidad(request):
    if request.method == 'POST':
        nombre_unidad = request.POST.get('txtEdUnidadNombre')
        if not nombre_unidad:
            return JsonResponse({'result': '0', 'message': 'Por favor ingrese un nombre para la unidad.'})
        try:
            unUnidad = Unidad.objects.get(pk=request.POST['txtIdUnidad'])
            unUnidad.nombre = request.POST['txtEdUnidadNombre']
            unUnidad.save()
            messages.success(
                request, 'El administrador se modificó exitosamente.')
            return JsonResponse({'result': '1'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al modificar la unidad, por favor intente nuevamente.'})

# Vista que busca a los administradores de forma filtrada


def vwBuscarUnidad(request):
    if request.method == 'POST':
        try:
            buscarUnidad = request.POST['txtBuscarunidad']
            unidades_filtradas = Unidad.objects.filter(
                nombre__icontains=buscarUnidad)
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

# Vista que eliminar una unidad mediante un id


def vwEliminarUnidad(request):
    if request.method == 'POST':
        try:
            unUnidad = Unidad.objects.get(pk=request.POST['idUnidad'])
            unUnidad.delete()
            return JsonResponse({'result': '1'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al modificar la unidad, por favor intente nuevamente.'})


def vwcontenido(request):
    # Obtener todos los registros de unidades
    contenido_list = Contenido.objects.all()

    # Configuración del paginador para mostrar 5 unidades por página
    paginator = Paginator(contenido_list, 5)

    page = request.GET.get('page')  # Obtener el número de página de la URL

    try:
        contenido = paginator.page(page)
    except PageNotAnInteger:
        # Si el número de página no es un número, mostrar la primera página
        contenido = paginator.page(1)
    except EmptyPage:
        # Si el número de página está fuera de rango, mostrar la última página
        contenido = paginator.page(paginator.num_pages)

    return render(request, 'create_contenido.html', {'contenido': contenido, 'btnContenido': 'activado'})


def vwObtener_Unidad(request):
    unidades = Unidad.objects.all().values('id', 'nombre')
    return JsonResponse(list(unidades), safe=False)


def create_contenido(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        unidad_id = request.POST.get('unidad_id')
        
        unidad = Unidad.objects.get(pk=unidad_id)
        
        contenido = Contenido(nombre=nombre, descripcion=descripcion, unidad=unidad)
        contenido.save()
        
        return JsonResponse({'result': 'success', 'message': 'Contenido registrado exitosamente.'})
    
    return JsonResponse({'result': 'error', 'message': 'Error en registrar contenido'}, status=400)
