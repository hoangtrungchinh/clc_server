from django.shortcuts import render

from rest_framework import viewsets
from .serializers import ClcSerializer
from .models import clc

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from django.http import JsonResponse, HttpResponse

from elasticsearch import Elasticsearch 
from elasticsearch_dsl import Search, Q
import json

class ClcViewSet(viewsets.ModelViewSet):
    queryset = clc.objects.all().order_by('tar')
    serializer_class = ClcSerializer


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
def clc_get_by_src(request):
    try:
        _src=request.data["src"]

        client = Elasticsearch()      
        q = Q("match", src=_src) 
        s = Search(using=client, index="clc").query(q)[0:20] 
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
