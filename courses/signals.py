from django.db.models.signals import post_save

from django.dispatch import receiver

from .models import (
    Compra,
    Enrollment
)


@receiver(post_save, sender=Compra)
def aprobar_compra(sender, instance, **kwargs):

    if instance.estado == 'aprobado':

        Enrollment.objects.get_or_create(

            user=instance.usuario,

            course=instance.curso,

            defaults={
                'paid': True
            }
        )