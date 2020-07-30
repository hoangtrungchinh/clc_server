from cat.tests.base import Base
from rest_framework import status
from cat import views
from cat.models import GlossaryType, Glossary
import copy

class TestGlossary(Base):
    def setUp(self):
        self.view = views.GlossaryViewSet.as_view({'get': 'list'})
        self.uri = '/glossary/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.instance_glosstary_type1 = GlossaryType.objects.create(
            id=1,
            name="khtn",
            description="Khoa học tự nhiên",
            user=self.user,
        )
        self.instance_glosstary_type2 = GlossaryType.objects.create(
            id=2,
            name="khxhnv",
            description="Khoa học xã hội nhân văn",
            user=self.user,
        )
        self.params_default = {
            "name": "Glossary 10",
            "description": "des",
            "src_lang": "en",
            "tar_lang": "vi",
            "user": 1,
            "gloss_type": 1,
        }
        self.params = {
            "name": "Glossary 11",
            "description": "des",
            "src_lang": "vi",
            "tar_lang": "en",
            "user": 1,
            "gloss_type": [2],
        }
        # Create instance with params_default
        self.instance=Glossary.objects.create(
            name=self.params_default["name"],
            description=self.params_default["description"],
            src_lang=self.params_default["src_lang"],
            tar_lang=self.params_default["tar_lang"],
            user=self.user,
        )
        self.instance.gloss_type.set([self.instance_glosstary_type1]),


# VALID TESTS
    def test_get_all_glossary(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_get_glossary_by_id(self):
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)               

    def test_create_glossary(self):
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_glossary(self):
        response = self.client.put(self.uri + str(self.instance.id) + "/", self.params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_glossary(self):
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# INVALID TESTS
    def test_get_all_glossary_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_get_glossary_by_id_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  


    def test_create_glossary_with_duplicate_name(self):
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_glossary_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["name"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["description"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["src_lang"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["tar_lang"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["user"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["gloss_type"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_glossary_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("name", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("description", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("src_lang", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("tar_lang", None)
        response = self.client.post(self.uri, err_params)        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("user", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("gloss_type", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_glossary_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["name"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["description"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["src_lang"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["tar_lang"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["user"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["gloss_type"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_glossary_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("name", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("description", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("src_lang", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("tar_lang", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("user", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("gloss_type", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_glossary_without_login(self):
        self.client.credentials()
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
      