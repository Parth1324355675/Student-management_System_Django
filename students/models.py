from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

# Create your models here.


class Course(models.Model):
    name=models.CharField(max_length=200)
    duration=models.IntegerField()
    fees=models.DecimalField(max_digits=10,decimal_places=2)
    

    def __str__(self):
        return self.name


class Skill(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


# CUSTOM QUERY SET

class UserQuerySet(models.QuerySet):
    def for_user(self,user):
        return self.filter(user=user)

    def passed(self):
        return self.filter(marks__gte=40)

    def top_students(self):
        return self.filter(marks__gte=80).order_by("-marks")




class Student(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE,default="",blank=True)

    # In User, Parent(User) deleted → Child(student) also deleted

    course=models.ForeignKey(Course,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             related_name="students"  # course.students.all()
                             )
    

    # SET_NULL means: delete the Course, but keep the Student.
    # Parent deleted → Child remains, ForeignKey becomes NULL

    skills=models.ManyToManyField(Skill,
                                  blank=True,
                                  related_name="students"
                                  )     # skills.students.all()

    name=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    marks=models.IntegerField()
    age=models.IntegerField()
    email=models.EmailField()

    phone=models.CharField(max_length=15,default="",blank=True)

    # Adding Profile Image
    profile_image=models.ImageField(upload_to="student_images/",blank=True,null=True)

    document=models.FileField(upload_to="student_document/",blank=True,null=True)

    # CUSTOM QUERY SET

    objects=UserQuerySet.as_manager()

    # Student.objects.for_user()

# UserQuerySet is a QuerySet.Student.objects is a Manager.
# as_manager() connects your custom QuerySet to the model's manager.





    # Meta is used for database     
    class Meta:
        constraints=[
            models.CheckConstraint(
                condition=Q(marks__gte=0) & Q(marks__lte=100),
                name="students_marks_0_to_100"
            ),

            models.UniqueConstraint(
                fields=["user","email"],
                name="unique_student_email_per_user",

            )
        ]


    # def clean is used for backend
    def clean(self):
        if self.marks < 0 & self.marks >100:
            raise ValidationError("Marks should be between 0 and 100")


    def __str__(self):
        return self.name


# on_delete	|     When Course/User is deleted

# CASCADE	|     Delete the Student too
# SET_NULL	|     Keep Student, set relationship to NULL


# related_name= students => It gives you a custom name to access related objects from the other side of the relationship.

# For example:

# Course:
#     Python

# Students:
#     Parth
#     Rahul
#     Aman


# you can do:

# course.students.all()

# and Django gives you:

# Parth
# Rahul
# Aman


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth=models.DateField(null=True,blank=True)
    address=models.TextField(blank=True)
    guardian_name=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
        



    