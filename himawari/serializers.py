from rest_framework import serializers
from django import core
from django.conf import settings
from django.db import models
from django.forms.models import model_to_dict
from functools import reduce

from himawari.models import BroadcastStationModel, ProgramModel, CategoryModel, SubCategoryModel


class BroadcastStationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BroadcastStationModel
        # fields = ('station_id',)
        fields = '__all__'

    station_id = serializers.CharField()
    name = serializers.CharField(required=False)
    service_id = serializers.IntegerField(required=False)
    transport_stream_id = serializers.IntegerField(required=False)
    original_network_id = serializers.IntegerField(required=False)


class SubCategorySerializer(serializers.Serializer):

    class Meta:
        model = SubCategoryModel
        fields = '__all__' #('id', 'name')

    id = serializers.IntegerField()
    # name = serializers.SerializerMethodField()
    large_category = serializers.SerializerMethodField()
    middle_category = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id

    # def get_name(self, obj):
    #     return obj.get_fullname()

    def get_large_category(self, obj):
        return obj.large_category.get_name()

    def get_middle_category(self, obj):
        return obj.get_name()

    def create(self, validated_data):
        id_pk = validated_data.pop('id')
        category = SubCategoryModel.objects.get(id=id_pk)
        return category


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramModel
        # fields = '__all__'
        fields = ("event_id", "station", "title", "detail",
                  "start_time", "end_time", "categories")

    event_id = serializers.IntegerField()
    station = serializers.PrimaryKeyRelatedField(
        queryset=BroadcastStationModel.objects.all())
    title = serializers.CharField()
    detail = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    categories = SubCategorySerializer(many=True, read_only=False)

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        program = ProgramModel.objects.create(**validated_data)

        f = reduce(lambda a, b: a | b, map(lambda c: models.Q(id=c['id']), categories_data))
        program.categories = SubCategoryModel.objects.filter(f)
        return program
