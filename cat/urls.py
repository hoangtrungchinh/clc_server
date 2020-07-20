from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url
from rest_framework.authtoken import views as v

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas.coreapi import AutoSchema

from django.contrib import admin

from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'translation_memory', views.TranslationMemoryViewSet, basename='translation_memory')
router.register(r'tm_content', views.TMContentViewSet, basename='tm_content')
router.register(r'glossary_type', views.GlossaryTypeViewSet, basename='glossary_type')
router.register(r'glossary', views.GlossaryViewSet, basename='glossary')
router.register(r'glossary_with_child', views.GlossaryWithChildViewSet, basename='glossary_with_child')
router.register(r'glossary_content', views.GlossaryContentViewSet, basename='glossary_content')
router.register(r'project', views.ProjectViewSet, basename='project')
router.register(r'sentence', views.SentenceViewSet, basename='sentence')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('file/', FileUploadView.as_view()),  
    path('file/<int:pk>/', FileUploadDetailView.as_view()),  
    path('tm_content_import/', ImportTMView.as_view()),  
    path('glossary_content_import/', ImportGlossaryView.as_view()),  
    url(r'^file_download/$', views.file_download),
    # url(r'^clc_collection/$', views.clc_collection),
    url(r'^get_tm_by_src_sentence/$', views.get_tm_by_src_sentence),
    url(r'^get_glossary_by_src_sentence/$', views.get_glossary_by_src_sentence),
    url(r'^machine_translate/$', views.machine_translate),
    
    url(r'^docs/', include_docs_urls(title='My API title', public=True)),



   #  url(r'^login/', views.login.as_view()),
    url(r'^sign_up/$', views.sign_up),
    path('sign_in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]