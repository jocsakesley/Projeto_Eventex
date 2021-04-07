from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(nome='Jocsã Kesley', cpf='08838184429', telefone='84996203426', email='jocsa_kesley@yahoo.com')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]
    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)
    def test_subscription_email_from(self):
        expect = 'jocsadm@gmail.com'
        self.assertEqual(expect, self.email.from_email)
    def test_subscription_email_to(self):
        expect = ['jocsa_kesley@yahoo.com', 'jocsadm@gmail.com']
        self.assertEqual(expect, self.email.to)
    def test_subscription_email_body(self):
        contents = ['Jocsã Kesley', '08838184429', '84996203426', 'jocsa_kesley@yahoo.com']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
