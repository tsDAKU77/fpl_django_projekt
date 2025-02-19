"""
URL configuration for FPL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from FPLapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.player_stats, name='player_stats'),
    path("register/", views.user_register, name='register'),
    path("login/", views.user_login, name='login'),
    path("manage-squad/", views.manage_squad, name='manage_squad'),
    path("manage-xi/", views.manage_xi, name='manage_xi'),
    path("logout/", views.user_logout, name='logout'),
]
