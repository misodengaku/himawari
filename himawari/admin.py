# coding=utf-8
from django.contrib import admin
from himawari.models import BroadcastStationModel, ProgramModel, CategoryModel

class BroadcastStationAdmin(admin.ModelAdmin):
    list_display = ("name", "station_id")
    list_filter = ("name", "station_id")

class ProgramAdmin(admin.ModelAdmin):
    list_display = ("event_id", "title", "detail", "start_time", "end_time")
    list_filter = ("category__large_category", "category__middle_category")
    search_fields = ("event_id", "title", "detail")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("large_category", "middle_category")
    list_filter = ("large_category", "middle_category")

admin.site.register(BroadcastStationModel, BroadcastStationAdmin)
admin.site.register(ProgramModel, ProgramAdmin)
admin.site.register(CategoryModel, CategoryAdmin)
