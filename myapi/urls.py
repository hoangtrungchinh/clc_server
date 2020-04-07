from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url
from rest_framework.authtoken import views as v

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas.coreapi import AutoSchema

from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'clcs', views.ClcViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^clc_collection/$', views.clc_collection),
    url(r'^get_tm_by_src/$', views.get_tm_by_src),
    url(r'^sign_up/$', views.sign_up),
    url(r'^get-token/', v.obtain_auth_token),
    
    url(r'^docs/', include_docs_urls(title='My API title', public=True))
]





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