from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    # Страница со списком сортов мороженого
    path('', views.abonents),
    # Отдельная страница с информацией о сорте мороженого
    path('<int:pk>/', views.abonent_detail),
]
