from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from courses.emails import enviar_mail_aprobado
from courses.models import (
    Compra, Course, Enrollment, Lesson, Module, Testimonio,
)

from .forms import CourseForm, EnrollmentForm, LessonForm, ModuleForm


def staff_required(view_func):
    """
    Solo staff logueado entra. Redirige al login propio del
    panel, no al de /admin/login/.
    """
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='panel:login',
    )(view_func)


# ==========================================
# AUTH
# ==========================================

def login_view(request):

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('panel:overview')

    error = None

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:

            login(request, user)

            next_url = request.GET.get('next') or reverse('panel:overview')

            return redirect(next_url)

        error = 'Usuario o contraseña incorrectos, o la cuenta no es de staff.'

    return render(request, 'panel/login.html', {'error': error})


@staff_required
def logout_view(request):

    logout(request)

    return redirect('panel:login')


# ==========================================
# RESUMEN
# ==========================================

@staff_required
def overview(request):

    compras_pendientes = Compra.objects.filter(
        estado='pendiente'
    ).select_related('curso', 'usuario').order_by('-creado')

    ingresos_aprobados = sum(
        compra.curso.price
        for compra in Compra.objects.filter(
            estado='aprobado'
        ).select_related('curso')
    )

    stats = {
        'pendientes_count': compras_pendientes.count(),
        'alumnos_count': Enrollment.objects.filter(paid=True).values('user').distinct().count(),
        'cursos_count': Course.objects.count(),
        'ingresos_aprobados': ingresos_aprobados,
    }

    return render(request, 'panel/overview.html', {
        'stats': stats,
        'compras_pendientes': compras_pendientes[:6],
    })


# ==========================================
# COMPRAS
# ==========================================

@staff_required
def compras_list(request):

    estado = request.GET.get('estado', 'pendiente')

    compras = Compra.objects.select_related(
        'curso', 'usuario'
    ).order_by('-creado')

    if estado in ('pendiente', 'aprobado', 'rechazado'):
        compras = compras.filter(estado=estado)

    return render(request, 'panel/compras_list.html', {
        'compras': compras,
        'estado_actual': estado,
    })


@staff_required
def compra_aprobar(request, pk):

    compra = get_object_or_404(Compra, pk=pk)

    if request.method == 'POST':

        ya_estaba_aprobada = compra.estado == 'aprobado'

        compra.estado = 'aprobado'
        # El post_save de Compra crea el Enrollment automáticamente.
        compra.save()

        if not ya_estaba_aprobada:
            enviar_mail_aprobado(compra.usuario, compra.curso)

        messages.success(
            request,
            f'Compra de {compra.nombre} {compra.apellido} aprobada. '
            f'Ya tiene acceso a "{compra.curso.title}".'
        )

    return redirect('panel:compras_list')


@staff_required
def compra_rechazar(request, pk):

    compra = get_object_or_404(Compra, pk=pk)

    if request.method == 'POST':

        compra.estado = 'rechazado'
        compra.save()

        messages.success(
            request,
            f'Compra de {compra.nombre} {compra.apellido} marcada como rechazada.'
        )

    return redirect('panel:compras_list')


# ==========================================
# TESTIMONIOS
# ==========================================

@staff_required
def testimonios_list(request):

    if request.method == 'POST':

        nombre = request.POST.get('nombre', '').strip()
        rol = request.POST.get('rol', '').strip()
        texto = request.POST.get('texto', '').strip()

        if nombre and texto:

            Testimonio.objects.create(
                nombre=nombre,
                rol=rol,
                texto=texto,
            )

            messages.success(request, 'Testimonio agregado.')

        else:

            messages.error(request, 'Falta el nombre o el texto del testimonio.')

        return redirect('panel:testimonios_list')

    testimonios = Testimonio.objects.all()

    return render(request, 'panel/testimonios_list.html', {
        'testimonios': testimonios,
    })


@staff_required
def testimonio_toggle(request, pk):

    testimonio = get_object_or_404(Testimonio, pk=pk)

    if request.method == 'POST':

        testimonio.activo = not testimonio.activo
        testimonio.save()

    return redirect('panel:testimonios_list')


@staff_required
def testimonio_delete(request, pk):

    testimonio = get_object_or_404(Testimonio, pk=pk)

    if request.method == 'POST':

        testimonio.delete()
        messages.success(request, 'Testimonio eliminado.')

    return redirect('panel:testimonios_list')


# ==========================================
# CURSOS
# ==========================================

@staff_required
def course_list(request):

    courses = Course.objects.all().order_by('-created_at')

    return render(request, 'panel/course_list.html', {
        'courses': courses,
    })


@staff_required
def course_create(request):

    if request.method == 'POST':

        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():

            course = form.save()
            messages.success(request, 'Curso creado.')
            return redirect('panel:course_detail', pk=course.pk)

    else:

        form = CourseForm()

    return render(request, 'panel/course_form.html', {
        'form': form,
        'is_new': True,
    })


