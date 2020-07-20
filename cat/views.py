from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
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
    GlossaryWithChildSerializer,
    FileWithChildSerializer,
    ImportTMSerializer,
    ImportGlossarySerializer,
    MachineTranslateSerializer,
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
import Levenshtein as lev
import sys
import openpyxl
from rest_framework.parsers import MultiPartParser
from django.db import IntegrityError

from django.core.files import File as _File
from django.http import HttpResponse, Http404
sys.path.append(os.path.join(settings.BASE_DIR,'preprocessing_python'))
from preprocessor import *
import requests
import ast

class TranslationMemoryViewSet(viewsets.ModelViewSet):
    queryset = TranslationMemory.objects.all().order_by('id')
    serializer_class = TranslationMemorySerializer
    
    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.request.user.id)
        return queryset


class TMContentViewSet(viewsets.ModelViewSet):
    queryset = TMContent.objects.all().order_by('id')
    serializer_class = TMContentSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(translation_memory__user__id = self.request.user.id)
        tm_id = self.request.query_params.get('tm_id', None)
        if tm_id is not None:
            queryset = queryset.filter(translation_memory=tm_id)
        return queryset


class GlossaryTypeViewSet(viewsets.ModelViewSet):
    queryset = GlossaryType.objects.all().order_by('id')
    serializer_class = GlossaryTypeSerializer
    
    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.request.user.id)
        return queryset


class GlossaryViewSet(viewsets.ModelViewSet):
    queryset = Glossary.objects.all().order_by('id')
    serializer_class = GlossarySerializer
    
    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.request.user.id)
        return queryset

class GlossaryWithChildViewSet(viewsets.ModelViewSet):
    queryset = Glossary.objects.all().order_by('id')
    serializer_class = GlossaryWithChildSerializer
    
    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.request.user.id)
        return queryset


class GlossaryContentViewSet(viewsets.ModelViewSet):
    queryset = GlossaryContent.objects.all().order_by('id')
    serializer_class = GlossaryContentSerializer


class ProjectViewSet(viewsets.ModelViewSet):    
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('id')
    
    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.request.user.id)
        return queryset


class SentenceViewSet(viewsets.ModelViewSet):
    queryset = Sentence.objects.all().order_by('id')
    serializer_class = SentenceSerializer
    
    def get_queryset(self):
        queryset = self.queryset.filter(file__project__user__id = self.request.user.id)
        file_id = self.request.query_params.get('file_id', None)
        if file_id is not None:
            queryset = queryset.filter(file_id=file_id)
        return queryset

#TODO: fix bug post data to another user
#TODO: fix bug security in upload file (upload to project not belongs to me)
class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = FileSerializer(data=request.data)
            # import pdb; pdb.set_trace() 
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
                if project.src_lang == "Vietnamese":
                    p = Preprocessor(Language.vietnamese)    
                elif project.src_lang == "English":
                    p = Preprocessor(Language.english)    

                sents = p.segment_to_sentences(text)
                sents_cnt = len(sents)
                
                for idx in range(0, sents_cnt):                
                    sentence_serilizer = SentenceSerializer(data = {"src_str":sents[idx],"file":uf.id})
                    if sentence_serilizer.is_valid():
                        sentence_serilizer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        try:
            p_id=(self.request.query_params.get('project_id'))
            files = File.objects.filter(project_id=p_id, project__user__id = self.request.user.id)
            serializer = FileSerializer(files, many=True)
            return Response (serializer.data)
        except ValueError:
            return Response("Please check your input", status=status.HTTP_400_BAD_REQUEST)

class FileUploadDetailView(APIView):
    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk, project__user__id = self.request.user.id)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileWithChildSerializer(file)
        return Response(serializer.data)       

    def put(self, request, pk, format=None):
        try:
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
        except ValueError:
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


# TODO: https://docs.python.org/3.6/library/concurrent.futures.html
@api_view(['POST'])
def machine_translate(request):
    try:
        serializer = MachineTranslateSerializer(data=request.data)    
        
        if serializer.is_valid():
            src_lang=serializer.initial_data["src_lang"]
            tar_lang=serializer.initial_data["tar_lang"]
            sentence=serializer.initial_data["sentence"]
            url = "https://api.mymemory.translated.net/get?langpair=%s|%s&key=9d62199240694d4c2176&q=%s" % (src_lang, tar_lang, sentence)
            response = requests.get(url)

            byte_str = response.content
            dict_str = byte_str.decode("UTF-8")
            
            data = json.loads(dict_str)
            dict=[]
            # arr = data["matches"]

            # for i in range(len(arr)):
            #     if float(arr[i]["match"]) >= 0.8:
            #         child={}
            #         child.update({"translation": arr[i]["translation"]})
            #         child.update({"match": arr[i]["match"]})
            #         child.update({"source": "mymemory"})
            #         dict.append(child)

            child={}
            child.update({"translation": data["responseData"]["translatedText"]})
            child.update({"source": "mymemory"})
            dict.append(child)

            j = {"is_success":True, "err_msg": None} 
            j.update({"result":dict})
            return HttpResponse(json.dumps(j, ensure_ascii=False),
                content_type="application/json",status=status.HTTP_200_OK)
        j = {"is_success":False, "err_msg":  serializer.errors}
        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        j = {"is_success":False, "err_msg":  "Failed to Get data: "+str(e)}
        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_200_OK)


