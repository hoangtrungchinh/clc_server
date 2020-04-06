from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url
from rest_framework.authtoken import views as v

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas.coreapi import AutoSchema

router = routers.DefaultRouter()
router.register(r'clcs', views.ClcViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^clc_collection/$', views.clc_collection),
    url(r'^get_tm_by_src/$', views.get_tm_by_src),
    url(r'^sign_up/$', views.sign_up),
    url(r'^get-token/', v.obtain_auth_token),
    path(r'docs/', include_docs_urls(title='CLC API')),
]
