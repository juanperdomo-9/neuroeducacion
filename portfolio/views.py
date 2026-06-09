from django.shortcuts import (
    render,
    get_object_or_404
)

from .models import Proyecto


def proyectos_view(request):

    proyectos = Proyecto.objects.all()

    return render(
        request,
        'portfolio/proyectos.html',
        {
            'proyectos': proyectos
        }
    )


def proyecto_detail(request, slug):

    proyecto = get_object_or_404(
        Proyecto,
        slug=slug
    )

    return render(
        request,
        'portfolio/proyecto_detail.html',
        {
            'proyecto': proyecto
        }
    )