from __future__ import unicode_literals

from django.db import models

from .exceptions import FTDataException
from .services import FusionTableClient


class LocationPoint(models.Model):
    address = models.TextField()
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        unique_together = ('address', 'longitude', 'latitude',)

    def save(self, **kwargs):
        try:
            service.insert(self)
        except Exception as e:
            raise FTDataException
        else:
            super(LocationPoint, self).save(**kwargs)

    def __unicode__(self):
        return '{} ({} {})'.format(self.address, self.longitude, self.latitude)


service = FusionTableClient().start_service()
