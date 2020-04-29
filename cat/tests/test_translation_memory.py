from cat.tests.base import Base
from rest_framework import status
from cat import views
from cat.models import TranslationMemory

class TestTranslationMemory(Base):
    def setUp(self):
        self.view = views.TranslationMemoryViewSet.as_view({'get': 'list'})
        self.uri = '/translation_memories/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.params_default = {
            "name": "TM1",
            "description": "des",
            "src_lang": "en",
            "tar_lang": "vi",
            "user": 1
        }
        self.params = {
            "name": "TM2",
            "description": "des",
            "src_lang": "vi",
            "tar_lang": "en",
            "user": 1
        }
        # Create instance with params_default
        self.instance=TranslationMemory.objects.create(
            name=self.params_default["name"],
            description=self.params_default["description"],
            src_lang=self.params_default["src_lang"],
            tar_lang=self.params_default["tar_lang"],
            user=self.user
        )


    def test_get_all_TM(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data[0]["id"]
        self.assertEqual(response.data, [self.params_default])    

    def test_get_all_TM_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)                  
    
    def test_get_TM_by_id(self):
        response = self.client.get(self.uri + str(self.instance.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.params_default["id"]=response.data["id"]
        self.assertEqual(response.data, self.params_default)                   


    def test_create_TM(self):
        response = self.client.post(self.uri, self.params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.params["id"]=response.data["id"]
        self.assertEqual(response.data, self.params)