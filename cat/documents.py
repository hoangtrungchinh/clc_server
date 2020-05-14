from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import TranslationMemory, TMContent, Glossary, GlossaryContent, GlossaryType

@registry.register_document
class TMContentDocument(Document):   
    class Index:
        name = 'translation_memory'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = TMContent 
        fields = [
            'id',
            'src_sentence',
            'tar_sentence',
        ]       
        related_models = [TranslationMemory]         

    translation_memory = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
        'src_lang': fields.TextField(),
        'tar_lang': fields.TextField(),
        'user' : fields.TextField(attr="get_user_id"),
    })



@registry.register_document
class GlossaryContentDocument(Document):   
    class Index:
        name = 'glossary'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = GlossaryContent 
        fields = [
            'id',
            'src_phrase',
            'tar_phrase',
        ]       
        related_models = [Glossary, GlossaryType]


    glossary = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
        'src_lang': fields.TextField(),
        'tar_lang': fields.TextField(),
        'user' : fields.TextField(attr="get_user_id"),
        'gloss_type': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'description': fields.TextField(),
        })
    })



#  Run to rebuild index
#  python3 manage.py search_index --rebuild
# https://github.com/sabricot/django-elasticsearch-dsl/blob/master/docs/source/quickstart.rst