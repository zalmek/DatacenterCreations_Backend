from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dcapi.models import Components, Creationcomponents, Datacentercreations
from dcapi.serializers import ComponentSerializer, DatacenterCreationSerializer, CreationComponentsSerializer


# Create your views here.
@api_view(['Get'])
def get_components(request, format=None):
    """
    Возвращает список компонентов
    """
    print('get')
    components = Components.objects.all()
    serializer = ComponentSerializer(components, many=True)
    return Response(serializer.data)


@api_view(['Post'])
def post_component(request, format=None):
    """
    Добавляет новый компонент
    """
    print('post')
    serializer = ComponentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Get'])
def get_component(request, pk, format=None):
    component = get_object_or_404(Components, pk=pk)
    if request.method == 'GET':
        """
        Возвращает информацию о компоненте
        """
        serializer = ComponentSerializer(component)
        return Response(serializer.data)


@api_view(['Put'])
def put_component(request, pk, format=None):
    """
    Обновляет информацию об компоненте
    """
    component = get_object_or_404(Components, pk=pk)
    serializer = ComponentSerializer(component, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Delete'])
def delete_component(request, pk, format=None):
    """
    Удаляет информацию об компоненте
    """
    component = get_object_or_404(Components, pk=pk)
    component.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['Post'])
# def post_component(request, pk, format=None):
#     """
#     Добавляет компонент в заявку
#     """
#     print('post')
#     component = get_object_or_404(Components, pk=pk)
#     serializer = DatacenterCreationSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])
def delete_mm(request, pk, format=None):
    """
    Удаляет информацию о мм
    """
    mm = get_object_or_404(Creationcomponents, pk=pk)
    mm.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['Put'])
def put_mm(request, pk, format=None):
    """
    Обновляет информацию о мм
    """
    mm = get_object_or_404(Creationcomponents, pk=pk)
    serializer = CreationComponentsSerializer(mm, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Get'])
def get_creations(request, format=None):
    """
    Возвращает список заявок
    """
    print('get')
    creations = Datacentercreations.objects.all()
    serializer = ComponentSerializer(creations, many=True)
    return Response(serializer.data)


@api_view(['Get'])
def get_creation(request, format=None):
    """
    Возвращает заявку
    """
    print('get')
    creations = Datacentercreations.objects.all()
    serializer = ComponentSerializer(creations, many=True)
    return Response(serializer.data)