import datetime
import uuid
from itertools import chain

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from dcapi.models import Components, CreationСomponents, DatacenterCreations, Users
from dcapi.permissions import IsAdmin, IsManager, IsAuth, session_storage
from dcapi.serializers import ComponentSerializer, DatacenterCreationSerializer, CreationComponentsSerializer, \
    UserSerializer
from minioClient import minio_bucket
from minioClient import minio_url
from django.conf import settings
import redis


# Create your views here

# Connect to our Redis instance

def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)

        return decorated_func

    return decorator


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
                ssid = request.COOKIES["session_id"]
                value = session_storage.get(ssid)
                creations = DatacenterCreations.objects.get(userid=Users.objects.get(email__iexact=value.decode("utf-8")).id)
            except:
                creations = None
            return Response({
                "components": serializer.data,
                "creation": DatacenterCreationSerializer(creations).data
            })
        else:
            component = get_object_or_404(self.model, pk=pk)
            component.componentimage = 'http://' + minio_url + '/' + minio_bucket + '/' + component.componentimage
            serializer = self.serializer(component)
            return Response(serializer.data)

    @swagger_auto_schema(request_body=ComponentSerializer)
    @method_permission_classes((IsAdmin,))
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

    @swagger_auto_schema(request_body=ComponentSerializer)
    @method_permission_classes((IsAdmin,))
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

    @method_permission_classes((IsAdmin,))
    def delete(self, request, pk, format=None):
        """
        Удаляет информацию об компоненте
        """
        component = get_object_or_404(self.model, pk=pk)
        component.componentstatus = 0
        component.save()
        return Response(data=self.serializer(self.model.objects.all().filter(componentstatus=1).order_by("componentid"),
                                             many=True).data, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(request_body=ComponentSerializer, method="post")
@api_view(['Post'])
@permission_classes([IsAuth])
def post_component_to_creation(request, pk, format=None):
    """
    Добавляет компонент в заявку
    """
    print('post')
    user_email = session_storage.get(request.COOKIES["session_id"]).decode("utf-8")
    user = Users.objects.get(email__iexact=user_email)
    component = get_object_or_404(Components, pk=pk)
    creation = DatacenterCreations.objects.get_or_create(user_id=user.id)
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

    @method_permission_classes((IsManager,))
    def delete(self, request, pk_creation=None, pk_component=None, format=None):
        """
        Удаляет информацию о мм
        """
        mm = get_object_or_404(self.model, component=Components.objects.get(pk_component),
                               creation=CreationСomponents.objects.get(pk_creation))
        mm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=CreationComponentsSerializer)
    @method_permission_classes((IsManager,))
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

    @method_permission_classes([IsAuth])
    def get(self, request, pk=None, format=None):
        user = Users.objects.get(email__exact=session_storage.get(request.COOKIES["session_id"]).decode("utf-8"))
        if pk is None and user.is_superuser:
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
            if pk is not None:
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
            else:
                creation = self.model.objects.get(user=user)
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

    @swagger_auto_schema(request_body=DatacenterCreationSerializer)
    @method_permission_classes([IsAdmin])
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

    @method_permission_classes([IsAdmin])
    def delete(self, request, pk, format=None):
        creation = get_object_or_404(self.model, pk=pk)
        creation_components = CreationСomponents.objects.all().filter(creation=creation)
        for one in creation_components:
            one.delete()
        creation.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuth])
def publish_creation(request, pk, format=None):
    creation = get_object_or_404(DatacenterCreations, pk=pk)
    creation.creationstatus = 1
    creation.creationdate = datetime.datetime.now().date()
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
@permission_classes([IsManager])
def approve_creation(request, pk, format=None):
    creation = get_object_or_404(DatacenterCreations, pk=pk)
    creation.creationstatus = 2
    creation.creationapproveddate = datetime.datetime.now().date()
    return return_creations(creation, request)


@api_view(['POST'])
@permission_classes([IsManager])
def reject_creation(request, pk, format=None):
    creation = get_object_or_404(DatacenterCreations, pk=pk)
    creation.creationstatus = 3
    creation.creationrejectiondate = datetime.datetime.now().date()
    return return_creations(creation, request)


@api_view(['POST'])
@permission_classes([IsManager])
def complete_creation(request, pk, format=None):
    creation = get_object_or_404(DatacenterCreations, pk=pk)
    creation.creationstatus = 4
    creation.creationcompleteddate = datetime.datetime.now().date()
    return return_creations(creation, request)


@api_view(['POST'])
@permission_classes([IsManager])
def delete_creation(request, pk, format=None):
    """
        Удаляет заявку (статус "удалён")
        """
    creation = get_object_or_404(DatacenterCreations, pk=pk)
    if creation.creationstatus != 1 and creation.creationid!=0:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    creation.creationstatus = 5
    creation.creationdeletiondate = datetime.datetime.now().date()
    return return_creations(creation, request)


def return_creations(creation, request):
    creation.save()
    creations = DatacenterCreations.objects.all().exclude(
        creationstatus=0) & DatacenterCreations.objects.all().exclude(
        creationstatus=5)
    return Response(DatacenterCreationSerializer(creations, many=True).data, status=status.HTTP_202_ACCEPTED)


class UserViewSet(viewsets.ModelViewSet):
    """Класс, описывающий методы работы с пользователями
    Осуществляет связь с таблицей пользователей в базе данных
    """
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    model_class = Users

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['list']:
            permission_classes = [IsAdmin | IsManager]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request, **kwargs):
        """
        Функция регистрации новых пользователей
        Если пользователя c указанным в request email ещё нет, в БД будет добавлен новый пользователь.
        """
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            self.model_class.objects.create_user(email=serializer.data['email'],
                                                 password=serializer.data['password'],
                                                 is_superuser=serializer.data['is_superuser'],
                                                 is_staff=serializer.data['is_staff'])
            return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Post'])
def login_view(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        user = authenticate(**serializer.data)
        if user is not None:
            random_key = uuid.uuid4()
            session_storage.set(random_key.__str__(), user.email)
            response = HttpResponse("{'status': 'ok'}")
            response.set_cookie("session_id", random_key)
            return response
        else:
            return HttpResponse("{'status': 'error', 'error': 'login failed'}")
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['Post'])
def logout_view(request):
    sessionid = request.COOKIES["session_id"]
    response = HttpResponse("{'status': 'ok'}")
    session_storage.set(sessionid, "expired")
    return response
