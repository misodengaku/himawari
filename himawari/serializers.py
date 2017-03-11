from rest_framework import serializers
from django.conf import settings

from himawari.models import BroadcastStationModel, ProgramModel, CategoryModel


class BroadcastStationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BroadcastStationModel
        fields = ("station_id", "name", "service_id",
                  "transport_stream_id", "original_network_id")

    station_id = serializers.CharField()
    name = serializers.CharField()
    service_id = serializers.IntegerField()
    transport_stream_id = serializers.IntegerField()
    original_network_id = serializers.IntegerField()


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramModel
        fields = ("event_id", "station", "title", "detail",
                  "start_time", "end_time", "category")

    event_id = serializers.IntegerField()
    station = serializers.PrimaryKeyRelatedField(queryset=BroadcastStationModel.objects.all(), source="station_id")
    title = serializers.CharField()
    detail = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    # category = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all(), require=False)
