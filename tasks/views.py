from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate,update_session_auth_hash
from django.db import IntegrityError
from .models import Unidad, Contenido, Material, Tema,Ejercicio
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import  JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet 
from reportlab.lib import colors
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
import json

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

@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST['contraseña']
        user = request.user

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Actualiza la sesión de autenticación

        return JsonResponse({'result': '1', 'message': 'Cambio de contraseña correctamente'})

    return JsonResponse({'result': '0', 'message': 'Error al modificar la contraseña, por favor intente nuevamente.'})

@login_required
def edit_usuario(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username_id=request.POST.get('usuario_id')
            nuevo_username  = request.POST.get('user')
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            email = request.POST.get('email')
            try:
                usuario = get_object_or_404(User, username=username_id)
                print(username_id,nuevo_username,nombres,apellidos,email)
                # Verifica si el usuario que se quiere editar es el mismo que el usuario autenticado
                if usuario == request.user:
                    # Comprobamos si el nuevo username está disponible
                    if nuevo_username != usuario.username and User.objects.filter(username=nuevo_username).exists():
                        return JsonResponse({'result': '0', 'message': 'El nombre de usuario ya está en uso.'})

                    # Si el nuevo username es diferente, actualizamos el username
                    if email != usuario.username:
                        usuario.username = email
                    usuario.first_name = nombres
                    usuario.last_name = apellidos
                    usuario.email = nuevo_username
                    usuario.save()
                    return JsonResponse({'result': '1'})
                else:
                    raise PermissionDenied("No tienes permisos para editar este usuario.")
            except Exception as e:
                return JsonResponse({'result': '0', 'message': str(e)})
        else:
            raise PermissionDenied("Debes estar autenticado para editar un usuario.")
@login_required
def get_user_data(request):
    if request.method == "GET" and "username" in request.GET:
        username = request.GET["username"]
        
        try:
            user = User.objects.get(username=username)
            user_data = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            return JsonResponse(user_data)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)
    else:
        return JsonResponse({'error': 'Petición inválida.'}, status=400)

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
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
            return JsonResponse({'result': '1', 'message': 'Se elimino correctamente'})
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
            contenido = Contenido(
                nombre=nombre, descripcion=descripcion, unidad=unidad)
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
                'contenido_id': contenido_id,
                'unidades': [{'id': unidad.id, 'nombre': unidad.nombre} for unidad in unidades],
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error en buscar la información del contenido'})


