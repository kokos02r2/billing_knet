"""billing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from . import views


urlpatterns = [
    path('admin/add-funds/<int:abonent_id>/', views.add_funds_to_abonent, name='add_funds_to_abonent'),
    path('abonents/', include('apps.abonents.urls')),
    path('groups/', include('apps.groups.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('apps.users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('profile_tarif/', views.profile_tarif, name='profile_tarif'),
    path('trust_payment/', views.trust_payment, name='trust_payment'),
    path('api/auth/', include('api.auth.urls')),
    path('api/', include('api.v1.urls')),
]
