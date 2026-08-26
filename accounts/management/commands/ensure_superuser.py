import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Sincroniza un superuser a partir de las env vars
    DJANGO_SUPERUSER_*, pensado para correr como parte del
    build en hostings sin shell interactiva (como el free tier
    de Render).

    A propósito SIEMPRE actualiza la contraseña (y se asegura
    de que sea staff+superuser+activo) si el usuario ya existe:
    es la herramienta de "no puedo entrar", así que tiene que
    ganar lo que hay cargado en la env var en cada redeploy, no
    quedarse pegado a un intento anterior. Si las env vars no
    están seteadas, no falla el build: simplemente no hace nada.
    """

    help = (
        'Crea o sincroniza un superuser desde '
        'DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD. No hace nada '
        'si esas env vars no están seteadas.'
    )

    def handle(self, *args, **options):

        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', '')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:

            self.stdout.write(
                'DJANGO_SUPERUSER_USERNAME / PASSWORD no están '
                'seteadas, no se toca ningún superuser.'
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email},
        )

        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{username}" creado correctamente.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{username}" ya existía, '
                    f'contraseña sincronizada con la env var.'
                )
            )
