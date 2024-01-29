from django.urls import path

from . import views

urlpatterns = [
    path('init/', views.init_payment),
    path('make_payment/', views.init),
    path('recieve_payment/', views.recieve_payment),
]
