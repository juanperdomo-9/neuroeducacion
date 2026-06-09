from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    short_description = models.TextField()

    thumbnail = models.ImageField(
        upload_to='courses/thumbnails/'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_published = models.BooleanField(
        default=True
    )

    is_free = models.BooleanField(
        default=False
    )

    resource_file = models.FileField(
        upload_to='resources/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Module(models.Model):

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules'
    )

    title = models.CharField(max_length=255)

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Lesson(models.Model):

    class Meta:
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    title = models.CharField(max_length=255)

    video_url = models.URLField()

    duration = models.CharField(
        max_length=50,
        blank=True
    )

    video_url = models.URLField(
        blank=True,
        null=True
    )

    content = models.TextField(
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(default=0)

    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Enrollment(models.Model):

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'

        unique_together = ('user', 'course')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    paid = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'
    

class LessonProgress(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )

    completed = models.BooleanField(
        default=False
    )

    completed_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        unique_together = (
            'user',
            'lesson'
        )

    def __str__(self):

        return f'{self.user} - {self.lesson}'
    
class Compra(models.Model):

    METODOS_PAGO = (

        ('mp', 'MercadoPago'),

        ('transferencia', 'Transferencia'),

    )

    ESTADOS = (

        ('pendiente', 'Pendiente'),

        ('aprobado', 'Aprobado'),

    )

    curso = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    nombre = models.CharField(
        max_length=255
    )

    apellido = models.CharField(
        max_length=255
    )

    dni = models.CharField(
        max_length=30
    )

    email = models.EmailField()

    metodo_pago = models.CharField(
        max_length=30,
        choices=METODOS_PAGO
    )

    estado = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default='pendiente'
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f'{self.nombre} - {self.curso.title}'