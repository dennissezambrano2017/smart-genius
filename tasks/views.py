from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.db import IntegrityError
from .forms import UnidadForm
from .models import Unidad, Contenido,Tema,Material
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# Create your views here.
def home (request):
    return render(request, 'home.html')
def signup (request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Register User
                user= User.objects.create_user(username=request.POST['username'],email=request.POST['email'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('perfil')
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error':'El usuario ya existe'
                })
        return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error':'Contraseña no coinciden'
        })
def profile (request):
    return render(request,'profile.html')
def signout (request):
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
def contenido (request):
    return render(request, 'contenido.html')
def inicio (request):
    return render(request, 'inicio.html')
def create_unidad (request):
    return render(request, 'create_unidad.html',{
        'form':UnidadForm
    })
def visualizar_reporte(request):
    busqueda_estudiante = request.GET.get('busqueda_estudiante')
    if busqueda_estudiante:
        usuarios_registrados = User.objects.filter(username__icontains=busqueda_estudiante)
    else:
        usuarios_registrados = User.objects.all()
    return render(request, 'reporte.html', {'usuarios_registrados': usuarios_registrados})


def visualizar_contenido(request):
    unidades = Unidad.objects.all()
    contenidos = Contenido.objects.select_related('unidad').all()
    temas = Tema.objects.select_related('contenido__unidad').all()
    materiales = Material.objects.prefetch_related('temas').all()

    context = {
        'unidades': unidades,
        'contenidos': contenidos,
        'temas': temas,
        'materiales': materiales,
    }

    return render(request, 'contenido_material.html',context)



def generar_unidad_pdf(request, unidad_id):
    unidad = Unidad.objects.get(pk=unidad_id)
    contenidos = Contenido.objects.filter(unidad=unidad)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{unidad.nombre}.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    story = []

    # Title
    title_style = getSampleStyleSheet()["Title"]
    title_text = f"Unidad: {unidad.nombre}"
    title_paragraph = Paragraph(title_text, title_style)
    story.append(title_paragraph)
    story.append(Spacer(1, 20))  # Add spacing

    for contenido in contenidos:
        # Content Header
        content_style = getSampleStyleSheet()["Heading1"]
        content_text = f"Contenido: {contenido.nombre}"
        content_paragraph = Paragraph(content_text, content_style)
        story.append(content_paragraph)
        story.append(Spacer(1, 10))  # Add spacing

        temas = Tema.objects.filter(contenido=contenido)
        data = []

        for tema in temas:
            tema_data = [f"Tema: {tema.nombre}"]
            data.append(tema_data)

            materiales = Material.objects.filter(temas=tema)
            for material in materiales:
                material_data = [ f"Material: {material.tipo} - {material.enlace}"]
                data.append(material_data)

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))  # Add spacing

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response

   
        