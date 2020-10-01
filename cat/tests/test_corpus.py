from cat.tests.base import Base
from rest_framework import status
from cat import views
from cat.models import Corpus
import copy
from django.conf import settings
class TestCorpus(Base):
  def setUp(self):
    self.view = views.CorpusViewSet.as_view({'get': 'list'})
    self.uri = '/corpus/'
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    self.params_default = {
      "name": "CORPUS_1",
      "description": "des",
      "language": settings.VIETNAMESE,
      "user": 1
    }
    self.params = {
      "name": "CORPUS_2",
      "description": "des",
      "language": settings.ENGLISH,
      "user": 1
    }
    # Create instance with params_default
    self.instance=Corpus.objects.create(
      name=self.params_default["name"],
      description=self.params_default["description"],
      language=self.params_default["language"],
      user=self.user
    )

# VALID TESTS
  def test_get_all_corpus(self):
    response = self.client.get(self.uri)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.params_default["id"]=response.data[0]["id"]
    self.assertEqual(response.data, [self.params_default])

  def test_get_corpus_by_id(self):
    response = self.client.get(self.uri + str(self.instance.id) + "/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.params_default["id"]=response.data["id"]
    self.assertEqual(response.data, self.params_default)

  def test_create_corpus(self):
    response = self.client.post(self.uri, self.params)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.params["id"]=response.data["id"]
    self.assertEqual(response.data, self.params)

  def test_update_corpus(self):
    response = self.client.put(self.uri + str(self.instance.id) + "/", self.params)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.params["id"]=response.data["id"]
    self.assertEqual(response.data, self.params)

  def test_delete_corpus(self):
    response = self.client.delete(self.uri + str(self.instance.id) + "/")
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# INVALID TESTS
  def test_get_all_corpus_without_login(self):
    self.client.credentials()
    response = self.client.get(self.uri)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_get_corpus_by_id_without_login(self):
    self.client.credentials()
    response = self.client.get(self.uri + str(self.instance.id) + "/")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_create_corpus_with_empty_fields(self):
    err_params = copy.copy(self.params)
    err_params["name"] = ""
    response = self.client.post(self.uri, err_params)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    err_params = copy.copy(self.params)
    err_params["description"] = ""
    response = self.client.post(self.uri, err_params)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    err_params = copy.copy(self.params)
    err_params["language"] = ""
    response = self.client.post(self.uri, err_params)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    err_params = copy.copy(self.params)
    err_params["user"] = ""
    response = self.client.post(self.uri, err_params)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_corpus_without_fields(self):
    err_params = copy.copy(self.params)
    err_params.pop("name", None)
    response = self.client.post(self.uri, err_params)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    err_params = copy.copy(self.params)
    err_params.pop("description", None)
    response = self.client.post(self.uri, err_params)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    err_params = copy.copy(self.params)
    err_params.pop("language", None)
    response = self.client.post(self.uri, err_params)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    err_params = copy.copy(self.params)
    err_params.pop("user", None)
    response = self.client.post(self.uri, err_params)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_update_corpus_with_empty_fields(self):
    err_params = copy.copy(self.params)
    err_params["name"] = ""
    response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    err_params = copy.copy(self.params)
    err_params["description"] = ""
    response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    err_params = copy.copy(self.params)
    err_params["language"] = ""
    response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    err_params = copy.copy(self.params)
    err_params["user"] = ""
    response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

  def test_update_corpus_without_fields(self):
    err_params = copy.copy(self.params)
    err_params.pop("name", None)
    response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    err_params = copy.copy(self.params)
    err_params.pop("description", None)
    response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    err_params = copy.copy(self.params)
    err_params.pop("language", None)
    response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    err_params = copy.copy(self.params)
    err_params.pop("user", None)
    response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

  def test_delete_corpus_without_login(self):
    self.client.credentials()
    response = self.client.delete(self.uri + str(self.instance.id) + "/")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
