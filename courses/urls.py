from django.urls import path
from . import views
urlpatterns = [

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