from cat.tests.base import Base
from rest_framework import status
from cat import views
from cat.models import TMContent, TranslationMemory
import copy

class TestTMContent(Base):
    def setUp(self):
        self.view = views.TMContentViewSet.as_view({'get': 'list'})
        self.uri = '/tm_content/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # Create instance with params_default
        self.params_default = {
            "src_sentence": "Love in your eyes",
            "tar_sentence": "Tình yêu trong mắt em",
            "translation_memory": 1
        }
        self.params = {
            "src_sentence": "I go to school",
            "tar_sentence": "Tôi đi đến trường",
            "translation_memory": 1
        }
        self.instance_memory_1=TranslationMemory.objects.create(
            id = 1,
            name="TM1",
            description="des",
            src_lang="en",
            tar_lang="vi",
            user=self.user
        )
        self.instance_memory_2=TranslationMemory.objects.create(
            id=2,
            name="TM2",
            description="des",
            src_lang="vi",
            tar_lang="en",
            user=self.user
        )
        self.instance = TMContent.objects.create(
            src_sentence=self.params_default["src_sentence"],
            tar_sentence=self.params_default["tar_sentence"],
            translation_memory=self.instance_memory_1,
        )




# VALID TESTS
    def test_get_all_tm_content(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data[0]["id"]
        self.assertEqual(response.data, [self.params_default])    

    def test_get_tm_content_by_id(self):
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data["id"]
        self.assertEqual(response.data, self.params_default)                   

    def test_create_tm_content(self):
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)

    def test_update_tm_content(self):
        response = self.client.put(self.uri + str(self.instance.id) + "/", self.params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)

    def test_delete_tm_content(self):
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# INVALID TESTS
    def test_get_all_tm_content_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_get_tm_content_by_id_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_create_tm_content_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["src_sentence"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["tar_sentence"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["translation_memory"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
        
    def test_create_tm_content_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("src_sentence", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("tar_sentence", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("translation_memory", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_tm_content_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["src_sentence"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["tar_sentence"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["translation_memory"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_update_tm_content_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("src_sentence", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("tar_sentence", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("translation_memory", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_delete_tm_content_without_login(self):
        self.client.credentials()
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
      