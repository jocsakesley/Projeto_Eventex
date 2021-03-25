from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionsForm
# Create your tests here.
class SubscriptionsTest(TestCase):
    def setUp(self):
        self.response = self.client.get("/inscricao/")
    def test_get_subscription(self):
        self.assertEqual(200, self.response.status_code)
    def test_template_subscription(self):
        self.assertTemplateUsed(self.response, "subscriptions/subscription_form.html")

    def test_form(self):
        self.assertContains(self.response, "<input", 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')
    def test_csrftoken(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionsForm)

class SubscriptionsPostValid(TestCase):
    def setUp(self):
        data = dict(name='Jocsã Kesley', cpf='08838184429',email='jocsa_kesley@yahoo.com.br', phone='84996203426')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]
    def test_post_form(self):
        self.assertEqual(302, self.response.status_code)
    def test_email_post(self):
        self.assertEqual(1, len(mail.outbox))
    def test_email_subject(self):
        self.assertEqual("Confirmação da Incrição", self.email.subject)
    def test_email_from(self):
        self.assertEqual("jocsadm@gmail.com", self.email.from_email)
    def test_email_to(self):
        self.assertEqual(['jocsadm@gmail.com', 'jocsa_kesley@yahoo.com.br'], self.email.to)
    def test_email_body(self):
        contents = ['Jocsã Kesley', '08838184429', 'jocsa_kesley@yahoo.com.br', '84996203426']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
