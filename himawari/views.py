
from django.conf import settings

from rest_framework import routers, exceptions, mixins, viewsets, status, filters, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from himawari.models import BroadcastStationModel, ProgramModel, SubCategoryModel
from himawari.serializers import BroadcastStationSerializer, ProgramSerializer, SubCategorySerializer

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


class SubCategoryViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):

    lookup_field = "id"
    serializer_class = SubCategorySerializer
    queryset = SubCategoryModel.objects.all()

    def get_queryset(self):
        name = self.request.query_params.get('name', None)

        if name is not None:
            sname = name.split(' - ')
            self.queryset = self.queryset.filter(
                large_category__name=sname[0], name=sname[1])

        return self.queryset

router.register('broadcaststations', BroadcastStationViewSet)
router.register('programs', ProgramViewSet)
router.register('categories', SubCategoryViewSet)
