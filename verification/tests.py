from django.test import TestCase
from unittest import mock
from django.core.mail import send_mail
from verification.models import User, Registration
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from verification.utils import send_code
# Create your tests here.
class TestSendEmail(TestCase):
    def setUp(self):
        email = 'tornadoalert2@gmail.com'
        user = User.objects.create_user(email, email=email)
        self.user = user
        self.client = APIClient()
        
    def test_createUser(self):
        return # Since it sends email
        with mock.patch('verification.utils.send_code') as mock_send_code:
            r = self.client.post(
                '/api/verify/',
                data={
                    "email":"tornadoalert@gmail.com",
                    "publicKey":"123",
                    "privateKey":"123"
                }, format= 'json'
            )
        self.assertIsNotNone(User.objects.get(username='tornadoalert@gmail.com'))

    def test_activateUser(self):
        user = self.user
        Registration.objects.create(publicKey="123",privateKey="123",user=user)
        url = '/api/verify/tornadoalert2@gmail.com/{}'.format(self.user.confirmation_key)
        r = self.client.get(url)
        self.assertTrue(self.user.is_confirmed)