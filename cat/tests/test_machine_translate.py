from cat.tests.base import Base
from rest_framework import status
from cat import views
import copy, json

class TestMachineTranslate(Base):
    def setUp(self):
        # self.view = views.machine_translate.as_view()
        self.uri = '/machine_translate/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.params = {
            "src_lang": "en",
            "tar_lang": "vi",
            "sentence": "I love you so much!"
        }

# VALID TESTS
    def test_translate(self):
        response = self.client.generic(method="GET", path=self.uri, data=json.dumps(self.params), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        byte_str = response.content
        dict_str = byte_str.decode("UTF-8")    
        data = json.loads(dict_str)
        self.assertEqual(data["is_success"], True)

# INVALID TESTS
    def test_translate_without_login(self):
        self.client.credentials()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
