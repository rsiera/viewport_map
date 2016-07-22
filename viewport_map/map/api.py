from __future__ import unicode_literals

import logging
import os

from django.conf import settings
from django.db import transaction
from rest_framework import response
from rest_framework import status
from rest_framework.views import APIView

from .exceptions import FTDataException
from .models import LocationPoint, service
from .serializers import LocationPointSerializer

CLIENT_SECRETS = os.path.join(settings.BASE_DIR, 'client_secrets.json')

logger = logging.getLogger(__name__)


class LocationPointList(APIView):
    def get_serializer_class(self):
        return LocationPointSerializer

    def get(self, request, format=None):
        points = LocationPoint.objects.all()
        serializer = self.get_serializer_class()(points, many=True)
        return response.Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except FTDataException as e:
                logger.error('Google Fusion Table Error %s', e)
                return response.Response(serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            with transaction.atomic():
                LocationPoint.objects.all().delete()
                service.bulk_delete()
        except Exception as e:
            return response.Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response({'success': True}, status=status.HTTP_200_OK)
