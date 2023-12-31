import base64
import datetime
import uuid
from itertools import chain

from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

import minioClient
from minioClient import minio_bucket
from minioClient import minio_url
from dcapi.models import Components, CreationСomponents, DatacenterCreations, Users
from dcapi.serializers import ComponentSerializer, DatacenterCreationSerializer, CreationComponentsSerializer

# Create your views here

user = Users.objects.get(userrole="Customer")


class ComponentsApiView(APIView):
    model = Components
    serializer = ComponentSerializer

    def get(self, request, pk=None, format=None):
        """
        Возвращает список компонентов
        """
        if pk is None:
            filterText = ""
            if request.GET.get("filterText") is not None:
                filterText = request.GET.get("filterText")
            components = self.model.objects.all().filter(componentstatus=1).order_by("componentid").filter(
                componentname__contains=filterText)
            for component in components:
                component.componentimage = 'http://' + minio_url + '/' + minio_bucket + '/' + component.componentimage
            serializer = self.serializer(components, many=True)
            try:
                creation = DatacenterCreations.objects.get(user=Users.objects.get(email=user.email))
                return Response({
                    "components": serializer.data,
                    "creation": creation.creationid
                })
            except:
                creation = None
                return Response({
                    "components": serializer.data,
                    "creation": None
                })
        else:
            component = get_object_or_404(self.model, pk=pk)
            component.componentimage = 'http://' + minio_url + '/' + minio_bucket + '/' + component.componentimage
            serializer = self.serializer(component)
            return Response(serializer.data)

    def post(self, request, format=None):
        """
        Добавляет новый компонент
        """
        print('post')
        try:
            image = bytes(request.data['componentimage'], "utf-8")
            print(image)
            filename = uuid.uuid4()
            file = open("dcapi/static/"+filename.__str__() + ".png", "wb")
            file.write(base64.b64decode(image))
            file.close()
            minioClient.load_file(filename.__str__() + ".png")
            request.data["componentimage"] = filename.__str__()+".png"
        finally:
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
        try:
            image = request.data['image'].decode("utf-8")
            filename = uuid.uuid4()
            file = open(filename.__str__()+".png", "wb")
            file.write(base64.b64decode(image))
            file.close()
            minioClient.load_file(filename.__str__()+".png")
            component.componentimage = filename.__str__()+".png"
        finally:
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


# Ааааааааааааааааааааааааааааааааааа
@api_view(['Post'])
def post_component_to_creation(request, pk, format=None):
    """
    Добавляет компонент в заявку
    """
    print('post')
    component = get_object_or_404(Components, pk=pk)
    creation = DatacenterCreations.objects.get_or_create(user=user)
    creation[0].save()
    creation_components = CreationСomponents.objects.get_or_create(component=component,
                                                                   creation=creation[0])
    creation_components[0].componentsnumber += 1
    creation_components[0].save()
    components = Components.objects.all().filter(componentstatus=1).order_by("componentid")
    serializer = ComponentSerializer(components, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CreationcomponentsApiVIew(APIView):
    model = CreationСomponents
    serializer = CreationComponentsSerializer

    def delete(self, request, pk_creation=None, pk_component=None, format=None):
        """
        Удаляет информацию о мм
        """
        mm = get_object_or_404(self.model, component=Components.objects.get(pk_component),
                               creation=CreationСomponents.objects.get(pk_creation))
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
        status_filter = request.GET.get("status")
        start_date_filter = request.GET.get("start_date")
        end_date_filter = request.GET.get("end_date")
        if pk is None:
            """
            Возвращает список заявок
            """
            print('get')
            creations = self.model.objects.all()
            if status_filter is not None:
                creations = creations.filter(creationstatus=status_filter)
            if start_date_filter is not None and end_date_filter is not None:
                start_date = datetime.datetime.strptime(start_date_filter, "%Y-%m-%d")
                end_date = datetime.datetime.strptime(end_date_filter, "%Y-%m-%d")
                creations = creations.filter(creationdate__range=(start_date, end_date))
            serializer = self.serializer(creations, many=True)
            return Response(serializer.data)
        else:
            """
            Возвращает заявку
            """
            print('get')
            creation = self.model.objects.get(pk=pk)
            creation_components = CreationСomponents.objects.all().filter(creation=creation)
            list = []
            number_of_components = []
            for one in creation_components:
                list.append(Components.objects.get(componentid=one.component.componentid))
                number_of_components.append(one.componentsnumber)
            components = chain(list)
            return Response({
                "creation": DatacenterCreationSerializer(creation).data,
                "components": ComponentSerializer(components, many=True).data,
                "number_of_components": number_of_components,
            })

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

    def delete(self, request, pk, format=None):
        creation = get_object_or_404(self.model, pk=pk)
        creation_components = CreationСomponents.objects.all().filter(creation=creation)
        for one in creation_components:
            one.delete()
        creation.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def publish_creation(request, pk, format=None):
    creation = get_object_or_404(DatacenterCreations, pk=pk)
    if creation.creationstatus == 0:
        creation.creationstatus = 1
        creation.creationformdate = datetime.datetime.now()
        creation.save()
    creation_components = CreationСomponents.objects.all().filter(creation=creation)
    list = []
    number_of_components = []
    for one in creation_components:
        list.append(Components.objects.get(componentid=one.component.componentid))
        number_of_components.append(one.componentsnumber)
    components = chain(list)
    return Response({
        "creation": DatacenterCreationSerializer(creation).data,
        "components": ComponentSerializer(components, many=True).data,
        "number_of_components": number_of_components,
    })


@api_view(['POST'])
def approve_creation(request, pk, format=None):
    creation = get_object_or_404(DatacenterCreations, pk=pk)
    if creation.creationstatus == 1:
        creation.creationstatus = 2
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    return return_creations(creation, request)


@api_view(['POST'])
def reject_creation(request, pk, format=None):
    creation = get_object_or_404(DatacenterCreations, pk=pk)
    if creation.creationstatus == 1:
        creation.creationstatus = 3
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    return return_creations(creation, request)


@api_view(['POST'])
def complete_creation(request, pk, format=None):
    creation = get_object_or_404(DatacenterCreations, pk=pk)
    if creation.creationstatus == 2:
        creation.creationstatus = 4
        creation.creationcompleteddate = datetime.datetime.now()
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    return return_creations(creation, request)


@api_view(['POST'])
def delete_creation(request, pk, format=None):
    """
        Удаляет заявку (статус "удалён")
        """
    creation = get_object_or_404(DatacenterCreations, pk=pk)
    if creation.creationstatus == 0:
        creation.creationstatus = 5
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    return return_creations(creation, request)


def return_creations(creation, request):
    creation.save()
    creations = DatacenterCreations.objects.all().exclude(
        creationstatus=0) & DatacenterCreations.objects.all().exclude(
        creationstatus=5)
    return Response(DatacenterCreationSerializer(creations, many=True).data, status=status.HTTP_202_ACCEPTED)
