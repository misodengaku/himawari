# coding=utf-8
from django.db import models


class AgentModel(models.Model):
    name = models.CharField("名前", max_length=256)
    ground_tunner = models.IntegerField("地上デジタルチューナー数")
    bs_tunner = models.IntegerField("BS/CSチューナー数")

    