from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Course, Module, Lesson, Enrollment, LessonProgress, Compra
from .utils import user_has_access
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .mp import crear_preferencia
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mercadopago
from django.conf import settings
from django.contrib.auth.models import User
from .emails import (
    enviar_mail_aprobado,
    enviar_mail_transferencia,
    enviar_mail_admin
)


sdk = mercadopago.SDK(
    settings.MERCADO_PAGO_ACCESS_TOKEN
)

def home(request):

    query = request.GET.get('q')

    courses = Course.objects.filter(
        is_free=False
    )

    if query:

        courses = courses.filter(
            title__icontains=query
        )

    return render(
        request,
        'pages/home.html',
        {
            'courses': courses,
            'query': query
        }
    )

def course_detail(request, slug):

    course = get_object_or_404(
        Course.objects.prefetch_related(
            'modules__lessons'
        ),
        slug=slug
    )

    modules = course.modules.all()

    lessons_count = Lesson.objects.filter(
        module__course=course
    ).count()

    has_access = user_has_access(
        request.user,
        course
    )

    return render(
        request,
        'pages/course_detail.html',
        {
            'course': course,
            'modules': modules,
            'lessons_count': lessons_count,
            'has_access': has_access,
        }
    )

def lesson_detail(request, id):

    lesson = get_object_or_404(
        Lesson.objects.select_related(
            'module__course'
        ),
        id=id
    )

    course = lesson.module.course

    has_access = user_has_access(
        request.user,
        course
    )

    if not has_access and not lesson.is_preview:

        return redirect(
            'course_detail',
            slug=course.slug
        )

    modules = course.modules.prefetch_related(
        'lessons'
    )

    completed_lessons = []

    if request.user.is_authenticated:

        completed_lessons = list(

            LessonProgress.objects.filter(
                user=request.user,
                completed=True
            ).values_list(
                'lesson_id',
                flat=True
            )

        )
    print(completed_lessons)

    current_progress = LessonProgress.objects.filter(
        user=request.user,
        lesson=lesson,
        completed=True
    ).exists()

    return render(
        request,
        'pages/lesson_detail.html',
        {
            'lesson': lesson,
            'course': course,
            'modules': modules,
            'has_access': has_access,
            'completed_lessons': completed_lessons,
            'current_progress': current_progress,
        }
    )


@login_required
def complete_lesson(request, id):

    lesson = get_object_or_404(
        Lesson,
        id=id
    )

    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    progress.completed = True

    progress.save()

    return redirect(
        'lesson_detail',
        id=lesson.id
    )

@login_required
def checkout_view(request, slug):

    course = get_object_or_404(
        Course,
        slug=slug
    )

    mp_url = crear_preferencia(
        course,
        request
    )

    if request.method == 'POST':

        metodo_pago = request.POST.get(
            'metodo_pago'
        )

        if metodo_pago == 'transferencia':

            request.session['checkout_data'] = {

                'course_id': course.id,

                'nombre': request.POST.get('nombre'),

                'apellido': request.POST.get('apellido'),

                'dni': request.POST.get('dni'),

                'email': request.POST.get('email'),

            }

            return redirect(
                'transferencia'
            )

        elif metodo_pago == 'mercadopago':

            return redirect(
                mp_url
            )

    return render(
        request,
        'pages/checkout.html',
        {
            'course': course,
            'mp_url': mp_url,
        }
    )

@login_required
def transferencia_view(request):

    data = request.session.get(
        'checkout_data'
    )

    if not data:

        return redirect('home')

    course = get_object_or_404(
        Course,
        id=data['course_id']
    )

    if request.method == 'POST':

        compra = Compra.objects.create(

            curso=course,

            usuario=request.user,

            nombre=data['nombre'],

            apellido=data['apellido'],

            dni=data['dni'],

            email=data['email'],

            metodo_pago='transferencia',

            estado='pendiente'
        )

        del request.session['checkout_data']

        enviar_mail_transferencia(
            request.user,
            course
        )

        enviar_mail_admin(
            compra
        )

        return redirect(
            f'/success/{course.slug}/?tipo=transferencia'
        )

    return render(
        request,
        'pages/transferencia.html',
        {
            'course': course
        }
    )

@login_required
def success_view(request, slug=None):

    tipo = request.GET.get(
        'tipo'
    )

    course = None

    if slug:

        course = get_object_or_404(
            Course,
            slug=slug
        )

    if tipo == 'transferencia':

        return render(
            request,
            'pages/success.html',
            {
                'tipo': 'transferencia'
            }
        )

    payment_id = request.GET.get(
        'payment_id'
    )

    status = request.GET.get(
        'status'
    )

    if payment_id and status == 'approved':

        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )

        if created:

            enviar_mail_aprobado(
                request.user,
                course
            )

    return render(
        request,
        'pages/success.html',
        {
            'course': course,
            'tipo': 'mp'
        }
    )


def recursos_gratuitos(request):

    free_courses = Course.objects.filter(
        is_free=True
    )

    return render(
        request,
        'pages/recursos_gratuitos.html',
        {
            'free_courses': free_courses
        }
    )

@csrf_exempt
def mp_webhook(request):

    if request.method == 'POST':

        data = json.loads(
            request.body
        )

        if data.get('type') == 'payment':

            payment_id = data['data']['id']

            payment = sdk.payment().get(
                payment_id
            )["response"]

            if payment["status"] == "approved":

                external_reference = payment.get(
                    "external_reference"
                )

                if external_reference:

                    user_id, course_id = external_reference.split(
                        "-"
                    )

                    user = User.objects.get(
                        id=user_id
                    )

                    course = Course.objects.get(
                        id=course_id
                    )

                    Enrollment.objects.get_or_create(
                        user=user,
                        course=course
                    )

                    compra, created = Compra.objects.get_or_create(

                        usuario=user,

                        curso=course,

                        defaults={

                            'nombre': user.first_name or user.username,

                            'apellido': '',

                            'dni': 'No informado',

                            'email': user.email,

                            'metodo_pago': 'mp',

                            'estado': 'aprobado',
                        }
                    )

                    if created:

                        enviar_mail_aprobado(
                            user,
                            course
                        )

                        enviar_mail_admin(
                            compra
                        )

        return JsonResponse(
            {'status': 'ok'}
        )

    return JsonResponse(
        {'status': 'error'}
    )
