from rest_framework import serializers

from dcapi.models import Components, DatacenterCreations, CreationСomponents


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = "__all__"


class DatacenterCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatacenterCreations
        fields = "__all__"


class CreationComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreationСomponents
        fields = ["creation", "component", "componentsnumber"]
