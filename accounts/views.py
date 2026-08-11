from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.contrib.auth import (
    authenticate,
    login,
    logout
)


def register_view(request):

    error_message = None

    if request.method == 'POST':

        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():

            error_message = 'El usuario ya existe.'

        elif User.objects.filter(email=email).exists():

            error_message = 'El email ya está registrado.'

        else:

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user)

            return redirect('home')

    return render(
        request,
        'accounts/register.html',
        {
            'error_message': error_message
        }
    )


def login_view(request):

    error_message = None

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        # Permite ingresar con el usuario o con el email,
        # por si el usuario no se acuerda cuál usó.
        if username and '@' in username:

            existing_user = User.objects.filter(
                email__iexact=username
            ).first()

            if existing_user:
                username = existing_user.username

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect('home')

        else:

            error_message = (
                'Usuario o contraseña incorrectos.'
            )

    return render(
        request,
        'accounts/login.html',
        {
            'error_message': error_message
        }
    )


def logout_view(request):

    logout(request)

    return redirect('home')