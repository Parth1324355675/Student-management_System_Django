"""
URL configuration for StudentPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings

# FOR MEDIA FOLDER
from django.conf.urls.static import static

# JWT AUTHENTICATION
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('students.urls')),


    # FOR API FOLDER VIEWS- ADD PATH:=>
    path("api/",include("students.api.urls")),




    # JWT AUTHENTICATION
    path("api/token/",TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path("api/token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# This is used during development to serve uploaded media files such as student profile pictures.