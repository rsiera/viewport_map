from __future__ import unicode_literals

import factory

from .models import LocationPoint


class LocationPointFactory(factory.DjangoModelFactory):
    class Meta:
        model = LocationPoint
