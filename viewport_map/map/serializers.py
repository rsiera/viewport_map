from __future__ import unicode_literals

from rest_framework import serializers

from .models import LocationPoint


class LocationPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationPoint
        fields = ('address', 'longitude', 'latitude',)
