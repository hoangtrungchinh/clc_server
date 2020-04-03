from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'clcs', views.ClcViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^clc_collection/$', views.clc_collection),
    url(r'^clc_get_by_src/$', views.clc_get_by_src)

]
