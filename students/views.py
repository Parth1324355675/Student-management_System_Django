from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse

from .models import Student
from .models import Course
from .models import UserProfile
from .models import Skill

from .forms import StudentForms

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import RegisterForm

from django.db.models import Q
from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
# UserPassesTestMixin — likely a mixin that checks whether a user passes a particular test or condition.
# PermissionRequiredMixin — a common Django class-based view mixin that checks whether a user has the required permission to access a page.


from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView

# Custom decorators
from .decorators import admin_required



from django.db.models import Avg,Count,Sum,Min,Max


from django.db import transaction
# (Transaction for commit and rollback)


from django.utils.http import url_has_allowed_host_and_scheme



# Create your views here.

@login_required
def home(request):
    # For seeing all students

    # students=Student.objects.all()



    # FOR SEEING STUDENTS UNDER USER LOGIN(Means only students under that user can be shown not other user students)

    students=Student.objects.filter(user=request.user)




    # FOR APPLYING SEARCH BAR AND ONLY SHOWING THOSE STUDENTS WHICH WE WANT REGARDLESS OF capital or small letters

    # search=request.GET.get("search")
    search=request.GET.get("search","")


    # marks_filter=request.GET.get("marks")
    marks_filter=request.GET.get("marks","")


    city_filter=request.GET.get("city","")

    # SESSION
    login_message=request.session.pop("login_message",None)

    # "login_message" is simply the key (name) you created in the session.
    # Value is "Welcome back!"
    # login_message is any variable








    # FOR SINGLE ENTRY SEARCH

    # if search:
    #     students=Student.objects.filter(name__icontains=search)







    # FOR MULTIPLE SEARCHES

    if search:
        # students=Student.objects.filter(Q(name__icontains=search) | Q(city__icontains=search))
        students=students.filter(Q(name__icontains=search) | Q(city__icontains=search))


# FOR MARKS LINKS TO FIND BW VARIOUS CATEGORY

    if marks_filter=="80":
        students=students.filter(marks__gte=80)

    elif marks_filter=="60":
        students=students.filter(marks__gte=60)

    elif marks_filter=="40":
        students=students.filter(marks__gte=40)

    elif marks_filter=="below40":
        students=students.filter(marks__lt=40)

        # here marks is the field name in Student mdel


    if city_filter:
        students=students.filter(city=city_filter)
        # here city is the field name in Student model

    cities=Student.objects.filter(user=request.user).values_list("city",flat=True).distinct() 



    # cities → gets the list of cities to show in the dropdown.
    # city_filter → remembers which city the user selected and filters students by that city   




    # For applying conditions filter

    # students=Student.objects.filter(marks__gte=70)
    # students=Student.objects.filter(marks__gte=70,city="Delhi")



    paginator=Paginator(students,5)
    page_num=request.GET.get("page")
    page_obj=paginator.get_page(page_num)



    context={
        # "students":students,
        "students":page_obj,
        "search":search,
        "marks_filter":marks_filter,
        "cities":cities,
        "city_filter":city_filter,
        "login_message":login_message,
        }

    return render(request,'home.html',context)


# def about(request):
#     return render(request,"about.html")


# CLASS BASED VIEW(CBV)

class AboutView(View):
    def get(self,request):
        return render(request,"about.html")

    def post(self,request):
        pass


# CUSTOM DECORATOR

@admin_required
def admin_dashboard(request):
    students=Student.objects.all()
    return render(request,"admin_dashboard.html",{"students":students})



def contact(request):
    return render(request,"contact.html")







# CRUD OPERATIONS

@login_required
def add_student(request):
    if request.method=="POST":
        form=StudentForms(request.POST,request.FILES)
        if form.is_valid():
            # form.save()

            # FOREIGN KEY CONCEPT

            student=form.save(commit=False)  # student=Student()


# Create the Student object, but don't save it to the database yet.

            student.user=request.user
            student.save()
            form.save_m2m()
