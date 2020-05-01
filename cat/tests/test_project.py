from cat.tests.base import Base
from rest_framework import status
from cat import views
from cat.models import GlossaryType, Glossary, TranslationMemory, Project

class TestProject(Base):
    def setUp(self):
        self.view = views.ProjectViewSet.as_view({'get': 'list'})
        self.uri = '/project/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.instance_glosstary_type1 = GlossaryType.objects.create(
            id=1,
            name="khtn",
            description="Khoa học tự nhiên",
        )
        
        self.instance_glossary=Glossary.objects.create(
            id=1,
            name="Glossary 1",
            description="des",
            src_lang="en",
            tar_lang="vi",
            user=self.user,
            gloss_type=self.instance_glosstary_type1,
        )
        self.instance_memory_1=TranslationMemory.objects.create(
            id = 1,
            name="TM1",
            description="des",
            src_lang="en",
            tar_lang="vi",
            user=self.user
        )
        
        self.instance_memory_2=TranslationMemory.objects.create(
            id = 2,
            name="TM2",
            description="des",
            src_lang="vi",
            tar_lang="en",
            user=self.user
        )

        self.params_default = {
            "name": "project 1",
            "user": 1,
            "src_lang": "en",
            "tar_lang": "vi",
            "translate_service": "GG",
            "translation_memory": [1,2],
            "glossary": [1]
        }

        self.params = {
            "name": "project 2",
            "user": 1,
            "src_lang": "vi",
            "tar_lang": "en",
            "translate_service": "Bing",
            "translation_memory": [1],
            "glossary": [1]
        }
        # Create instance with params_default
        self.instance=Project.objects.create(
            name=self.params_default["name"],
            user=self.user,
            src_lang=self.params_default["src_lang"],
            tar_lang=self.params_default["tar_lang"],
            translate_service=self.params_default["translate_service"],
        )
        self.instance.glossary.set([self.instance_glossary]),
        self.instance.translation_memory.set([self.instance_memory_1, self.instance_memory_2]),


# VALID TESTS
    def test_get_all_project(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data[0]["id"]
        self.assertEqual(response.data, [self.params_default])    

    def test_get_project_by_id(self):
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data["id"]
        self.assertEqual(response.data, self.params_default)                   

    def test_create_project(self):
        response = self.client.post(self.uri, self.params)
        # import pdb; pdb.set_trace() 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)

    def test_update_project(self):
        response = self.client.put(self.uri + str(self.instance.id) + "/", self.params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)

    def test_delete_project(self):
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# # INVALID TESTS
    def test_get_all_project_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_get_project_by_id_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  


    def test_create_project_with_duplicate_name(self):
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_project_with_empty_fields(self):
        err_params = self.params
        err_params["name"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params["user"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params["src_lang"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params["tar_lang"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params["translate_service"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params["translation_memory"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params["glossary"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # import pdb; pdb.set_trace() 
    def test_create_project_without_fields(self):
        err_params = self.params
        err_params.pop("name", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params.pop("user", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params.pop("src_lang", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params.pop("tar_lang", None)
        response = self.client.post(self.uri, err_params)        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params.pop("translate_service", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params.pop("translation_memory", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = self.params
        err_params.pop("glossary", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_project_with_empty_fields(self):
        err_params = self.params
        err_params["name"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params["user"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params["src_lang"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params["tar_lang"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params["translate_service"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params["translation_memory"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params["glossary"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


        # import pdb; pdb.set_trace() 
    def test_update_project_without_fields(self):
        err_params = self.params
        err_params.pop("name", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params.pop("user", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params.pop("src_lang", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params.pop("tar_lang", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params.pop("translate_service", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params.pop("translation_memory", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = self.params
        err_params.pop("glossary", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_project_without_login(self):
        self.client.credentials()
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
      