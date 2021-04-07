<<<<<<< HEAD
from django.test import TestCase

class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')
    def test_get(self):
        self.assertEqual(200, self.response.status_code)
    def test_template(self):
        self.assertTemplateUsed(self.response, 'index.html')
    def test_subscription_link(self):
        self.assertContains(self.response, 'href="/inscricao/"')
=======
from django.test import TestCase
from django.shortcuts import resolve_url as r

class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('home'))
    def test_status(self):
        self.assertEqual(200, self.response.status_code)
    def test_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        expected ='href="{}"' .format(r('subscriptions:new'))
        self.assertContains(self.response, expected)
>>>>>>> aca268c631696747785d45fece78bf666b8ad7f7
