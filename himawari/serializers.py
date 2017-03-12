from rest_framework import serializers
from django import core
from django.conf import settings
from django.db import models
from django.forms.models import model_to_dict

from himawari.models import BroadcastStationModel, ProgramModel, CategoryModel, SubCategoryModel


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

class CategoryField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, obj):
        return CategoryModel.objects.filter(large_category=1, middle_category=1)
        # return model_to_dict(obj)
        # print(obj)
        # if str(obj) == 'himawari.CategoryModel.None':
        #     return [None,]
        # print(core.serializers.serialize('json', obj))
        # return core.serializers.serialize('json', obj)

    def to_internal_value(self, data):
        if data == 'ニュース／報道 - 天気':
            print(CategoryModel.objects.filter(large_category=1, middle_category=1))
            return CategoryModel.objects.filter(large_category=1, middle_category=1)
        raise serializer.ValidationError('unknown category')


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramModel
        fields = ("event_id", "station", "title", "detail",
                  "start_time", "end_time", "category")

    event_id = serializers.IntegerField()
    station = serializers.PrimaryKeyRelatedField(
        queryset=BroadcastStationModel.objects.all(), source="station_id")
    title = serializers.CharField()
    detail = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    category = serializers.ListField(
        CategoryField(
           queryset=SubCategoryModel.objects.all(), source="category__id"
        )
    )
    # category = CategoryField()


