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

from apps.sberbank_payments.views import recieve_payment_sberbank
from apps.users.views import report, send_status, send_tarif
from apps.abonents.views import report_view

from . import views


urlpatterns = [
    path('admin/add-funds/<int:abonent_id>/', views.add_funds_to_abonent, name='add_funds_to_abonent'),
    path('admin/block/<int:abonent_id>/', views.block_abonent, name='block_abonent'),
    path('admin/change-tarif/<int:abonent_id>/', views.change_tarif, name='change_tarif'),
    path('payment_report/', report_view, name='report_view'),
    path('tinkoff/', include('apps.tinkoff_payments.urls')),
    path('sberbank/', recieve_payment_sberbank, name='sberbank_payment'),
    path('admin/', admin.site.urls),
    path('auth/', include('apps.users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('payment/', views.payment, name='payment'),
    path('tarif/', send_tarif, name='tarif'),
    path('block/', send_status, name='block'),
    path('report/', report, name='report'),
    path('trust_payment/', views.trust_payment, name='trust_payment'),
    path('api/auth/', include('api.auth.urls')),
    path('api/', include('api.v1.urls'))
]
