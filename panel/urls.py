from django.urls import path

from . import views

app_name = 'panel'

urlpatterns = [

    path('ingresar/', views.login_view, name='login'),
    path('salir/', views.logout_view, name='logout'),
    path('', views.overview, name='overview'),

    path('compras/', views.compras_list, name='compras_list'),
    path('compras/<int:pk>/aprobar/', views.compra_aprobar, name='compra_aprobar'),
    path('compras/<int:pk>/rechazar/', views.compra_rechazar, name='compra_rechazar'),

    path('testimonios/', views.testimonios_list, name='testimonios_list'),
    path('testimonios/<int:pk>/toggle/', views.testimonio_toggle, name='testimonio_toggle'),
    path('testimonios/<int:pk>/eliminar/', views.testimonio_delete, name='testimonio_delete'),

    path('cursos/', views.course_list, name='course_list'),
    path('cursos/nuevo/', views.course_create, name='course_create'),
    path('cursos/<int:pk>/', views.course_detail, name='course_detail'),
    path('cursos/<int:pk>/editar/', views.course_edit, name='course_edit'),
    path('cursos/<int:pk>/eliminar/', views.course_delete, name='course_delete'),

    path('cursos/<int:course_pk>/modulos/nuevo/', views.module_create, name='module_create'),
    path('modulos/<int:pk>/editar/', views.module_edit, name='module_edit'),
    path('modulos/<int:pk>/eliminar/', views.module_delete, name='module_delete'),

    path('modulos/<int:module_pk>/lecciones/nueva/', views.lesson_create, name='lesson_create'),
    path('lecciones/<int:pk>/editar/', views.lesson_edit, name='lesson_edit'),
    path('lecciones/<int:pk>/eliminar/', views.lesson_delete, name='lesson_delete'),

    path('inscripciones/', views.enrollment_list, name='enrollment_list'),
    path('inscripciones/nueva/', views.enrollment_create, name='enrollment_create'),
    path('inscripciones/<int:pk>/eliminar/', views.enrollment_delete, name='enrollment_delete'),

]
