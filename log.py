# https://medium.com/@BennettGarner/build-your-first-rest-api-with-django-rest-framework-e394e39a482c

django-admin startproject mysite
cd mysite/

python3 manage.py startapp myapi

# Add to setting.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myapi',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

#update to DB
python3 manage.py migrate

# add to setting.py
INSTALLED_APPS = [
    'myapi.apps.MyapiConfig'
]

#run server
python3 manage.py runserver



#update to DB
python3 manage.py migrate

# create superuser to login    
python3 manage.py createsuperuser
    Username: chinh
    Email address: chinhguitar@gmail.com
    Password: 123456789

# Add to models.py
from django.db import models
class clc(models.Model):
    src = models.TextField()
    tar = models.TextField()
    
    def __str__(self):
        return self.src + " | " + self.tar



# create migration
python3 manage.py makemigrations
    # Migrations for 'myapi':
    # myapi/migrations/0001_initial.py
    #     - Create model clc


# update to DB
python3 manage.py migrate
    # Operations to perform:
    #   Apply all migrations: admin, auth, contenttypes, myapi, sessions
    # Running migrations:
    #   Applying myapi.0001_initial... OK


# Add to myapi/admin.py to Register clc
from .models import Clc
admin.site.register(Clc)



# add to setting.py
INSTALLED_APPS = [
    'myapi.apps.MyapiConfig'
    'rest_framework',
]



# add to myapi/serializers.py
from rest_framework import serializers
from .models import clc
class ClcSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = clc
        fields = ('src', 'tar')


# add to views.py
from rest_framework import viewsets
from .serializers import ClcSerializer
from .models import clc

class ClcViewSet(viewsets.ModelViewSet):
    queryset = clc.objects.all().order_by('tar')
    serializer_class = ClcSerializer



#add to mysite/url.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapi.urls')),
]




#add to myapi/url.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'clcs', views.ClcViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]



