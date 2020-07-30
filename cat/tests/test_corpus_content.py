from cat.tests.base import Base
from rest_framework import status
from cat import views
from cat.models import CorpusContent, Corpus
import copy

class TestCorpusContent(Base):
    def setUp(self):
        self.view = views.CorpusContentViewSet.as_view({'get': 'list'})
        self.uri = '/corpus_content/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # Create instance with params_default
        self.params_default = {
            "phrase": "Tình yêu trong mắt em",
            "corpus": 1
        }
        self.params = {
            "phrase": "Tôi đi đến trường",
            "corpus": 1
        }
        self.instance_corpus_1=Corpus.objects.create(
            id = 1,
            name="Corpus_1",
            description="des",
            language="en",
            user=self.user
        )
        self.instance_corpus_2=Corpus.objects.create(
            id=2,
            name="Corpus_2",
            description="des",
            language="vi",
            user=self.user
        )
        self.instance = CorpusContent.objects.create(
            phrase=self.params_default["phrase"],
            corpus=self.instance_corpus_1,
        )




# VALID TESTS
    def test_get_all_corpus_content(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data[0]["id"]
        self.assertEqual(response.data, [self.params_default])    

    def test_get_corpus_content_by_id(self):
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data["id"]
        self.assertEqual(response.data, self.params_default)                   

    def test_create_corpus_content(self):
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)

    def test_update_corpus_content(self):
        response = self.client.put(self.uri + str(self.instance.id) + "/", self.params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)

    def test_delete_corpus_content(self):
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# INVALID TESTS
    def test_get_all_corpus_content_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_get_corpus_content_by_id_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_create_corpus_content_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["phrase"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["corpus"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_corpus_content_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("phrase", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("corpus", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_corpus_content_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["phrase"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["corpus"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_update_corpus_content_without_fields(self):
        err_params = copy.copy(self.params)
        err_params = copy.copy(self.params)
        err_params.pop("phrase", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("corpus", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_delete_corpus_content_without_login(self):
        self.client.credentials()
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
      