from apps.abonents.models import Abonent
from apps.abonents.models import Group
from django.contrib.auth.models import User
from api.v1.serializers import AbonentSerializer, UserSerializer, GroupSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets


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
