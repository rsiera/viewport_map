from __future__ import unicode_literals

from collections import namedtuple

import mock
from django.test import SimpleTestCase

from ..services import FusionTableClient

FakeLocationPoint = namedtuple('FakeLocationPoint', ['address', 'longitude', 'latitude'])


class FakeStorage(object):
    def __init__(self, invalid):
        self.invalid = invalid


class FusionTableClientTest(SimpleTestCase):
    @mock.patch('viewport_map.map.services.FusionTableClient._create_service')
    def test_start_service_should_create_service_only_once(self, mocked__create_service):
        client = FusionTableClient().start_service()
        client.start_service()
        mocked__create_service.assert_called_once_with()

    @mock.patch('viewport_map.map.services.FusionTableClient._create_service')
    @mock.patch('viewport_map.map.services.FusionTableClient.query')
    def test_insert_should_call_query_with_proper_params_when_ok(self, mocked__query, mocked__create_service):
        mocked__create_service.return_value = mock.Mock()
        client = FusionTableClient().start_service()
        client.insert(FakeLocationPoint('Address', 40.0, 50.0))
        mocked__query.assert_called_once_with(
            "INSERT INTO 15jQJZ3ZC7LtI9ZtU2r1epPObVyyMnhYngemTG3if (Long, Lat, City) VALUES (40.0, 50.0, 'Address')"
        )

    @mock.patch('viewport_map.map.services.FusionTableClient._create_service')
    @mock.patch('viewport_map.map.services.FusionTableClient.query')
    def test_delete_should_call_query_with_proper_params_when_ok(self, mocked__query, mocked__create_service):
        mocked__create_service.return_value = mock.Mock()
        client = FusionTableClient().start_service()
        client.bulk_delete()
        mocked__query.assert_called_once_with("DELETE FROM 15jQJZ3ZC7LtI9ZtU2r1epPObVyyMnhYngemTG3if")

    @mock.patch('viewport_map.map.services.Storage')
    def test__authenticate_should_return_credentials_when_storage_ok(self, mocked_storage):
        mocked_storage_get = FakeStorage(invalid=False)
        mocked_storage.return_value.get.return_value = mocked_storage_get
        credentials = FusionTableClient()._authenticate()
        self.assertEqual(mocked_storage_get, credentials)

    @mock.patch('viewport_map.map.services.Storage')
    @mock.patch('viewport_map.map.services.run_flow')
    def test__authenticate_should_call_run_flow_when_empty_storage(self, mocked_run_flow, mocked_storage):
        mocked_storage.return_value.get.return_value = None
        client = FusionTableClient()
        client._authenticate()
        mocked_run_flow.assert_called_once_with(client.flow, mocked_storage.return_value)
