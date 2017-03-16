# coding=utf-8
from django.contrib import admin
from himawari.models import BroadcastStationModel, ChannelModel, ProgramModel, CategoryModel, SubCategoryModel

class BroadcastStationAdmin(admin.ModelAdmin):
    list_display = ("name", "station_id")
    list_filter = ("name", "station_id")

class ChannelAdmin(admin.ModelAdmin):
    list_display = ("physical_channel", )
    list_filter = ("physical_channel", )

class ProgramAdmin(admin.ModelAdmin):
    list_display = ("event_id", "title", "detail", "start_time", "end_time")
    list_filter = ("categories", "categories__category_id")
    search_fields = ("event_id", "title", "detail")

class CategoryAdmin(admin.ModelAdmin):
    # list_display = ("large_category", "middle_category")
    list_filter = ("category_id", )

class SubCategoryAdmin(admin.ModelAdmin):
    # list_display = ("large_category", "middle_category")
    list_filter = ("large_category__category_id", "category_id")

admin.site.register(BroadcastStationModel, BroadcastStationAdmin)
admin.site.register(ChannelModel, ChannelAdmin)
admin.site.register(ProgramModel, ProgramAdmin)
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(SubCategoryModel, SubCategoryAdmin)
