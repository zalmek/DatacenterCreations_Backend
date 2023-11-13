import datetime

from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from minioClient import minio_bucket
from minioClient import minio_url
from dcapi.models import Components, CreationСomponents, DatacenterCreations
from dcapi.serializers import ComponentSerializer, DatacenterCreationSerializer, CreationComponentsSerializer


# Create your views here.

class ComponentsApiView(APIView):
    model = Components
    serializer = ComponentSerializer

    def get(self, request, pk=None, format=None):
        """
        Возвращает список компонентов
        """
        if pk is None:
            print('get')
            components = self.model.objects.all().filter(componentstatus=1).order_by("componentid")
            for component in components:
                component.componentimage = 'http://'+minio_url+'/'+minio_bucket+'/'+component.componentimage
            serializer = self.serializer(components, many=True)
            return Response(serializer.data)
        else:
            print('get')
            component = get_object_or_404(self.model, pk=pk)
            serializer = self.serializer(component)
            return Response(serializer.data)

    def post(self, request, format=None):
        """
        Добавляет новый компонент
        """
        print('post')
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        """
        Обновляет информацию об компоненте
        """
        component = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(component, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Удаляет информацию об компоненте
        """
        component = get_object_or_404(self.model, pk=pk)
        component.componentstatus = 0
        component.save()
        return Response(data=self.serializer(self.model.objects.all().filter(componentstatus=1).order_by("componentid"),
                                             many=True).data, status=status.HTTP_204_NO_CONTENT)


# # Ааааааааааааааааааааааааааааааааааа
# @api_view(['Post'])
# def post_component_to_creation(request, pk, format=None):
#     """
#     Добавляет компонент в заявку
#     """
#     print('post')
#     component = get_object_or_404(Components, pk=pk)
#     creation = DatacenterCreations.objects.get_or_create(userid_id=1)
#     creation[0].save()
#     try:
#         creation_components = CreationСomponents.objects.get(
#             componentid=component.componentid, creationid=creation[0].creationid,
#         )
#     except:
#         creation_components = CreationСomponents.objects.create(
#             componentid=component.componentid,
#             creationid=creation[0].creationid,
#             componentsnumber=0
#         )
#     creation_components[0].componentsnumber += 1
#     serializer = DatacenterCreationSerializer(creation_components)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreationcomponentsApiVIew(APIView):
    model = CreationСomponents
    serializer = CreationComponentsSerializer

    def delete(self, request, pk_creation=None, pk_component=None, format=None):
        """
        Удаляет информацию о мм
        """
        mm = get_object_or_404(self.model, componentid=pk_component, creationid=pk_creation)
        mm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        """
        Обновляет информацию о мм
        """
        mm = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(mm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatacenterCreationsApiVIew(APIView):
    model = DatacenterCreations
    serializer = DatacenterCreationSerializer

    def get(self, request, pk=None, format=None):
        if pk is None:
            """
            Возвращает список заявок
            """
            print('get')
            creations = self.model.objects.all()
            serializer = self.serializer(creations, many=True)
            return Response(serializer.data)
        else:
            """
            Возвращает заявку
            """
            print('get')
            creations = self.model.objects.all()
            serializer = self.serializer(creations, many=True)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Обновляет информацию о заявке
        """
        creations = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(creations, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def publish_creation(request, pk, format=None):
    creations = get_object_or_404(DatacenterCreations, pk=pk)
    creations.creationstatus = 1
    creations.creationdate = datetime.datetime.now().date()
    serializer = CreationComponentsSerializer(creations, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def approve_creation(request, pk, format=None):
    creations = get_object_or_404(DatacenterCreations, pk=pk)
    creations.creationstatus = 2
    creations.creationapproveddate = datetime.datetime.now().date()
    serializer = CreationComponentsSerializer(creations, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reject_creation(request, pk, format=None):
    creations = get_object_or_404(DatacenterCreations, pk=pk)
    creations.creationstatus = 3
    creations.creationrejectiondate = datetime.datetime.now().date()
    serializer = CreationComponentsSerializer(creations, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def complete_creation(request, pk, format=None):
    creations = get_object_or_404(DatacenterCreations, pk=pk)
    creations.creationstatus = 4
    creations.creationcompleteddate = datetime.datetime.now().date()
    serializer = CreationComponentsSerializer(creations, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_creation(request, pk, format=None):
    """
    Удаляет заявку (статус "удалён")
    """
    creations = get_object_or_404(DatacenterCreations, pk=pk)
    creations.creationstatus = 5
    creations.creationdeletiondate = datetime.datetime.now().date()
    serializer = DatacenterCreationSerializer(creations, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
