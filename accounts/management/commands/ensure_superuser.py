import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Crea un superuser a partir de las env vars DJANGO_SUPERUSER_*,
    pensado para correr como parte del build en hostings sin
    shell interactiva (como el free tier de Render).

    Es idempotente a propósito: si el usuario ya existe, no hace
    nada (no falla el build, no pisa la contraseña de un usuario
    que ya armaste a mano). Si las env vars no están seteadas,
    tampoco falla el build: simplemente no crea nada.
    """

    help = (
        'Crea un superuser desde DJANGO_SUPERUSER_USERNAME/'
        'EMAIL/PASSWORD si no existe todavía. No hace nada si '
        'esas env vars no están seteadas o si el usuario ya existe.'
    )

    def handle(self, *args, **options):

        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', '')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:

            self.stdout.write(
                'DJANGO_SUPERUSER_USERNAME / PASSWORD no están '
                'seteadas, no se crea ningún superuser.'
            )
            return

        if User.objects.filter(username=username).exists():

            self.stdout.write(
                f'El usuario "{username}" ya existe, no se toca.'
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Superuser "{username}" creado correctamente.'
            )
        )
