from django.urls import path
from django.views.generic import TemplateView
from . import views
urlpatterns = [

    path(
        'terminos/',
        TemplateView.as_view(template_name='pages/terminos.html'),
        name='terminos'
    ),

    path(
        'privacidad/',
        TemplateView.as_view(template_name='pages/privacidad.html'),
        name='privacidad'
    ),

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'checkout/<slug:slug>/',
        views.checkout_view,
        name='checkout'
    ),

    path(
        'course/<slug:slug>/',
        views.course_detail,
        name='course_detail'
    ),

    path(
        'lesson/<int:id>/',
        views.lesson_detail,
        name='lesson_detail'
    ),

    path(
        'lesson/<int:id>/complete/',
        views.complete_lesson,
        name='complete_lesson'
    ),

    path(
        'transferencia/',
        views.transferencia_view,
        name='transferencia'
    ),
    
    path(
        'success/<slug:slug>/',
        views.success_view,
        name='success'
    ),
    
    path(
        'recursos-gratuitos/',
        views.recursos_gratuitos,
        name='recursos_gratuitos'
    ),

    path(
        'webhook/mp/',
        views.mp_webhook,
        name='mp_webhook'
    ),
]