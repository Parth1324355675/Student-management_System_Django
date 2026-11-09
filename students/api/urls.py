
# FOR GENERIC VIEWS

# from django.urls import path
# from . import views

# urlpatterns = [
#     path("students/",views.StudentListCreateAPIView.as_view(),name="api_students"),
#     path("students/<int:pk>",views.StudentDetailAPIView.as_view(),name="api_student_detail"),
# ]


# VIEW SETS
# Model View Set

from .views import StudentViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("students",StudentViewSet,basename="students")

urlpatterns = router.urls


##########################################################
# JWT Authentication(JavascriptObjectNotation Web Token)=[{}]