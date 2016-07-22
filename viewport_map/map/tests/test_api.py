from __future__ import unicode_literals

import json

import mock
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from viewport_map.map.models import LocationPoint
from ..factories import LocationPointFactory


class LocationPointList(APITestCase):
    def setUp(self):
        self.url = reverse('list_points')

    def test_get_should_return_empty_list_when_no_points(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual([], json.loads(response.content))

    @mock.patch('viewport_map.map.models.service')
    def test_get_should_return_object_list_when_points_exist(self, mocked_service):
        LocationPointFactory.create(address='Address', longitude='20.0', latitude='30.0')
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            [{u'address': u'Address', u'latitude': 30.0, u'longitude': 20.0}],
            json.loads(response.content)
        )

    def test_post_should_return_400_when_no_valid_data(self):
        response = self.client.post(self.url, {'test': 'wrong'})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({
            'latitude': ['This field is required.'],
            'longitude': ['This field is required.'],
            'address': ['This field is required.']},
            json.loads(response.content)
        )

    @mock.patch('viewport_map.map.models.service.insert', side_effect=Exception)
    def test_post_should_return_500_when_exception_on_saving_to_fusion_tables(self, mocked_service_insert):
        response = self.client.post(self.url, {
            'latitude': '50.0', 'longitude': '30.0', 'address': 'Address'})
        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

    @mock.patch('viewport_map.map.models.service')
    def test_post_should_return_400_when_already_exist(self, mocked_service):
        LocationPointFactory.create(address='Address', longitude='20.0', latitude='30.0')
        response = self.client.post(self.url, {
            'latitude': '30.0', 'longitude': '20.0', 'address': 'Address'})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({
            'non_field_errors': ['The fields address, longitude, latitude must make a unique set.']}, json.loads(response.content))

    @mock.patch('viewport_map.map.models.service')
    def test_post_should_return_200_when_properly_created(self, mocked_service):
        response = self.client.post(self.url, {
            'latitude': '50.0', 'longitude': '30.0', 'address': 'Address'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual({
            "address": "Address", "longitude": 30.0, "latitude": 50.0}, json.loads(response.content))

    @mock.patch('viewport_map.map.api.service')
    def test_post_should_return_200_when_deleted_ok(self, mocked_service):
        response = self.client.delete(self.url)
        mocked_service.bulk_delete.assert_called_once_with()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'success': True}, json.loads(response.content))

    @mock.patch('viewport_map.map.models.service.bulk_delete', side_effect=Exception)
    def test_post_should_return_400_when_errors_on_delete(self, mocked_service_bulk_delete):
        LocationPointFactory.create(address='Address', longitude='20.0', latitude='30.0')
        response = self.client.delete(self.url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({'success': False}, json.loads(response.content))
        self.assertEqual(1, LocationPoint.objects.all().count())

