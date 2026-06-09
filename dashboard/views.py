from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from courses.models import (
    Enrollment,
    Lesson,
    LessonProgress
)


@login_required
def dashboard_view(request):

    enrollments = Enrollment.objects.filter(
        user=request.user,
        paid=True
    ).select_related('course')

    dashboard_courses = []

    for enrollment in enrollments:

        course = enrollment.course

        total_lessons = Lesson.objects.filter(
            module__course=course
        ).count()

        completed_lessons = LessonProgress.objects.filter(
            user=request.user,
            lesson__module__course=course,
            completed=True
        ).count()

        progress_percentage = 0

        if total_lessons > 0:

            progress_percentage = int(
                (completed_lessons / total_lessons) * 100
            )

        last_completed = LessonProgress.objects.filter(
            user=request.user,
            lesson__module__course=course,
            completed=True
        ).select_related(
            'lesson'
        ).order_by(
            '-completed_at'
        ).first()

        all_lessons = list(

            Lesson.objects.filter(
                module__course=course
            ).order_by(
                'module__id',
                'id'
            )

        )

        next_lesson = None

        if last_completed:

            for index, lesson in enumerate(all_lessons):

                if lesson.id == last_completed.lesson.id:

                    if index + 1 < len(all_lessons):

                        next_lesson = all_lessons[index + 1]

                    break

        if not next_lesson and all_lessons:

            next_lesson = all_lessons[0]

        dashboard_courses.append({

            'course': course,

            'total_lessons': total_lessons,

            'completed_lessons': completed_lessons,

            'progress_percentage': progress_percentage,

            'next_lesson': next_lesson,
        })

    return render(
        request,
        'dashboard/index.html',
        {
            'dashboard_courses': dashboard_courses
        }
    )