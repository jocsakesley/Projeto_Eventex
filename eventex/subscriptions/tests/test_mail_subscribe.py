from django.test import TestCase
from django.core import mail


class SubscriptionsPostValid(TestCase):
    def setUp(self):
        data = dict(name='Jocsã Kesley', cpf='08838184429',
                    email='jocsa_kesley@yahoo.com.br', phone='84996203426')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual("Confirmação da Incrição", self.email.subject)

    def test_email_from(self):
        self.assertEqual("jocsadm@gmail.com", self.email.from_email)

    def test_email_to(self):
        self.assertEqual(
            ['jocsadm@gmail.com', 'jocsa_kesley@yahoo.com.br'], self.email.to)

    def test_email_body(self):
        contents = ['Jocsã Kesley', '08838184429',
                    'jocsa_kesley@yahoo.com.br', '84996203426']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
