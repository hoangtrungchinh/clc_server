from cat.tests.base import Base
from rest_framework import status
from cat import views
from cat.models import GlossaryType, Glossary, TranslationMemory, Project, File, Sentence
from django.core.files import File as SysFile
from django.conf import settings
import os, copy

class TestSentence(Base):
    def setUp(self):
        self.view = views.SentenceViewSet.as_view({'get': 'list'})
        self.uri = '/sentence/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # Create instance with params_default
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
        self.instance_project=Project.objects.create(
            name="project 1",
            user=self.user,
            src_lang="en",
            tar_lang="vi",
            translate_service="GG",
        )
        self.instance_project.glossary.set([self.instance_glossary]),
        self.instance_project.translation_memory.set([self.instance_memory_1, self.instance_memory_2]),
        self.file = SysFile(open(os.path.join(os.path.abspath(os.path.dirname(__file__)),"data", '_ex_en.txt'), 'r'))

        self.instance_file=File.objects.create(
            project=self.instance_project,
            confirm=1,
            file=self.file,
        )

        self.params_default = {
            "file": self.instance_file.id,
            "src_str": "Tôi yêu em",
            "tar_str": "I love you",
            "score": 25,
            "is_confirmed": False,
            "tag": "ok"
        }

        self.params = {
            "file": self.instance_file.id,
            "src_str": "Tôi yêu em",
            "tar_str": "I love you",
            "score": 25,
            "is_confirmed": False,
            "tag": "ok"
        }

        self.instance=Sentence.objects.create(
            file=self.instance_file,
            src_str=self.params_default["src_str"],
            tar_str=self.params_default["tar_str"],
            score=self.params_default["score"],
            is_confirmed=self.params_default["is_confirmed"],
            tag=self.params_default["tag"],
        )
        
    def tearDown(self):
        if os.path.exists(self.instance_file.file.path):
            os.remove(self.instance_file.file.path)
  
# VALID TESTS
    def test_get_all_sentence(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data[0]["id"]
        self.assertEqual(response.data, [self.params_default])    

    def test_get_sentence_by_id(self):
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data["id"]
        self.assertEqual(response.data, self.params_default)              

    def test_create_sentence(self):
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)

    def test_update_sentence(self):
        response = self.client.put(self.uri + str(self.instance.id) + "/", self.params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)

    def test_delete_sentence(self):
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# # INVALID TESTS
    def test_get_all_sentence_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_get_sentence_by_id_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_create_sentence_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["file"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["src_str"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["tar_str"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        err_params = copy.copy(self.params)
        err_params["score"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        err_params = copy.copy(self.params)
        err_params["is_confirmed"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        err_params = copy.copy(self.params)
        err_params["tag"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
    def test_create_sentence_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("file", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("src_str", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("tar_str", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        err_params = copy.copy(self.params)
        err_params.pop("score", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        err_params = copy.copy(self.params)
        err_params.pop("is_confirmed", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        err_params = copy.copy(self.params)
        err_params.pop("tag", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_sentence_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["file"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["src_str"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["tar_str"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["score"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["is_confirmed"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["tag"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_update_sentence_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("file", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("src_str", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("tar_str", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)  
        err_params = copy.copy(self.params)
        err_params.pop("score", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("is_confirmed", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("tag", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_delete_sentence_without_login(self):
        self.client.credentials()
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
      