##############################################################################      



            messages.success(request,"Student added successfully")
            return redirect("home")

    else:
        form=StudentForms()

    return render(request,"add_student.html",{"form":form})


# So every Student object has a user field.

# For example:

# student.name = "Parth"
# student.age = 22
# student.user = ???

# The user field is asking:

# "Which Django User does this student belong to


# request.user means:

# The user who is currently logged in.

# Because you have:

# @login_required
# def add_student(request):
# Django knows who is logged in.

# Imagine Parth is logged in.


# form is a form object

# When you write:

# form = StudentForms(request.POST)

# form is an instance of your Django Form.

# It contains the submitted form data and validation logic.

# It is not your Student model object.

# student is the model object

# When you write:

# student = form.save(commit=False)

# Django takes the form data and creates a Student model object.

# It tells Django:

# "This form is connected to the Student model."

# So when you do:

# student = form.save(commit=False)

# Django says:

# "This is a ModelForm for the Student model, so I'll create a Student model object from the form data."






@login_required
def edit_student(request,id):
    # student=get_object_or_404(Student,id=id)

    # student=Student.objects.get(id=id,user=request.user)
    student=get_object_or_404(Student,id=id,user=request.user)
    if request.method=="POST":
        form=StudentForms(request.POST,request.FILES,instance=student)
        if form.is_valid():
            form.save()
            messages.success(request,"Student updated successfully")
            return redirect("home")

    else:
        form=StudentForms(instance=student)

    return render(request,"edit_student.html",{"form":form})





@login_required
def delete_student(request,id):
    # student=get_object_or_404(Student,id=id)


    student=get_object_or_404(Student,id=id,user=request.user)

    if request.method=="POST":
        student.delete()
        messages.success(request,"Student deleted successfully")  #success, error, warning,info  
        return redirect("home")

    return render(request,"delete_student.html",{"student":student})








# FOR LOGIN FORM

def user_login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)

            # Session
            request.session["login_message"]="Welcome back!"

            # "login_message" is just a key/name used to identify the data stored in the session.
            #  "Welcome back" is value.

            # Before pop:

            # Session
            # └── login_message → "Welcome back!"


            # After pop:

            # Session
            # └── empty

            # Python variable:
            # message → "Welcome back!"



            messages.success(request,"Login successfully")
            next_url=request.POST.get("next")or request.GET.get("next")

# url_has_allowed_host_and_scheme => If your website redirects users to any URL without checking it, an attacker could trick users into visiting a malicious website after login. This is called an open redirect vulnerability.Your code checks the destination before redirecting.

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts=request.get_host(),
                require_https=request.is_secure()
            ):
                return redirect(next_url)


            return redirect("home")

        else:
            messages.error(request,"Invalid username or password.")

    return render(request,"login.html")

#  the next_url part in your Django login code is used to send the user back to the page they wanted to visit before logging in.
# Suppose a user is not logged in and tries to open /profile/.

# Your website redirects the user to:
# /login/?next=/profile/

# After successful login, you want to send them to /profile/, not always to the home page.
# That's exactly what next_url does!






@login_required
@require_POST
def user_logout(request):
    logout(request)
    messages.success(request,"You have been logged out successfully")
    return redirect("login")


def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration successful")
            return redirect("login")
    else:
        form=RegisterForm()

    return render(request,"register.html",{"form":form})




# GENERIC CLASS BASED VIEWS



# 1.LISTVIEW


# from django.views.generic import ListView
# from django.contrib.auth.mixins import LoginRequiredMixin

class StudentListView(LoginRequiredMixin,ListView):
    model=Student
    template_name="student_list.html"
    context_object_name="students"

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)
    
# Student.objects.all()--->by default.

# But you don't want all students.You want only the students belonging to the logged-in user.That's why you're overriding get_queryset().

# get_queryset() tells Django: "Exactly which Student objects should I show?"






#2. DetailView

# from django.views.generic import DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin
class StudentDetailView(DetailView,LoginRequiredMixin):
    model=Student
    template_name="student_detail.html"
    context_object_name="student"

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)

    