@login_required
def vwEditar_Contenido(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreContenidoMod')
        descripcion = request.POST.get('descripcionEdContenido')
        unidad_id = request.POST.get('selectModContenido')
        contenido_id = request.POST.get('txtIdContenido')
        print(nombre, descripcion, unidad_id)
        if not nombre:
            return JsonResponse({'result': '0', 'message': 'Por favor ingrese un nombre para el contenido.'})
        try:
            unidad = Unidad.objects.get(pk=unidad_id)
            contenido = Contenido.objects.get(pk=contenido_id)
            contenido.nombre = nombre
            contenido.descripcion = descripcion
            contenido.unidad = unidad
            contenido.save()
            return JsonResponse({'result': '1', 'message': 'El contenido se modificó exitosamente.'})
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
            return JsonResponse({'result': '1', 'message': 'Se elimino correctamente'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al eliminar el contenido, por favor intente nuevamente.'})

@login_required
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

@login_required
def vwObtener_Contenido(request):
    contenido = Contenido.objects.all().values('id', 'nombre')
    return JsonResponse(list(contenido), safe=False)


@login_required
def vwCreate_tema(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contenido_id = request.POST.get('contenido_id')
        print(nombre, contenido_id)
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
@login_required
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
                'tema_id': tema_id,
                'contenidos': [{'id': contenido.id, 'nombre': contenido.nombre} for contenido in contenidos],
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error en buscar la información del contenido'})

@login_required
def vwEditar_Tema(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreTemaModi')
        contenido_id = request.POST.get('selectRegisterTemaModi')
        tema_id = request.POST.get('txtIdTema')
        print(nombre, contenido_id, tema_id)
        if not nombre:
            return JsonResponse({'result': '0', 'message': 'Por favor ingrese un nombre para el tema.'})
        try:
            contenido = Contenido.objects.get(pk=contenido_id)
            tema = Tema.objects.get(pk=tema_id)
            tema.nombre = nombre
            tema.contenido = contenido
            tema.save()
            return JsonResponse({'result': '1', 'message': 'El tema se modificó exitosamente.'})
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
            return JsonResponse({'result': '1', 'message': 'Se elimino correctamente'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al modificar la unidad, por favor intente nuevamente.'})
@login_required
def vwMaterial(request):
    material_list = Material.objects.all().order_by('tema')  # Obtener todos los registros de unidades

    # Configuración del paginador para mostrar 5 unidades por página
    paginator = Paginator(material_list, 5)

    page = request.GET.get('page')  # Obtener el número de página de la URL

    try:
        material = paginator.page(page)
    except PageNotAnInteger:
        # Si el número de página no es un número, mostrar la primera página
        material = paginator.page(1)
    except EmptyPage:
        # Si el número de página está fuera de rango, mostrar la última página
        material = paginator.page(paginator.num_pages)
    # Encontrar los materiales que no tienen ejercicios relacionados
    materials_without_exercises = Material.objects.filter(ejercicio__isnull=True)

    return render(request, 'material.html', {'material': material, 'materials_without_exercises': materials_without_exercises})
@login_required
def vwGetMaterial_Tema(request):
    if request.method == 'GET':
        try:
            material_id = request.GET.get('idMaterial');
            material= Material.objects.get(pk=material_id);

            temas = Tema.objects.filter(material=material)
            temas_data = [{'id': tema.id, 'nombre': tema.nombre} for tema in temas]

            ejercicios = Ejercicio.objects.filter(material=material)
            ejercicio_data = [{'id': ejercicio.id, 'enunciado': ejercicio.enunciado} for ejercicio in ejercicios]
            data = {
                'result': '1',
                'material_id': material_id,
                'enlace': material.enlace,
                'pdf': material.archivo_pdf.url,
                'temas': temas_data,
                'ejercicios': ejercicio_data,
            }
            print(data)
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error en buscar la información del contenido'})
@login_required       
def vwGetMaterial_ejercicio(request):
    if request.method == 'GET':
        try:
            ejercicio_id = request.GET.get('ejercicioId');
            ejercicio = Ejercicio.objects.get(pk=ejercicio_id);  # Usa el modelo Ejercicio
            print(ejercicio_id)
            data = {
                'result': '1',
                'enunciado': ejercicio.enunciado,
                'opciones': ejercicio.opciones,
                'resp_correct': ejercicio.respuesta_correcta
            }
            print(data)
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error en buscar la información del contenido'})
@login_required
def vwObtener_Temas(request):
    temas_registrados = Material.objects.values_list('tema__id', flat=True)
    print(temas_registrados)
    temas_no_registrados = Tema.objects.exclude(id__in=temas_registrados).values('id', 'nombre')
    return JsonResponse(list(temas_no_registrados), safe=False)
@login_required
def vwCreate_material(request):
    if request.method == 'POST':
        enlace = request.POST.get('enlace')
        archivo = request.FILES.get('archivo_pdf')
        tema_id = request.POST.get('tema_id')
        if not enlace or not archivo or not tema_id:
            return JsonResponse({'result': 'error', 'message': 'Por favor ingrese todo los datos'})
        try:
            print('si')
            tema = Tema.objects.get(pk=tema_id)
            # Guardar el archivo en el modelo Material
            material = Material(enlace=enlace, tema=tema)
            material.archivo_pdf.save(archivo.name, ContentFile(archivo.read()), save=True)

            return JsonResponse({'result': 'success', 'message': 'Tema registrado exitosamente.'})
        except Exception as e:
            return JsonResponse({'result': 'error', 'message': 'Error en registrar contenido'}, status=400)
@login_required
def vwCreate_ejercicio(request):
    if request.method == 'POST':
        
        enunciado = request.POST.get('enunciado')
        opciones_json = request.POST.get('opciones')
        respuesta = request.POST.get('respuesta')
        material_id = request.POST.get('material_id')
        if not enunciado or not opciones_json or not respuesta:
            return JsonResponse({'result': 'error', 'message': 'Por favor ingrese los datos faltantes de la pregunta'})
        try:
            print(enunciado,opciones_json,respuesta,material_id)
            material = Material.objects.get(pk=material_id)
            opciones = json.loads(opciones_json)  # Deserializar la cadena JSON a un array Python

            ejercicio = Ejercicio(enunciado=enunciado, opciones=opciones, respuesta_correcta=respuesta, material=material)
            ejercicio.save()
            return JsonResponse({'result': 'success', 'message': 'Ejercicio registrado exitosamente.'})
        except Exception as e:
            return JsonResponse({'result': 'error', 'message': 'Error en registrar el ejercicio'}, status=400)
@login_required    
def vwEliminarEjercicio(request):
    if request.method == 'POST':
        try:
            unEjer = Ejercicio.objects.get(pk=request.POST['idEjercicio'])
            unEjer.delete()
            return JsonResponse({'result': '1', 'message': 'Se elimino correctamente'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al modificar la unidad, por favor intente nuevamente.'})
@login_required
def vwEliminarMaterial(request):
    if request.method == 'POST':
        try:
            unMaterial = Material.objects.get(pk=request.POST['idMaterial'])
            unMaterial.delete()
            return JsonResponse({'result': '1', 'message': 'Se elimino correctamente'})
        except Exception as e:
            return JsonResponse({'result': '0', 'message': 'Error al modificar la unidad, por favor intente nuevamente.'})
@login_required
def visualizar_reporte(request):
    busqueda_estudiante = request.GET.get('busqueda_estudiante')
    
    if busqueda_estudiante:
        usuarios_no_administradores = User.objects.filter(
            is_staff=False, username__icontains=busqueda_estudiante
        )
    else:
        usuarios_no_administradores = User.objects.filter(is_staff=False)
    
    paginator = Paginator(usuarios_no_administradores, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'reporte.html', {'page_obj': page_obj})

@login_required
def visualizar_contenido(request):
    unidades = Unidad.objects.all()
    contenidos = Contenido.objects.select_related('unidad').all()
    temas = Tema.objects.select_related('contenido__unidad').all()
    materiales = Material.objects.prefetch_related('tema').all()
    ejercicios = Ejercicio.objects.select_related('material').all()
    print(unidades,contenidos,temas,materiales,ejercicios)    
    context = {
        'unidades': unidades,
        'contenidos': contenidos,
        'temas': temas,
        'materiales': materiales,
        'ejercicios': ejercicios,
    }
    print(materiales)
    return render(request, 'contenido_material.html', context)

@login_required
def generar_unidad_pdf(request, unidad_id):
    unidad = Unidad.objects.get(pk=unidad_id)
    contenidos = Contenido.objects.filter(unidad=unidad)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{unidad.nombre}.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    story = []

    for contenido in contenidos:
        content_style = getSampleStyleSheet()["Heading1"]
        content_text = f"Contenido: {contenido.nombre}"
        content_paragraph = Paragraph(content_text, content_style)
        story.append(content_paragraph)
        
        content_style = getSampleStyleSheet()["Normal"]
        description_text = f"Descripción: {contenido.descripcion}"
        description_paragraph = Paragraph(description_text, content_style)
        story.append(description_paragraph)
        story.append(Spacer(1, 10))  # Add spacing

        temas = Tema.objects.filter(contenido=contenido)

        for tema in temas:
            story.append(Spacer(1, 10))  # Add spacing

            
            content_style = getSampleStyleSheet()["Title"]
            content_text = f"Tema: {tema.nombre}"
            content_paragraph = Paragraph(content_text, content_style)
            story.append(content_paragraph)

            tema_data = [f"Recursos"]
            data = [tema_data]

            material = Material.objects.filter(tema=tema).first()
            if material:
                enlace_data = [f"Enlace: {material.enlace}"]
                pdf_data = [f"Archivo PDF: {material.archivo_pdf.url}"]
                ejercicios_data = ["Ejercicios:"]
                ejercicios = Ejercicio.objects.filter(material=material)
                for ejercicio in ejercicios:
                    ejercicios_data.append(f"- {ejercicio.enunciado}")
                
                data.extend([enlace_data, pdf_data])
                ejercicios_data = "\n".join(ejercicios_data)
                data.append([ejercicios_data])

                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ]))
                story.append(table)

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response

def vwContenidoAlumno(request):
    contenidos = Contenido.objects.select_related('unidad').all()

    context = {
        'contenidos': contenidos
    }

    return render(request, 'contenido_alumno.html', context)

def vwTemaAlumno(request):
    id = request.POST.get('id')
    temas = Tema.objects.filter(contenido_id=id)
    materiales = Material.objects.prefetch_related('tema').all()
    ejercicios = Ejercicio.objects.select_related('tema').all()

    context = {
        'id_contenido': id,
        'temas': temas,
        'materiales': materiales,
        'ejercicios': ejercicios,
    }
    print(temas)

    return render(request, 'tema_alumno.html', context)

def vwPerfilAlumno(request):
    return render(request, 'perfil_alumno.html')

def vwAvanceAlumno(request):
    return render(request, 'avance_alumno.html')


