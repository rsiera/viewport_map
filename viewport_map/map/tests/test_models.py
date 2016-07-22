import mock
from django.test import TestCase

from ..exceptions import FTDataException
from ..models import LocationPoint


class LocationPointTest(TestCase):
    @mock.patch('viewport_map.map.models.service.insert', side_effect=Exception)
    def test_save_should_save_when_no_exception(self, mocked_service_insert):
        point = LocationPoint(address='Address', longitude='40.0', latitude='50.0')
        with self.assertRaises(FTDataException):
            point.save()
        self.assertFalse(LocationPoint.objects.all().exists())

    @mock.patch('viewport_map.map.models.service.insert')
    def test_save_should_save_when_no_exception(self, mocked_service_insert):
        mocked_service_insert.return_value = {}
        point = LocationPoint(address='Address', longitude='40.0', latitude='50.0')
        point.save()
        self.assertEqual(point, LocationPoint.objects.get(pk=point.pk))
