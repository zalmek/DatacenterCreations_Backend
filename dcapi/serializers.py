from rest_framework import serializers

from dcapi.models import Components, Datacentercreations


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = ["componentid", "componentname", "componentprice", "componentimage", "componentdescription",
                  "componentstatus"]


class DatacenterCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datacentercreations
        fields = ["creationid", "creationdate", "creationapproveddate", "creationrejectiondate", "creationcompleteddate", "creationdeletiondate", "userid", "creationstatus"]


class CreationComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datacentercreations
        fields = ["creationid", "componentid", "componentsnumber"]
