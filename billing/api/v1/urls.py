from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AbonentViewSet, GroupViewSet, UserEventViewSet, UserViewSet, GroupByNameViewSet

router = DefaultRouter()
router.register(r'v1/abonents', AbonentViewSet)
router.register(r'v1/users', UserViewSet)
router.register(r'v1/groups', GroupViewSet)
router.register(r'v1/group_names', GroupByNameViewSet)
router.register(r'v1/user_events', UserEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
