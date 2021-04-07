from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionsForm
# Create your tests here.


class SubscriptionGet(TestCase):
    def setUp(self):
        self.response = self.client.get("/inscricao/")

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(
            self.response, "subscriptions/subscription_form.html")

    def test_html(self):
        tags = (
            ("<form", 1),
            ("<input", 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrftoken(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionsForm)


class SubscriptionsPostValid(TestCase):
    def setUp(self):
        data = dict(name='Jocsã Kesley', cpf='08838184429',
                    email='jocsa_kesley@yahoo.com.br', phone='84996203426')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_post_form(self):
        self.assertEqual(302, self.response.status_code)

    def test_email_post(self):
        self.assertEqual(1, len(mail.outbox))


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(
            self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionsForm)

    def test_from_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Jocsã Kesley', cpf='08838184429',
                    email='jocsa_kesley@yahoo.com.br', phone='84996203426')
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, "Inscrição realizada com sucesso!")
