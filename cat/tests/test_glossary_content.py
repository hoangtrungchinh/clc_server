from cat.tests.base import Base
from rest_framework import status
from cat import views
from cat.models import GlossaryContent, Glossary, GlossaryType
import copy

class TestGlossaryContent(Base):
    def setUp(self):
        self.view = views.GlossaryContentViewSet.as_view({'get': 'list'})
        self.uri = '/glossary_content/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # Create instance with params_default
        self.params_default = {
            "src_phrase": "Database",
            "tar_phrase": "Cơ sở dữ liệu",
            "glossary": 1
        }
        self.params = {
            "src_phrase": "Bộ nhớ",
            "tar_phrase": "storage",
            "glossary": 1
        }
        self.instance_glosstary_type = GlossaryType.objects.create(
            id=1,
            name="khtn",
            description="Khoa học tự nhiên",
        )
        self.instance_glossary_1=Glossary.objects.create(
            id = 1,
            name="TM1",
            description="des",
            src_lang="en",
            tar_lang="vi",
            user=self.user, 
            gloss_type=self.instance_glosstary_type,
        )
        self.instance_glossary_2=Glossary.objects.create(
            id=2,
            name="TM2",
            description="des",
            src_lang="vi",
            tar_lang="en",
            user=self.user,
            gloss_type=self.instance_glosstary_type,
        )
        self.instance = GlossaryContent.objects.create(
            src_phrase=self.params_default["src_phrase"],
            tar_phrase=self.params_default["tar_phrase"],
            glossary=self.instance_glossary_1,
        )




# VALID TESTS
    def test_get_all_glossary_content(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data[0]["id"]
        self.assertEqual(response.data, [self.params_default])    

    def test_get_glossary_content_by_id(self):
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data["id"]
        self.assertEqual(response.data, self.params_default)                   

    def test_create_glossary_content(self):
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)

    def test_update_glossary_content(self):
        response = self.client.put(self.uri + str(self.instance.id) + "/", self.params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)

    def test_delete_glossary_content(self):
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# INVALID TESTS
    def test_get_all_glossary_content_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_get_glossary_content_by_id_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_create_glossary_content_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["src_phrase"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["tar_phrase"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["glossary"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
        
    def test_create_glossary_content_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("src_phrase", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("tar_phrase", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("glossary", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_glossary_content_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["src_phrase"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["tar_phrase"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["glossary"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_update_glossary_content_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("src_phrase", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("tar_phrase", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("glossary", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_delete_glossary_content_without_login(self):
        self.client.credentials()
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
      