@staff_required
def course_detail(request, pk):

    course = get_object_or_404(
        Course.objects.prefetch_related('modules__lessons'),
        pk=pk
    )

    return render(request, 'panel/course_detail.html', {
        'course': course,
        'modules': course.modules.all().order_by('order', 'id'),
    })


@staff_required
def course_edit(request, pk):

    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':

        form = CourseForm(request.POST, request.FILES, instance=course)

        if form.is_valid():

            form.save()
            messages.success(request, 'Curso actualizado.')
            return redirect('panel:course_detail', pk=course.pk)

    else:

        form = CourseForm(instance=course)

    return render(request, 'panel/course_form.html', {
        'form': form,
        'course': course,
        'is_new': False,
    })


@staff_required
def course_delete(request, pk):

    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':

        title = course.title

        try:
            course.delete()
            messages.success(request, f'"{title}" eliminado.')
        except ProtectedError:
            messages.error(
                request,
                f'No se puede eliminar "{title}": tiene compras o '
                f'inscripciones asociadas.'
            )

        return redirect('panel:course_list')

    return render(request, 'panel/confirm_delete.html', {
        'title': f'¿Eliminar "{course.title}"?',
        'warning': 'Esto borra también sus módulos y lecciones. No se puede deshacer.',
        'cancel_url': 'panel:course_detail',
        'cancel_pk': course.pk,
    })


# ==========================================
# MÓDULOS
# ==========================================

@staff_required
def module_create(request, course_pk):

    course = get_object_or_404(Course, pk=course_pk)

    if request.method == 'POST':

        form = ModuleForm(request.POST)

        if form.is_valid():

            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, 'Módulo creado.')
            return redirect('panel:course_detail', pk=course.pk)

    else:

        form = ModuleForm()

    return render(request, 'panel/module_form.html', {
        'form': form,
        'course': course,
        'is_new': True,
    })


@staff_required
def module_edit(request, pk):

    module = get_object_or_404(Module, pk=pk)

    if request.method == 'POST':

        form = ModuleForm(request.POST, instance=module)

        if form.is_valid():

            form.save()
            messages.success(request, 'Módulo actualizado.')
            return redirect('panel:course_detail', pk=module.course_id)

    else:

        form = ModuleForm(instance=module)

    return render(request, 'panel/module_form.html', {
        'form': form,
        'course': module.course,
        'module': module,
        'is_new': False,
    })


@staff_required
def module_delete(request, pk):

    module = get_object_or_404(Module, pk=pk)
    course_pk = module.course_id

    if request.method == 'POST':

        module.delete()
        messages.success(request, 'Módulo eliminado.')

    return redirect('panel:course_detail', pk=course_pk)


# ==========================================
# LECCIONES
# ==========================================

@staff_required
def lesson_create(request, module_pk):

    module = get_object_or_404(Module, pk=module_pk)

    if request.method == 'POST':

        form = LessonForm(request.POST)

        if form.is_valid():

            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, 'Lección creada.')
            return redirect('panel:course_detail', pk=module.course_id)

    else:

        form = LessonForm()

    return render(request, 'panel/lesson_form.html', {
        'form': form,
        'module': module,
        'is_new': True,
    })


@staff_required
def lesson_edit(request, pk):

    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'POST':

        form = LessonForm(request.POST, instance=lesson)

        if form.is_valid():

            form.save()
            messages.success(request, 'Lección actualizada.')
            return redirect('panel:course_detail', pk=lesson.module.course_id)

    else:

        form = LessonForm(instance=lesson)

    return render(request, 'panel/lesson_form.html', {
        'form': form,
        'module': lesson.module,
        'lesson': lesson,
        'is_new': False,
    })


@staff_required
def lesson_delete(request, pk):

    lesson = get_object_or_404(Lesson, pk=pk)
    course_pk = lesson.module.course_id

    if request.method == 'POST':

        lesson.delete()
        messages.success(request, 'Lección eliminada.')

    return redirect('panel:course_detail', pk=course_pk)


# ==========================================
# INSCRIPCIONES
# ==========================================

@staff_required
def enrollment_list(request):

    enrollments = Enrollment.objects.select_related(
        'user', 'course'
    ).order_by('-created_at')

    return render(request, 'panel/enrollment_list.html', {
        'enrollments': enrollments,
    })


@staff_required
def enrollment_create(request):

    if request.method == 'POST':

        form = EnrollmentForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request, 'Inscripción creada / acceso otorgado.')
            return redirect('panel:enrollment_list')

    else:

        form = EnrollmentForm()

    return render(request, 'panel/enrollment_form.html', {
        'form': form,
    })


@staff_required
def enrollment_delete(request, pk):

    enrollment = get_object_or_404(Enrollment, pk=pk)

    if request.method == 'POST':

        nombre = f'{enrollment.user} - {enrollment.course}'
        enrollment.delete()
        messages.success(request, f'Acceso revocado: {nombre}.')

    return redirect('panel:enrollment_list')
