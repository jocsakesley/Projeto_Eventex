from django.test import TestCase
from eventex.subscriptions.forms import SubscribeForm
from django.core import mail
from django.shortcuts import resolve_url as r

from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r('subscriptions:new'))
    def test_get(self):
        '''Get '/inscricao/' must return status code '200' '''
        self.assertEqual(200, self.response.status_code)
    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')
    def test_html(self):
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)


    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscribeForm)


class SubscriptionsNewPostValid(TestCase):
    def setUp(self):
        data = dict(nome='Jocsã Kesley', cpf='08838184429', telefone='84996203426', email='jocsadm@gmail.com')
        self.response = self.client.post(r('subscriptions:new'), data)
    def test_post(self):
        self.assertEqual(302, self.response.status_code)
        self.assertRedirects(self.response, r('subscriptions:detail', 1))
    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))
    def test_save_model(self):
        self.assertTrue(Subscription.objects.exists())

class SubscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post(r('subscriptions:new'), {})
    def test_invalid_post(self):
        self.assertEqual(200, self.response.status_code)
    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')
    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscribeForm)
    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)
    def test_dont_save_model(self):
        self.assertFalse(Subscription.objects.exists())

