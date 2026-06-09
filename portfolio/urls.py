from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.proyectos_view,
        name='proyectos'
    ),

    path(
        '<slug:slug>/',
        views.proyecto_detail,
        name='proyecto_detail'
    ),

]