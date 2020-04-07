from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from myapi import views

class TestClc(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.ClcViewSet.as_view({'get': 'list'})
        self.uri = '/clcs/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
    
    def get_tm_list(self):
        request = self.factory.get(self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
            'Expected Response Code 200, received {0} instead.'
            .format(response.status_code))

    def get_tm_list_without_token(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 401,
            'Expected Response Code 200, received {0} instead.'
            .format(response.status_code))


    def create_tm(self):
        self.client.login(username="test", password="test")
        params = {
            "src": "How are you?",
            "tar": "Bạn khỏe không?"
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201,
            'Expected Response Code 201, received {0} instead.'
            .format(response.status_code))
                    