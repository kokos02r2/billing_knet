from django.test import TestCase
from django.urls import reverse
from apps.abonents.models import Abonent, Group
from django.contrib.auth.models import User
from datetime import datetime


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.abonent = Abonent.objects.create(login=self.user, balance=100)

    def test_profile_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.abonent.balance)
        self.assertContains(response, datetime.now().month)


class AddFundsToAbonentViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.abonent = Abonent.objects.create(login=self.user, balance=100)

    def test_add_funds_to_abonent_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_funds_to_abonent', kwargs={'abonent_id': self.abonent.id}),
                                    {'amount': 50})
        self.assertEqual(response.status_code, 302)  # Redirects after successful POST


class ChangeTarifViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.abonent = Abonent.objects.create(login=self.user, balance=100)
        self.group = Group.objects.create(group_name='testgroup', month_price=50)

    def test_change_tarif_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('change_tarif', kwargs={'abonent_id': self.abonent.id}),
                                    {'new_tariff': self.group.group_name})
        self.assertEqual(response.status_code, 302)  # Redirects after successful POST
