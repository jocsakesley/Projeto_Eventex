import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):

    def setUp(self):
        self.obj = Subscription(
            nome='Jocsã Kesley',
            cpf='08838184429',
            email='jocsadm@gmail.com',
            telefone='088381844229',
        )
        self.obj.save()
    def test_create_model(self):
        self.assertTrue(Subscription.objects.exists())
    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime.datetime)

    def test_str(self):
        self.assertEqual("Jocsã Kesley", str(self.obj))

    def test_paid_dafault_to_false(self):
        self.assertEqual(False, self.obj.paid)