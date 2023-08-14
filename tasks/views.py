from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.db import IntegrityError
from .forms import UnidadForm


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
    
    # if request.method == 'GET':
        # usuarios_registrados = Usuario.objects.filter(tipo_usuario='Estudiante', estado_usuario='Activo')



    usuarios_registrados = User.objects.all()
    return render(request, 'reporte.html', {'usuarios_registrados': usuarios_registrados})