@api_view(['GET'])
def file_download(request):
    try:
        f = File.objects.get(id=request.data["file_id"], project__user__id = request.user.id)
        # import pdb; pdb.set_trace() 
        path = f.file.path
        
        with open(path, 'r') as file :
            filedata = file.read()

        for s in f.sentence_set.all():
            filedata = filedata.replace(s.src_str, s.tar_str, 1)

        new_path = os.path.splitext(path)[0]+" (export)" + os.path.splitext(path)[1]
        
        # with open(new_path, 'w') as file:
        #     file.write(filedata)
        # print(os.path.basename(new_path))

        response = HttpResponse(filedata, content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename={0}'.format(os.path.basename(new_path))
        return response
    except File.DoesNotExist:
        raise Http404
    except Exception as e:
        j = {"is_success":False, "err_msg":  "Failed to Get data: "+str(e)}
        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_tm_by_src_sentence(request):
    try:
        sentence=request.data["sentence"]
        min_similarity=request.data["min_similarity"]

        client = Elasticsearch()     
        if "translation_memory_id" in request.data: 
            translation_memory_id = request.data["translation_memory_id"]
            q = Q('bool', must=[Q('match', src_sentence=sentence), Q('match', translation_memory__id=translation_memory_id)])
        else:
            q = Q("match", src_sentence=sentence) 

        s = Search(using=client, index=settings.INDEX_TM).query(q)[0:20] 
        res = s.execute()

        dict=[]
        for i in range(len(res)):
            simi = lev.ratio(sentence, res[i].src_sentence)
            if simi>= min_similarity:
                child={}
                child.update({"src_sentence": res[i].src_sentence})
                child.update({"tar_sentence": res[i].tar_sentence})
                child.update({"similarity": round(simi, 2)})
                dict.append(child)
        
        dict = sorted(dict, key = lambda i: i['similarity'], reverse=True) 

        j = {"is_success":True, "err_msg": None} 
        j.update({"result":dict})

        return HttpResponse(json.dumps(j, ensure_ascii=False),
            content_type="application/json",status=status.HTTP_200_OK)

    except Exception as e:
        j = {"is_success":False, "err_msg":  "Failed to Get data: "+str(e)}
        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_200_OK)


@api_view(['GET'])
def get_glossary_by_src_sentence(request):
    try:
        phrase=request.data["sentence"]
        min_similarity=request.data["min_similarity"]

        client = Elasticsearch()     
        if "glossary_id" in request.data: 
            glossary_id = request.data["glossary_id"]
            q = Q('bool', must=[Q('match', src_phrase=phrase), Q('match', glossary__id=glossary_id)])
        else:
            q = Q("match", src_phrase=phrase) 

        s = Search(using=client, index=settings.INDEX_GLOSSARY).query(q)[0:100] 
        res = s.execute()

        dict=[]
        for i in range(len(res)):
            simi = lev.ratio(phrase, res[i].src_phrase)
            if simi>= min_similarity:
                if res[i].src_phrase in phrase:
                    child={}
                    child.update({"src_phrase": res[i].src_phrase})
                    child.update({"tar_phrase": res[i].tar_phrase})
                    child.update({"similarity": round(simi, 2)})
                    dict.append(child)
        
        dict = sorted(dict, key = lambda i: i['similarity'], reverse=True) 

        j = {"is_success":True, "err_msg": None} 
        j.update({"result":dict})

        return HttpResponse(json.dumps(j, ensure_ascii=False),
            content_type="application/json",status=status.HTTP_200_OK)

    except Exception as e:
        j = {"is_success":False, "err_msg":  "Failed to Get data: "+str(e)}
        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_200_OK)


# TODO: Add more security
@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    try:
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]

        if User.objects.filter(email=email).exists():
            j = {"is_success":False, "err_msg": email+" already exists"}
            return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username, email, password)

        j = {"id":user.id, "username":username, "email":email}

        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_200_OK)

    except IntegrityError as e:
        j = {"is_success":False, "err_msg": username+" already exists"}
        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        j = {"is_success":False, "err_msg": ""+str(e)}
        return HttpResponse(json.dumps(j, ensure_ascii=False), content_type="application/json",status=status.HTTP_400_BAD_REQUEST)



class ImportGlossaryView(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request, *args, **kwargs):
        try:
            serializer = ImportGlossarySerializer(data=request.data)    
            glossary_id=request.data["glossary_id"]
            if serializer.is_valid():
                glossary=Glossary.objects.get(pk=glossary_id, user = self.request.user.id)
                # import pdb; pdb.set_trace() 

                file_obj = request.FILES['glossary_file']

                wb = openpyxl.load_workbook(file_obj)
                ws = wb[wb.sheetnames[0]]

                for row in ws.iter_rows(min_row=2):
                    GlossaryContent.objects.create(
                        src_phrase=row[0].value,
                        tar_phrase=row[1].value,
                        glossary_id=glossary_id
                    )

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Glossary.DoesNotExist:
            return Response({"detail":"glossary_id not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImportTMView(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request, *args, **kwargs):
        try:
            serializer = ImportTMSerializer(data=request.data)    
            tm_id=request.data["tm_id"]
            if serializer.is_valid():
                tm=TranslationMemory.objects.get(pk=tm_id, user = self.request.user.id)
                # import pdb; pdb.set_trace() 

                file_obj = request.FILES['tm_file']

                wb = openpyxl.load_workbook(file_obj)
                ws = wb[wb.sheetnames[0]]

                for row in ws.iter_rows(min_row=2):
                    TMContent.objects.create(
                        src_sentence=row[0].value,
                        tar_sentence=row[1].value,
                        translation_memory_id=tm_id
                    )
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TranslationMemory.DoesNotExist:
            return Response({"detail":"tm_id not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)