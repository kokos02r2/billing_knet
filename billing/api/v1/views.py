from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api.v1.serializers import (AbonentSerializer, GroupSerializer,
                                UserEventSerializer, UserSerializer)
from apps.abonents.models import Abonent, Group, UserEvent
from core.helpers.сhange_tarif import change_tarif_logic
from core.helpers.trust_payment_logic import set_trust_payment
from core.helpers.recalculation import recalculation_logic
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from core.helpers.ip_generator_from_pool import generate_unique_ip_from_range
from core.helpers.ip_generator_unique import generate_unique_ip
from core.helpers.constants import CONTRACT_RANGES


class AbonentViewSet(viewsets.ModelViewSet):
    queryset = Abonent.objects.all()
    serializer_class = AbonentSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'account_number'

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def change_tarif(self, request, account_number=None):
        new_tariff = request.data.get('new_tariff')
        abonent = self.get_object()
        try:
            change_tarif_logic(abonent, str(new_tariff))
            return Response({'message': 'Тариф успешно изменен'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Ошибка при изменении тарифа: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def trust_payment(self, request, account_number=None):
        abonent = self.get_object()
        try:
            result = set_trust_payment(abonent)
            return Response({'message': f'{result}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Ошибка доверительного платежа: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def recalculation(self, request, account_number=None):
        days = request.data.get('days')
        abonent = self.get_object()
        try:
            result = recalculation_logic(abonent, days)
            return Response({'message': f'{result}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Ошибка перерасчета: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def add_money(self, request, account_number=None):
        amount = request.data.get('add_money')
        abonent = self.get_object()
        try:
            abonent.balance += amount
            abonent.save()
            event = UserEvent(
                abonent=abonent,
                event=f"{amount} руб.",
                comment=f"Добавлена сумма {amount} руб.",
                new_balance=f"{abonent.balance} руб."
            )
            event.save()
            return Response(
                {'message': f'Добавлено {amount} руб. на договор {abonent.account_number}'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({'message': f'Ошибка при добавлении средств: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def load_events(self, request, account_number=None):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        try:
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%d%m%Y').date()
                end_date = datetime.strptime(end_date, '%d%m%Y').date()
                abonent = self.get_object()
                events = UserEvent.objects.filter(date__range=(start_date, end_date), abonent=abonent)
                serializer = UserEventSerializer(events, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Ошибка при запросе событий: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def generate_unique_ip(self, request, account_number=None):
        tariff = request.data.get('tariff')
        try:
            if any(start <= int(account_number) <= end for start, end in CONTRACT_RANGES):
                new_ip_address = generate_unique_ip()
            else:
                new_ip_address = generate_unique_ip_from_range(str(tariff), int(account_number))
            data = {
                "ip_address": new_ip_address
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Ошибка при запросе сгенерированного ip: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'username'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'


class GroupByNameViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'group_name'


class UserEventViewSet(viewsets.ModelViewSet):
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'abonent'
