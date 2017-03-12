from rest_framework import serializers
from django import core
from django.conf import settings
from django.db import models
from django.forms.models import model_to_dict

from himawari.models import BroadcastStationModel, ProgramModel, CategoryModel, SubCategoryModel


class BroadcastStationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BroadcastStationModel
        # fields = ('station_id',)
        fields = '__all__'

    station_id = serializers.CharField()
    name = serializers.CharField()
    service_id = serializers.IntegerField()
    transport_stream_id = serializers.IntegerField()
    original_network_id = serializers.IntegerField()


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategoryModel
        fields = ('id', 'name')

    name = serializers.SerializerMethodField()
    # name = serializers.CharField()

    def get_name(self, obj):
        return obj.get_fullname()


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramModel
        fields = '__all__'
        # ("event_id", "station", "title", "detail",
        #           "start_time", "end_time", "categories")

    event_id = serializers.IntegerField()
    # station = BroadcastStationSerializer(read_only=True)
    station = serializers.PrimaryKeyRelatedField(
        queryset=BroadcastStationModel.objects.all())
    title = serializers.CharField()
    detail = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    categories = SubCategorySerializer(many=True, read_only=False)

    def create(self, validated_data):
        print(validated_data)
        categories_data = validated_data.pop('categories')
        program = ProgramModel.objects.create(**validated_data)
        for category_data in categories_data:
            print(category_data)
            program.categories.create(**category_data)
        return program
