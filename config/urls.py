from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.urls import (
    path,
    include
)


def robots_txt(request):

    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Disallow: /checkout/",
        "Disallow: /accounts/",
    ]

    return HttpResponse(
        "\n".join(lines),
        content_type="text/plain"
    )


urlpatterns = [
    path('admin/', admin.site.urls),

    path('robots.txt', robots_txt, name='robots_txt'),

    path('', include('courses.urls')),

    path(
        'accounts/',
        include('accounts.urls')
    ),

    path(
        'dashboard/',
        include('dashboard.urls')
    ),

    path(
        'proyectos/',
        include('portfolio.urls')
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

