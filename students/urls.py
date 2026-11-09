from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    # path('about/',views.about,name="about"),


    path('contact/',views.contact,name="contact"),
    path('add/',views.add_student,name="add_student"),
    path('student/<int:id>/edit/',views.edit_student,name="edit_student"),
    path('student/<int:id>/delete/',views.delete_student,name="delete_student"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('register/',views.register,name="register"),
    path('logout/',views.logout,name="logout"),

    # FOR CLASS BASED VIEW
    path('about/',views.AboutView.as_view(),name="about"),

    # Generic class Based view-- Listview
    path('student-list/',views.StudentListView.as_view(),name="student-list"),


    # Generic class Based view-- Detailview
    # Find the Student whose primary key (pk) is 2. Generic view uses pk to identify an object.
    path('student/<int:pk>/',views.StudentDetailView.as_view(),name="student_detail"),


    # Generic class Based view-- Createview
    path('student/add-cbv',views.StudentCreateView.as_view(),name='student_add_cbv'),


    #  Generic class Based view-- Updateview
    path("student/<int:pk>/edit-cbv/",views.StudentUpdateView.as_view(),name="student_edit_cbv"),


    # Generic class Based view-- Deleteview
    path("student/<int:pk>/delete-cbv",views.StudentDeleteView.as_view(),name="student_delete_cbv"),

    # Permissions- view_student
    path("permission-studentsview/",views.StudentPermissionView.as_view(),name="permission_students"),


    path("admin-students/",views.AdminOnlyView.as_view(),name="admin_students"),

    path("admin-dashboard/",views.admin_dashboard,name="admin_dashboard"),

    #COURSE LIST VIEW
    
    path("courses/",views.CourseListView.as_view(),name="course_list"),

    # COURSE DETAIL VIEW
    path("course/<int:pk>/",views.CourseDetailView.as_view(),name="course_detail"),

    # USER PROFILE VIEW
    path("profile/",views.UserProfileView.as_view(),name="user_profile"),

    # Skill
    path("skill/<int:pk>/",views.SkillDetailView.as_view(),name="skill_detail"),

    path("skills/",views.SkillListView.as_view(),name="skill_list"),

    path("statistics/",views.StudentStatisticView.as_view(),name="student_statistics"),

    path("course-statistics/",views.CourseStatisticsview.as_view(),name="course_statistics"),

    path("top-students/",views.TopStudentsView.as_view(),name="top_students"),

    path("popular-courses/",views.PopularCourseView.as_view(),name="popular_courses"),



]
    