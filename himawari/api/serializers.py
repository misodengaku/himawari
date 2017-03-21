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
        fields = '__all__'  # ('id', 'name')

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
    detail = serializers.CharField(allow_blank=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    categories = SubCategorySerializer(many=True, read_only=False)

    def create(self, validated_data):
        event_id = validated_data.get('event_id')
        station = validated_data.get('station')
        program = ProgramModel.objects.filter(event_id=event_id, station=station)
        categories_data = validated_data.pop('categories')
        category_filters = list(
            map(lambda c: models.Q(id=c['id']), categories_data))
        if len(category_filters) > 1:
            f = reduce(lambda a, b: a | b, category_filters)
            program.categories = SubCategoryModel.objects.filter(f)
        elif len(category_filters) == 1:
            print(category_filters)
            program.categories = SubCategoryModel.objects.filter(
                category_filters[0])


        program = ProgramModel.objects.create(**validated_data)
        # if len(program) == 0:
        #     print("create")
        # else:
        #     print("save")
        #     program['start_time'] = validated_data.get('start_time')
        #     program['end_time'] = validated_data.get('end_time')
        #     program.save()
        return program
