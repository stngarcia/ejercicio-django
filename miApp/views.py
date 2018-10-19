from django.shortcuts import render, redirect
from .forms import AgregarUsuario, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('gestionUsuario')
    else:
        return redirect('login')


@login_required(login_url='login')
def gestionUsuario(request):
    usuarios = User.objects.all()
    paginator = Paginator(usuarios, 5)
    page = request.GET.get('page')
    usersPaginator = paginator.get_page(page)
    form = AgregarUsuario(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        u = User.objects.create_user(
            data.get("username"), data.get("correo"), data.get("password"))
        u.save()
        enviarCorreo(data.get("username"), data.get("correo"))
    form = AgregarUsuario()
    return render(request, "gestion-usuario.html", {'form': form, 'usuarios': usersPaginator})


def ingresar(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data.get("username"),
                            password=data.get("password"))
        if user is not None:
            login(request, user)
            return redirect('gestionUsuario')
    return render(request, "login.html", {'form': form})


def enviarCorreo(usuario, email):
    send_mail(
        'Ejercicio con django',
        'Weeeeeena po ' + usuario + '!!! Te has registrado en el ejercicio de django.',
        'stngarcia8@gmail.com',
        [email],
    )


def salir(request):
    logout(request)
    return redirect("/")


def cambiarPassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Clave actualizada!')
            return redirect("/login")
        else:
            messages.error(request, 'No fue posible cambiar su password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "CambiarPassword.html", {
        'form': form
    })
