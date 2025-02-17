"""code_analyzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # Include the app's URLs
]

from django.urls import path
#from .views import analyze_repo
from app.views import analyze_repo

urlpatterns = [
    path('', analyze_repo, name="analyze_repo"),
]
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),  # Ensure app.urls is included
]
