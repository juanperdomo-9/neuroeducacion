from .models import Enrollment


def user_has_access(user, course):

    if not user.is_authenticated:
        return False

    return Enrollment.objects.filter(
        user=user,
        course=course,
        paid=True
    ).exists()