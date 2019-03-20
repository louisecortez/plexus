"""plexus URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth import views as auth_views

from admin_console import views

urlpatterns = [
    path('',views.index),
    path('upload/', views.upload),
    path('admin/', admin.site.urls),
    path('datafiles/', views.datafiles.as_view()),
    path('users/', views.users),
    path('barangays/<int:city>/geo.json', views.BarangayGeojson.as_view()),
    path('barangays/<slug:city>/geo.json', views.BarangayGeojson.as_view()),
    path('amenities/<int:city>/geo.csv', views.AmenityGeojson.as_view()),
    path('amenities/<slug:city>/geo.csv', views.AmenityGeojson.as_view()),
    path('regions/', views.AmenityGeojson.as_view()),
    path('cities/', views.get_provinces),
    path('cities/<int:id>/', login_required(views.CityList.as_view())),
    path('get_active_cities/', views.GetActiveCities.as_view()),
    path('accounts/login/', views.login_view),
    path('accounts/logout/', views.logout_view),
    # path('list/', views.list.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
