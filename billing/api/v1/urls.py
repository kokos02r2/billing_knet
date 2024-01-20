from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AbonentViewSet, UserViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'v1/abonents', AbonentViewSet)
router.register(r'v1/users', UserViewSet)
router.register(r'v1/groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
