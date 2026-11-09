from django.db import transaction
from .models import Student,UserProfile

@transaction.atomic
def create_student_with_profile(
    user,
    student_data,
    profile_data
):
    student=Student.objects.create(
        user=user,
        **student_data
    )

    UserProfile.objects.create(
        user=user,
        **profile_data
    )

    return student


# All databases changes inside the transaction success together or they rolled back together.