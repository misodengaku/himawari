# coding=utf-8
from django.db import models
import uuid
import secrets

def generate_token():
    return str(uuid.uuid4)

def generate_secret():
    return secrets.token_urlsafe(48)

class AgentModel(models.Model):
    name = models.CharField("名前", max_length=256)
    ground_tunner = models.IntegerField("地上デジタルチューナー数")
    bs_tunner = models.IntegerField("BS/CSチューナー数")
    token = models.CharField("トークン", max_length=200)

    