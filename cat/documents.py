from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import TranslationMemory

@registry.register_document
class TranslationMemoryDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'translation_memory'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = TranslationMemory # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'id',
            'src',
            'tar',
        ]                   

        
#  Run to rebuild index
#  python3 manage.py search_index --rebuild
# https://github.com/sabricot/django-elasticsearch-dsl/blob/master/docs/source/quickstart.rst