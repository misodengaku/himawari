# coding=utf-8
from django.db import models


class BroadcastStationModel(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "放送局"

    station_id = models.CharField("局ID", max_length=16, primary_key=True)
    name = models.CharField("局名", max_length=64)
    service_id = models.IntegerField("サービスID")
    transport_stream_id = models.IntegerField("トランスポートストリームID")
    original_network_id = models.IntegerField("オリジナルネットワークID")

    def __str__(self):
        return self.name


class ProgramModel(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "番組"

    event_id = models.IntegerField("イベントID")
    station = models.ForeignKey('BroadcastStationModel')
    title = models.TextField("番組名")
    detail = models.TextField("番組内容")
    start_time = models.DateTimeField("開始時刻")
    end_time = models.DateTimeField("終了時刻")
    category = models.ForeignKey('CategoryModel', blank=True, null=True)

    def __str__(self):
        return "%d - %s" % (self.event_id, self.title)


class CategoryModel(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "番組カテゴリ"

    large_category = models.CharField("カテゴリ", max_length=64)
    middle_category = models.CharField("サブカテゴリ", max_length=64)

    def __str__(self):
        return "%s - %s" % (self.large_category, self.middle_category)