# DIFFERENCE BETWEEN FUNCTION AND CLASS BASED VIEWS

@login_required
def student_detail(request,id):
    student=get_object_or_404(Student,id=id,user=request.user)

    return render(request,"student_detail.html",{"student":student})



# 3. CREATEVIEW


# from django.views.generic import CreateView

class StudentCreateView(LoginRequiredMixin,CreateView):
    model=Student
    form_class=StudentForms
    template_name="add_student_cbv.html"
    success_url="/"

    def form_valid(self, form):
        student=form.save(commit=False)
        student.user=self.request.user
        student.save()
        return super().form_valid(form)

#     When a user submits the form, Django validates the data first.
# - If the form is invalid, Django displays the form again with errors.
# - If the form is valid, Django calls form_valid().

# - form parameter — the form object containing the submitted data, which has already passed validation.



# 4. UPDATEVIEW

from django.views.generic import UpdateView

class StudentUpdateView(LoginRequiredMixin,UpdateView):
    model=Student
    form_class=StudentForms
    template_name="edit_student_cbv.html"
    success_url="/"

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)




# 5.DELETE VIEW

# from django.views.generic import DeleteView

class StudentDeleteView(LoginRequiredMixin,DeleteView):
    model=Student
    template_name="delete_student_cbv.html"
    context_object_name:"students"
    success_url="/"

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)
    


# PERMISSION

# from django.contrib.auth.mixins import PermissionRequiredMixin
class StudentPermissionView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model=Student
    template_name="permission_students.html"
    context_object_name="students"
    permission_required="students.view_student"

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)

# Here    permission_required="students.view_student" means
#     permission_required:"app_label.permission"

# appName/label=students
# permission:view_student

# Django automatically creates model permissions such as:

# add_student
# change_student
# delete_student
# view_student

# LoginRequiredMixin → Are you logged in?
# PermissionRequiredMixin → Are you allowed to do this?
# ListView → Show me a list.
# get_queryset() → Which objects should I show?



# add_student
# change_student
# delete_student
# view_student
# Here student means:

# The type of object on which this permission operates
# 4. What are Student objects?

# Suppose your database has:

# Student #1 → Parth
# Student #2 → Rahul
# Student #3 → Aman

# All three are instances/objects of the Student model.

# Model	          Permission
# Student  	      view_student
# Manager	          view_manager
# Employee	      view_employee

# And remember: model name → lowercase for the default permission codenam

# Django stores permissions in the database.Django has a built-in model called: Permission

# Why do we need permissions?
# Suppose you have a student management website.

# You have these URLs:

# /students/
# /students/add/
# /students/edit/5/
# /students/delete/5/
# Now imagine a normal user logs in.

# Should that user automatically be allowed to:

# View students?    ✅
# Add students?     ❓
# Edit students?    ❓
# Delete students?  ❌
# If you don't have permissions, you may accidentally allow users to perform actions they shouldn't.

# Permissions help you control this.

# 3. Authentication vs Permission/Authorization

# Authentication asks:

# "Who are you?"

# For example:

# Username: parth
# Password: ********

#         ↓

# Django checks

#         ↓

# You are Parth
# This is authentication.

# Authorization / Permission
# Permission asks:

# "What are you allowed to do?"

# For example:

# You are Parth
#        ↓
# Are you allowed to delete students?
#        ↓
#        NO
# That's authorization.



# UserPassesTestMixin-UserPassesTestMixin lets you create a rule to decide whether a user is allowed to access a view.
# User must be in the Admin group → UserPassesTestMixin 

# UserPassesTestMixin lets you create a custom permission rule for a class-based view.
# UserPassesTestMixin  => "Does the user pass my custom rule?"


# in this case abc is in admin group
# And ab is in Student Group



from django.contrib.auth.mixins import UserPassesTestMixin
class AdminOnlyView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model=Student
    template_name="admin_only.html"
    context_object_name="students"


