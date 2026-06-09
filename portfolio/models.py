from django.db import models
from django.utils.text import slugify


class Proyecto(models.Model):

    titulo = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    imagen = models.ImageField(
        upload_to='proyectos/',
        blank=True,
        null=True
    )

    descripcion_corta = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    tecnologias = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    link_demo = models.URLField(
        blank=True,
        null=True
    )

    link_github = models.URLField(
        blank=True,
        null=True
    )

    destacado = models.BooleanField(
        default=False
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ['-creado']

    def __str__(self):

        return self.titulo
    
    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(
                self.titulo
            )

        super().save(*args, **kwargs)