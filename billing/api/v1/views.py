from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api.v1.serializers import (AbonentSerializer, GroupSerializer,
                                UserEventSerializer, UserSerializer)
from apps.abonents.models import Abonent, Group, UserEvent


class AbonentViewSet(viewsets.ModelViewSet):
    queryset = Abonent.objects.all()
    serializer_class = AbonentSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'account_number'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'username'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'group_name'


class UserEventViewSet(viewsets.ModelViewSet):
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'abonent'
