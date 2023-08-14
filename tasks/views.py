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

@login_required
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
@login_required
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
@login_required
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
@login_required
def vwGetUnidad(request):
    if request.method == 'GET':
        try:
            idUnidad = request.GET['idUnidad']
            unUnidad = Unidad.objects.get(pk=idUnidad)
            return JsonResponse({'result': '1', 'nombre': unUnidad.nombre, 'id': unUnidad.pk})
        except Exception as e:
            return JsonResponse({'result': '0'})

# Vista que eliminar una unidad mediante un id
@login_required
def vwEliminarUnidad(request):
    if request.method == 'POST':
        try:
            unUnidad = Unidad.objects.get(pk=request.POST['idUnidad'])
            unUnidad.delete()
            return JsonResponse({'result': '1','message': 'Se elimino correctamente'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al modificar la unidad, por favor intente nuevamente.'})

@login_required
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

@login_required
def vwObtener_Unidad(request):
    unidades = Unidad.objects.all().values('id', 'nombre')
    return JsonResponse(list(unidades), safe=False)

@login_required
def create_contenido(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        unidad_id = request.POST.get('unidad_id')

        if not nombre or not unidad_id:
            return JsonResponse({'result': 'error', 'message': 'Por favor ingrese un nombre para el contenido'})
        try:
            unidad = Unidad.objects.get(pk=unidad_id)
            contenido = Contenido(nombre=nombre, descripcion=descripcion, unidad=unidad)
            contenido.save()
            return JsonResponse({'result': 'success', 'message': 'Contenido registrado exitosamente.'})
        except Exception as e:
                return JsonResponse({'result': 'error', 'message': 'Error en registrar contenido'}, status=400)

# Vista que obtiene un datos de un unidad mediante un id
@login_required
def vwGetUnidad_Contenido(request):
    if request.method == 'GET':
        try:
            contenido_id = request.GET.get('idContenido')
            
            contenido = Contenido.objects.get(pk=contenido_id)
            unidades = Unidad.objects.all()
            data = {
                'result': '1',
                'nombre': contenido.nombre,
                'descripcion': contenido.descripcion,
                'unidad_id': contenido.unidad_id,
                'contenido_id':contenido_id,
                'unidades': [{'id': unidad.id, 'nombre': unidad.nombre} for unidad in unidades],
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'result': '0','message': 'Error en buscar la información del contenido'})

@login_required       
def vwEditar_Contenido (request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreContenidoMod')
        descripcion = request.POST.get('descripcionEdContenido')
        unidad_id = request.POST.get('selectModContenido')
        contenido_id = request.POST.get('txtIdContenido')
        print(nombre,descripcion,unidad_id)
        if not nombre:
            return JsonResponse({'result': '0', 'message': 'Por favor ingrese un nombre para el contenido.'})
        try:
            unidad = Unidad.objects.get(pk=unidad_id)
            contenido = Contenido.objects.get(pk=contenido_id)
            contenido.nombre = nombre
            contenido.descripcion = descripcion
            contenido.unidad = unidad
            contenido.save()
            return JsonResponse({'result': '1','message':'El contenido se modificó exitosamente.'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al modificar el contenido, por favor intente nuevamente.'})
    else:
        # Si no es una solicitud POST, puedes manejarlo de acuerdo a tus necesidades
        return JsonResponse({'result': '0', 'message': 'Método no permitido.'})

@login_required
def vwEliminarContenido(request):
    if request.method == 'POST':
        try:
            unContenido = Contenido.objects.get(pk=request.POST['idContenido'])
            unContenido.delete()
            return JsonResponse({'result': '1','message': 'Se elimino correctamente'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al eliminar el contenido, por favor intente nuevamente.'})
        
def vwTemas(request):
    tema_list = Tema.objects.all()  # Obtener todos los registros de unidades

    # Configuración del paginador para mostrar 5 unidades por página
    paginator = Paginator(tema_list, 5)

    page = request.GET.get('page')  # Obtener el número de página de la URL

    try:
        temas = paginator.page(page)
    except PageNotAnInteger:
        # Si el número de página no es un número, mostrar la primera página
        temas = paginator.page(1)
    except EmptyPage:
        # Si el número de página está fuera de rango, mostrar la última página
        temas = paginator.page(paginator.num_pages)

    return render(request, 'temas.html', {'temas': temas, 'btnUnidad': 'activado'})

def vwObtener_Contenido(request):
    contenido = Contenido.objects.all().values('id', 'nombre')
    return JsonResponse(list(contenido), safe=False)

@login_required
def vwCreate_tema(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contenido_id = request.POST.get('contenido_id')
        print(nombre,contenido_id)
        if not nombre or not contenido_id:
            return JsonResponse({'result': 'error', 'message': 'Por favor ingrese un nombre para el tema'})
        try:
            print('si')
            contenido = Contenido.objects.get(pk=contenido_id)
            tema = Tema(nombre=nombre, contenido=contenido)
            tema.save()
            return JsonResponse({'result': 'success', 'message': 'Tema registrado exitosamente.'})
        except Exception as e:
                return JsonResponse({'result': 'error', 'message': 'Error en registrar contenido'}, status=400)
        
def vwGetContenido_Tema(request):
    if request.method == 'GET':
        try:
            tema_id = request.GET.get('idTema')
           
            tema = Tema.objects.get(pk=tema_id)
            contenidos = Contenido.objects.all()
            data = {
                'result': '1',
                'nombre': tema.nombre,
                'contenido_id': tema.contenido_id,
                'tema_id':tema_id,
                'contenidos': [{'id': contenido.id, 'nombre': contenido.nombre} for contenido in contenidos],
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'result': '0','message': 'Error en buscar la información del contenido'})
        
def vwEditar_Tema(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreTemaModi')
        contenido_id = request.POST.get('selectRegisterTemaModi')
        tema_id = request.POST.get('txtIdTema')
        print(nombre,contenido_id,tema_id)
        if not nombre:
            return JsonResponse({'result': '0', 'message': 'Por favor ingrese un nombre para el tema.'})
        try:
            contenido = Contenido.objects.get(pk=contenido_id)
            tema = Tema.objects.get(pk=tema_id)
            tema.nombre = nombre
            tema.contenido = contenido
            tema.save()
            return JsonResponse({'result': '1','message':'El tema se modificó exitosamente.'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al modificar el tema, por favor intente nuevamente.'})
    else:
        # Si no es una solicitud POST, puedes manejarlo de acuerdo a tus necesidades
        return JsonResponse({'result': '0', 'message': 'Método no permitido.'})
    
@login_required
def vwEliminarTema(request):
    if request.method == 'POST':
        try:
            unTema = Tema.objects.get(pk=request.POST['idTema'])
            unTema.delete()
            return JsonResponse({'result': '1','message': 'Se elimino correctamente'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al modificar la unidad, por favor intente nuevamente.'})
    

        




