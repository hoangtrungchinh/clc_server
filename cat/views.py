from django.shortcuts import render

from rest_framework import viewsets

from .models import (
    TranslationMemory,
    TMContent,
    GlossaryType,
    Glossary,
    GlossaryContent,
    Project,
    File,
)

from .serializers import (
    TranslationMemorySerializer,
    TMContentSerializer,
    GlossaryTypeSerializer,
    GlossarySerializer,
    GlossaryContentSerializer,
    ProjectSerializer,
    FileSerializer,
)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from django.contrib.auth.models import User

from django.http import JsonResponse, HttpResponse

from elasticsearch import Elasticsearch 
from elasticsearch_dsl import Search, Q

import json
from django.db import IntegrityError


class TranslationMemoryViewSet(viewsets.ModelViewSet):
    queryset = TranslationMemory.objects.all().order_by('id')
    serializer_class = TranslationMemorySerializer


class TMContentViewSet(viewsets.ModelViewSet):
    queryset = TMContent.objects.all()
    serializer_class = TMContentSerializer


class GlossaryTypeViewSet(viewsets.ModelViewSet):
    queryset = GlossaryType.objects.all()
    serializer_class = GlossaryTypeSerializer


class GlossaryViewSet(viewsets.ModelViewSet):
    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer


class GlossaryContentViewSet(viewsets.ModelViewSet):
    queryset = GlossaryContent.objects.all()
    serializer_class = GlossaryContentSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

      file_serializer = FileSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# class FileViewSet(viewsets.ModelViewSet):
#     queryset = File.objects.all()
#     serializer_class = FileSerializer


# @api_view(['GET','POST'])
# def clc_collection(request):
#     if request.method =='GET':
#         my_clc = clc.objects.all()
#         clc_serializer = ClcSerializer(my_clc,many=True)
#         return Response(clc_serializer.data)
#     elif request.method =='POST':
#         clc_serializer = ClcSerializer(data=request.data)
#         if clc_serializer.is_valid():
#             clc_serializer.save()
#             # post to Elasticsearch
            
#             return Response(clc_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(clc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def get_tm_by_src(request):
    try:
        _src=request.data["src"]

        client = Elasticsearch()      
        q = Q("match", src=_src) 
        s = Search(using=client, index="translation_memorys").query(q)[0:20] 
        res = s.execute()

        dict={}
        for i in range(len(res)):
            child={}
            child.update({"score": res[i].meta.score})
            child.update({"tar": res[i].tar})
            dict.update({i:child})

        j = {"is_success":True, "err_msg": None} 
        j.update({"result":dict})

        return HttpResponse(json.dumps(j, ensure_ascii=False),
            content_type="application/json",status=status.HTTP_200_OK)

    except Exception as e:
        j = {"is_success":False, "err_msg":  "Failed to Get data: "+str(e)}
        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    try:
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]

        # import pdb; pdb.set_trace()
        user = User.objects.create_user(username, email, password)
        token = Token.objects.create(user=user)

        j = {"id":user.id, "username":username, "email":email, "token": token.key }

        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_200_OK)

    except IntegrityError as e:
        j = {"is_success":False, "err_msg": username+" already exists"}
        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        j = {"is_success":False, "err_msg": ""+str(e)}
        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_400_BAD_REQUEST)
