from django.contrib.auth.models import User
from rest_framework import serializers

from apps.abonents.models import Abonent, UserEvent
from apps.groups.models import Group, TvIdentifier


class AbonentSerializer(serializers.ModelSerializer):
    login = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Abonent
        fields = ['id', 'login', 'login_mikrotik', 'password', 'name', 'account_number',
                  'balance', 'ip_addr', 'block', 'credit', 'credit_check',
                  'email', 'phone', 'address', 'passport', 'description', 'group', 'create_date']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TvIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvIdentifier
        fields = ['identifier']


class GroupSerializer(serializers.ModelSerializer):
    tv_identifiers = TvIdentifierSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'month_price', 'bandwidth', 'tv_identifiers']


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ['id', 'abonent', 'date', 'event', 'comment', 'new_balance']
