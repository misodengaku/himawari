
from django.conf import settings
from django.db.models import Q

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
        large_category = self.request.query_params.get('large_category', None)
        middle_category = self.request.query_params.get(
            'middle_category', None)

        l_query = Q()
        m_query = Q()

        if large_category is not None:
            l_query = Q(large_category__name=large_category)

        if middle_category is not None:
            m_query = Q(name=middle_category)

        self.queryset = self.queryset.filter(l_query, m_query)

        return self.queryset


router.register('broadcaststations', BroadcastStationViewSet)
router.register('programs', ProgramViewSet)
router.register('categories', SubCategoryViewSet)
