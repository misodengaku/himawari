from django.contrib import admin
from himawari.agent.models import AgentModel

class AgentAdmin(admin.ModelAdmin):
    list_display = ("name", "ground_tunner", "bs_tunner")
    list_filter = ("name", "ground_tunner", "bs_tunner")


admin.site.register(AgentModel, AgentAdmin)
