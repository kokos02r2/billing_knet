from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    # Страница со списком сортов мороженого
    path('', views.groups),
    # Отдельная страница с информацией о сорте мороженого
    path('<str:pk>/', views.group_detail),
]
