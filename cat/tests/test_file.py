from cat.tests.base import Base
from rest_framework import status
from cat import views
from cat.models import GlossaryType, Glossary, TranslationMemory, Project, File
from django.core.files import File as SysFile
import os, copy
from django.conf import settings

class TestFile(Base):
    def setUp(self):
        self.view = views.FileUploadView.as_view()
        self.uri = '/file/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # Create instance with params_default
        self.instance_glosstary_type1 = GlossaryType.objects.create(
            id=1,
            name="khtn",
            description="Khoa học tự nhiên",
            user=self.user
        )
        
        self.instance_glossary=Glossary.objects.create(
            id=1,
            name="Glossary 1",
            description="des",
            src_lang=settings.ENGLISH,
            tar_lang=settings.VIETNAMESE,
            user=self.user,
        )
        self.instance_glossary.gloss_type.set([self.instance_glosstary_type1]),

        self.instance_memory_1=TranslationMemory.objects.create(
            id = 1,
            name="TM1",
            description="des",
            src_lang=settings.ENGLISH,
            tar_lang=settings.VIETNAMESE,
            user=self.user
        )
        
        self.instance_memory_2=TranslationMemory.objects.create(
            id = 2,
            name="TM2",
            description="des",
            src_lang=settings.VIETNAMESE,
            tar_lang=settings.ENGLISH,
            user=self.user
        )
        self.instance_project=Project.objects.create(
            name="project 1",
            user=self.user,
            src_lang=settings.ENGLISH,
            tar_lang=settings.VIETNAMESE,
            translate_service="GG",
            writable_translation_memory=self.instance_memory_1
        )
        self.instance_project.glossary.set([self.instance_glossary]),
        self.instance_project.searchable_translation_memory.set([self.instance_memory_1, self.instance_memory_2]),
        self.file = SysFile(open(os.path.join(os.path.abspath(os.path.dirname(__file__)),"data", '_ex_en.txt'), 'r'))

        self.params_default = {
            "project": self.instance_project.id,
            "confirm": 1,
            "file": SysFile(open(os.path.join(os.path.abspath(os.path.dirname(__file__)),"data", '_ex_en.txt'), 'r')),
        }

        self.params = {
            "project": self.instance_project.id,
            "confirm": 2,
            "file": SysFile(open(os.path.join(os.path.abspath(os.path.dirname(__file__)),"data", '_ex_en.txt'), 'r')),
        }
        
        self.instance=File.objects.create(
            project=self.instance_project,
            confirm=self.params_default["confirm"],
            file=self.file,
        )
        
    def tearDown(self):
        if os.path.exists(self.instance.file.path):
            os.remove(self.instance.file.path)
  
# VALID TESTS
    def test_get_all_file(self):
        response = self.client.get(self.uri+'?project_id='+str(self.instance_project.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.params_default["confirm"], response.data[0]["confirm"])    

    def test_get_file_by_id(self):
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.params_default["confirm"], response.data["confirm"])                

    def test_create_file(self):
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if os.path.exists(response.data['file']):
            os.remove(response.data['file'])
  

    def test_update_file(self):
        response = self.client.put(self.uri + str(self.instance.id) + "/", self.params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_file(self):
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# # INVALID TESTS
    def test_get_all_file_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_get_file_by_id_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_create_file_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["project"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["confirm"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params["file"] = ""
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
    def test_create_file_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("project", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("confirm", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        err_params = copy.copy(self.params)
        err_params.pop("file", None)
        response = self.client.post(self.uri, err_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_file_with_empty_fields(self):
        err_params = copy.copy(self.params)
        err_params["project"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["confirm"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params["file"] = ""
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_update_file_without_fields(self):
        err_params = copy.copy(self.params)
        err_params.pop("project", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("confirm", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        err_params = copy.copy(self.params)
        err_params.pop("file", None)
        response = self.client.post(self.uri + str(self.instance.id) + "/", err_params)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_delete_file_without_login(self):
        self.client.credentials()
        response = self.client.delete(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
      