from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import nested_admin

from .models import (
    Course,
    Module,
    Lesson,
    Enrollment,
    Compra,
)

class LessonInline(admin.StackedInline):

    model = Lesson

    extra = 0

    show_change_link = True

    fields = (
        'title',
        'duration',
        'is_preview',
        'video_url',
        'content',
    )

class ModuleInline(admin.StackedInline):

    model = Module

    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    inlines = [ModuleInline]

    list_display = (
        'thumbnail_preview',
        'title',
        'price',
        'course_type',
    )

    search_fields = (
        'title',
        'description',
    )

    list_filter = (
        'is_free',
    )

    list_per_page = 10

    def thumbnail_preview(self, obj):

        if obj.thumbnail:

            return format_html(
                '''
                <img
                    src="{}"
                    style="
                        width: 90px;
                        height: 56px;
                        object-fit: cover;
                        border-radius: 12px;
                        border: 1px solid rgba(75,46,131,0.08);
                    "
                >
                ''',
                obj.thumbnail.url
            )

        return "-"

    thumbnail_preview.short_description = 'Preview'

    def course_type(self, obj):

        if obj.is_free:

            return mark_safe('''
            <span style="
                background: rgba(233,60,172,0.12);
                color: #E93CAC;
                padding: 6px 12px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: 600;
            ">
                GRATIS
            </span>
            ''')

        return mark_safe('''
        <span style="
            background: rgba(75,46,131,0.10);
            color: #4B2E83;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
        ">
            PREMIUM
        </span>
        ''')

    course_type.short_description = 'Tipo'


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):

    inlines = [LessonInline]

    list_display = (
        'title',
        'course',
    )

    search_fields = (
        'title',
        'course__title',
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'module',
    )

    search_fields = (
        'title',
        'module__title',
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'course',
    )

    search_fields = (
        'user__username',
        'course__title',
    )


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'apellido',
        'email',
        'curso',
    )

    search_fields = (
        'nombre',
        'apellido',
        'email',
    )