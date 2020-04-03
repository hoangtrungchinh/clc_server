from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import clc

@registry.register_document
class ClcDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'clc'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = clc # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'id',
            'src',
            'tar',
        ]                   

        
#  Run to rebuild index
#  python3 manage.py search_index --rebuild