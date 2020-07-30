from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import TranslationMemory, TMContent, Glossary, GlossaryContent, GlossaryType, Corpus, CorpusContent
from django.conf import settings

@registry.register_document
class TMContentDocument(Document):   
    class Index:
        name = settings.INDEX_TM
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

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the instance(s) from the related model."""
        if isinstance(related_instance, TranslationMemory):
            return related_instance.tmcontent_set.all()

@registry.register_document
class CorpusContentDocument(Document):   
    class Index:
        name = settings.INDEX_CORPUS
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = CorpusContent 
        fields = [
            'id',
            'phrase',
        ]       
        related_models = [Corpus]         

    corpus = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
        'language': fields.TextField(),
        'user' : fields.TextField(attr="get_user_id"),
    })

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the instance(s) from the related model."""
        if isinstance(related_instance, Corpus):
            return related_instance.corpuscontent_set.all()


@registry.register_document
class GlossaryContentDocument(Document):   
    class Index:
        name = settings.INDEX_GLOSSARY
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

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the instance(s) from the related model."""
        if isinstance(related_instance, Glossary):
            return related_instance.glossarycontent_set.all()

#  Run to rebuild index
#  python3 manage.py search_index --rebuild
# https://github.com/sabricot/django-elasticsearch-dsl/blob/master/docs/source/quickstart.rst
