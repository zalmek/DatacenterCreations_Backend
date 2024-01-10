from rest_framework import serializers

from dcapi.models import Components, DatacenterCreations, CreationСomponents, Users


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = "__all__"


class DatacenterCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DatacenterCreations
        fields = ["creationid", "creationdate", "creationformdate", "creationcompleteddate", "creationstatus",
                  "useremail", "moderatoremail"]


class CreationComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreationСomponents
        fields = ["creation", "component", "componentsnumber"]


class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = Users
        fields = ['email', 'password', 'is_staff']
