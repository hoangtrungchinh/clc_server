from django.test import TestCase
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
# run this command "python3 manage.py test cat.tests" to run all test

class Base(APITestCase):
  # this method only load 1 time when run test


  @classmethod
  def setUpTestData(cls):
    cls.client = APIClient()
    cls.user = cls.setup_user()
    cls.token = cls.get_token()

  @staticmethod
  def setup_user():
    User = get_user_model()
    return User.objects.create_user(
      id=1,
      username="test",
      email="testuser@test.com",
      password="test"
    )

  @staticmethod
  def get_token():
    static_user = {
      "username":"test",
      "email":"testuser@test.com",
      "password":"test"
    }
    client = APIClient()
    response = client.post("/sign_in/", static_user)
    return response.data["access"]

