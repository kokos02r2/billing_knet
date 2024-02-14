from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime
from apps.abonents.models import Abonent, UserEvent
from apps.groups.models import Group

User = get_user_model()


class AbonentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.group = Group.objects.create(group_name='Test Group', month_price=50)
        self.abonent = Abonent.objects.create(
            login=self.user,
            login_mikrotik='test_login',
            password='test_password',
            name='Test Abonent',
            account_number='123456',
            balance=100,
            group=self.group,
            ip_addr='192.168.0.1',
            block=False,
            create_date=datetime.now(),
            credit='1000x01-01-2023',
            email='test@example.com',
            phone='123456789',
            address='Test Address',
            passport='1234567890',
            description='Test Description'
        )

    def test_colored_balance(self):
        # Test for positive balance
        self.abonent.balance = 100
        self.assertEqual(self.abonent.colored_balance(), '<b><span style="color: #008000;">100</span></b>')

        # Test for negative balance
        self.abonent.balance = -50
        self.assertEqual(self.abonent.colored_balance(), '<b><span style="color: #ff0000;">-50</span></b>')

    def test_colored_name(self):
        # Test for unblocked user with positive balance
        self.abonent.block = False
        self.abonent.balance = 100
        self.assertEqual(self.abonent.colored_name(), '<b><span style="color: #008000;">Test Abonent</span></b>')

        # Test for unblocked user with negative balance
        self.abonent.balance = -50
        self.assertEqual(self.abonent.colored_name(), '<b><span style="color: #d4d4d4;">Test Abonent</span></b>')

        # Test for blocked user
        self.abonent.block = True
        self.assertEqual(self.abonent.colored_name(), '<b><span style="color: #ff0000;">Test Abonent</span></b>')

    def test_string_representation(self):
        self.assertEqual(str(self.abonent), 'test_user')


class UserEventModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.group = Group.objects.create(group_name='Test Group', month_price=50)
        self.abonent = Abonent.objects.create(
            login=self.user,
            login_mikrotik='test_login',
            password='test_password',
            name='Test Abonent',
            account_number='123456',
            balance=100,
            group=self.group,
            ip_addr='192.168.0.1',
            block=False,
            create_date=datetime.now(),
            credit='1000x01-01-2023',
            email='test@example.com',
            phone='123456789',
            address='Test Address',
            passport='1234567890',
            description='Test Description'
        )
        self.event = UserEvent.objects.create(
            abonent=self.abonent,
            event='Test Event',
            comment='Test Comment',
            new_balance='150'
        )

    def test_string_representation(self):
        expected_string = f"Event for {self.abonent.login} on {self.event.date.strftime('%Y-%m-%d %H:%M:%S')}"
        self.assertEqual(str(self.event), expected_string)