# test_func(self):This checks whether the currently logged-in user belongs to the Admin group.

    def test_func(self):
        return self.request.user.groups.filter(name="Admin").exists()

    def get_queryset(self):
        return Student.objects.all()


#COURSE LIST VIEW

class CourseListView(LoginRequiredMixin,ListView):
    model=Course
    template_name="course_list.html"
    context_object_name="courses"
    ordering=["name"]


# COURSE DETAIL VIEW

# from .models import Course
class CourseDetailView(LoginRequiredMixin,DetailView):
    model=Course
    template_name="course_detail.html"
    context_object_name="course"


# USERPROFILE VIEW

class UserProfileView(LoginRequiredMixin,DetailView):
    model=UserProfile
    template_name="user_profile.html"
    context_object_name="profile"

    def get_object(self):
        return get_object_or_404(UserProfile,user=self.request.user)


# get_object(self)=>get_object() tells the DetailView:-"Which single object should I show?"
# Normally, DetailView expects an ID or primary key from the URL.
# For example:

# /profile/5/
# But you don't want that.

# You want:

# "Show the profile of the currently logged-in user."
# That's why you override get_object().




# get_object_or_404(UserProfile,user=self.request.user)=>"Find the UserProfile belonging to the currently logged-in user. If it doesn't exist, show a 404 page."



class SkillListView(LoginRequiredMixin,ListView):
    model=Skill
    template_name="skill_list.html"
    context_object_name="skills"




class SkillDetailView(LoginRequiredMixin,DetailView):
    model=Skill
    template_name="skill_detail.html"
    context_object_name="skill"




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["students"] = self.object.students.filter(
            user=self.request.user
        )

        return context

# get_context_data() => This is a Django-provided method that you can override to add extra data to the template.



class StudentStatisticView(LoginRequiredMixin,View):

    def get(self,request):

        students=Student.objects.filter(user=request.user)

        total_students=students.count()

        average_marks=students.aggregate(
            Avg("marks")
        )["marks__avg"]


        lowest_marks=students.aggregate(
            Min("marks")
        )["marks__min"]


        highest_marks=students.aggregate(
            Max("marks")
        )["marks__max"]

        context={
            "total_students":total_students,
            "average_marks": average_marks,
            "highest_marks": highest_marks,
            "lowest_marks": lowest_marks
        }

        return render(request,"student_statistic.html",context)


class CourseStatisticsview(LoginRequiredMixin,ListView):
    model=Course
    template_name="course_statistics.html"
    context_object_name="courses"

    def get_queryset(self):
        return Course.objects.annotate(
            student_count=Count("students",filter=Q(students__user=self.request.user))

        ).order_by("-student_count")   
    
    # .filter(student_count__gte=3)
    # .order_by("-student_count") = descending order
    # .order_by("student_count") = ascending order

#  annotate - annotate() adds extra calculated information to each object.

class TopStudentsView(LoginRequiredMixin,ListView):
    model=Student
    template_name="top_students.html"
    context_object_name="students"

    def get_queryset(self):
        return Student.objects.filter(
            user=self.request.user,marks__gte=80).order_by("-marks")
    
        # return Student.objects.filter(user=self.request.user, Q(marks__gte=80)& Q(city__exact="Delhi")).order_by("-marks")

    
class PopularCourseView(LoginRequiredMixin,ListView):
    model=Course
    template_name="popular_courses.html"
    context_object_name="courses"

    def get_queryset(self):
        return Course.objects.annotate(student_count=Count("students",filter=Q(students__user=self.request.user))).filter(
            Q(student_count__gte=2)|
            Q(name__icontains="Python")
        ).order_by("-student_count")



# ORM PERFORMANCE

# select_related => OnetoOne , Foreign Key(OnetoMany),ReverseForegnKey(ManytoOne)

# prefetch_related => ManytoMany relationship

# students=Student.objects.select_related("user","course").prefetch_related("skills").filter(user=request.user)
