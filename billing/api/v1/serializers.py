from rest_framework import serializers
from apps.abonents.models import Abonent
from apps.groups.models import Group
from django.contrib.auth.models import User


class AbonentSerializer(serializers.ModelSerializer):
    login = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Abonent
        fields = ['id', 'login', 'login_mikrotik', 'password', 'name', 'account_number',
                  'balance', 'ip_addr', 'block', 'credit', 'credit_check',
                  'email', 'phone', 'address', 'passport', 'description', 'group']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'month_price', 'bandwidth']
