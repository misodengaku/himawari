
from django.conf import settings

from rest_framework import routers, exceptions, mixins, viewsets, status, filters, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from himawari.models import BroadcastStationModel, ProgramModel, CategoryModel
from himawari.serializers import BroadcastStationSerializer, ProgramSerializer

router = routers.SimpleRouter()


class BroadcastStationViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):

    lookup_field = "station_id"
    serializer_class = BroadcastStationSerializer
    queryset = BroadcastStationModel.objects.all()

    def get_queryset(self):
        return self.queryset


class ProgramViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    lookup_field = "event_id"
    serializer_class = ProgramSerializer
    queryset = ProgramModel.objects.all()

    def get_queryset(self):
        return self.queryset

router.register('broadcaststations', BroadcastStationViewSet)
router.register('programs', ProgramViewSet)
