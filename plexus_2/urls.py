"""plexus_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views

from admin_console import views

urlpatterns = [
    path('',views.index),
    path('upload/', views.upload),
    path('admin/', admin.site.urls),
    path('datafiles/', views.datafiles.as_view()),
    path('barangays/<slug:city>/geo.json', views.BarangayGeojson.as_view()),
    path('amenities/<slug:city>/geo.json', views.AmenityGeojson.as_view()),
    path('regions/', views.AmenityGeojson.as_view()),
    path('cities/', views.get_cities),
    path('accounts/login/', views.login_view),
    # path('list/', views.list.as_view())
]
