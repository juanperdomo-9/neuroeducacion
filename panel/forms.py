from django import forms

from courses.models import Course, Enrollment, Lesson, Module


INPUT_CLASSES = (
    'h-12 w-full rounded-xl border border-white/10 bg-white/5 '
    'px-4 text-sm text-white outline-none transition-all '
    'placeholder:text-white/30 focus:border-[#E93CAC]/40 '
    'focus:bg-white/[0.08] focus:ring-2 focus:ring-[#E93CAC]/20'
)

TEXTAREA_CLASSES = INPUT_CLASSES + ' h-auto min-h-[120px] py-3 resize-y'

CHECKBOX_CLASSES = (
    'h-5 w-5 rounded border-white/20 bg-white/5 '
    'text-[#E93CAC] focus:ring-[#E93CAC]/40'
)

FILE_CLASSES = (
    'w-full rounded-xl border border-dashed border-white/15 '
    'bg-white/5 px-4 py-3 text-sm text-white/70 '
    'file:mr-4 file:rounded-lg file:border-0 file:bg-[#E93CAC] '
    'file:px-4 file:py-2 file:text-xs file:font-medium '
    'file:text-white'
)

SELECT_CLASSES = INPUT_CLASSES


class StyledFormMixin:
    """
    Le pone clases Tailwind a cada widget según su tipo, para no
    repetir attrs={'class': ...} campo por campo en cada form.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = CHECKBOX_CLASSES

            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs['class'] = FILE_CLASSES

            elif isinstance(widget, forms.Textarea):
                widget.attrs['class'] = TEXTAREA_CLASSES

            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs['class'] = SELECT_CLASSES

            else:
                widget.attrs['class'] = INPUT_CLASSES


class CourseForm(StyledFormMixin, forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            'title', 'slug', 'short_description', 'thumbnail',
            'resource_file', 'price', 'is_free', 'is_published',
        ]
        labels = {
            'title': 'Título',
            'slug': 'Slug (URL)',
            'short_description': 'Descripción corta',
            'thumbnail': 'Imagen de portada',
            'resource_file': 'Archivo descargable (opcional)',
            'price': 'Precio',
            'is_free': 'Es gratuito',
            'is_published': 'Publicado',
        }


class ModuleForm(StyledFormMixin, forms.ModelForm):

    class Meta:
        model = Module
        fields = ['title', 'order']
        labels = {
            'title': 'Título del módulo',
            'order': 'Orden',
        }


class LessonForm(StyledFormMixin, forms.ModelForm):

    class Meta:
        model = Lesson
        fields = [
            'title', 'video_url', 'duration', 'content',
            'attachment', 'order', 'is_preview',
        ]
        labels = {
            'title': 'Título de la lección',
            'video_url': 'URL del video',
            'duration': 'Duración',
            'content': 'Contenido / notas',
            'attachment': 'Archivo de la clase (PDF, ejercicios, etc.)',
            'order': 'Orden',
            'is_preview': 'Vista previa gratuita',
        }


class EnrollmentForm(StyledFormMixin, forms.ModelForm):

    class Meta:
        model = Enrollment
        fields = ['user', 'course', 'paid']
        labels = {
            'user': 'Usuario',
            'course': 'Curso',
            'paid': 'Acceso pago (activo)',
        }
