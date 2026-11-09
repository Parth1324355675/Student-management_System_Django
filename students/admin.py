from django.contrib import admin
from .models import Student
from .models import Course
from .models import UserProfile
from .models import Skill

# Register your models here.
# username=abc
# password=123

# admin.site.register(Student)


@admin.register(Student)
class Student(admin.ModelAdmin):
    list_display=[
        "id",
        "name",
        "age",
        "email",
        "city",
        "marks",
        "phone"
    ]

    list_filter=[
        "city"

    ]

    search_fields=[
        "name",
        "city",
        "email",
        "phone"
    ]

    ordering=[
        "-marks"
    ]


admin.site.register(Course)

admin.site.register(UserProfile)

admin.site.register(Skill)