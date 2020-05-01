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
    Sentence,
)

from .serializers import (
    TranslationMemorySerializer,
    TMContentSerializer,
    GlossaryTypeSerializer,
    GlossarySerializer,
    GlossaryContentSerializer,
    ProjectSerializer,
    FileSerializer,
    SentenceSerializer,
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
import os

from django.db import IntegrityError
from django.conf import settings

import sys
sys.path.append(os.path.join(settings.BASE_DIR,'preprocessing_python'))
from preprocessor import *

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


class SentenceViewSet(viewsets.ModelViewSet):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if "file" not in request.data:
            return Response({"file":["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)          
        if serializer.is_valid():
            uf = serializer.save()
            # Read from file
            inp_path = os.path.join(settings.BASE_DIR, uf.file.path)
            with open(inp_path, 'r', encoding='utf8') as f:
                text = f.read()
            
            # Find src_lang
            # import pdb; pdb.set_trace()
            project = Project.objects.get(pk=uf.project.id)
            if project.src_lang == "vi":
                p = Preprocessor(Language.vietnamese)    
            elif project.src_lang == "en":
                p = Preprocessor(Language.english)    

            sents = p.segment_to_sentences(text)
            sents_cnt = len(sents)
            
            for idx in range(0, sents_cnt):                
                sentence_serilizer = SentenceSerializer(data = {"src_str":sents[idx],"file":uf.id})
                if sentence_serilizer.is_valid():
                    sentence_serilizer.save()


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response (serializer.data)

class FileUploadDetailView(APIView):
    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileSerializer(file)
        return Response(serializer.data)       

    def put(self, request, pk, format=None):
        file = self.get_object(pk)
        # Dont update upload file by remove it from request
        if "file" in request.data:
            del request.data["file"]

        serializer = FileSerializer(file, data=request.data)
        print("request.data = ", request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        filePath = file.file.path
        folderPath = os.path.join(settings.DOCUMENT_FOLDER, str(file.project.id))
        # remove soft file
        if os.path.exists(filePath):
            os.remove(filePath)
        # remove empty folder     
        if os.path.exists(folderPath):   
            if len(os.listdir(folderPath)) == 0:
                os.rmdir(folderPath)
        #remove record in db
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
