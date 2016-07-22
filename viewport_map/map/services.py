from __future__ import unicode_literals

import os

import httplib2
from django.conf import settings
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from viewport_map.map.sqls import INSERT_QUERY, DELETE_ALL_QUERY

CLIENT_SECRETS = os.path.join(settings.BASE_DIR, 'client_secrets.json')


class FusionTableClient(object):
    TOKEN_FILE_NAME = 'fusiontables.dat'
    SERVICE = 'fusiontables'
    SERVICE_VERSION = 'v2'

    def __init__(self):
        self.service = None
        self.db_name = settings.FUSION_TABLES_DB_ID
        self.flow = flow_from_clientsecrets(
            CLIENT_SECRETS,
            scope='https://www.googleapis.com/auth/{}'.format(self.SERVICE),
            redirect_uri='http://localhost:8000/oauth2callback'
        )

    def _authenticate(self):
        storage = Storage(self.TOKEN_FILE_NAME)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(self.flow, storage)
        return credentials

    def _create_service(self):
        http = httplib2.Http()
        credentials = self._authenticate()
        http = credentials.authorize(http)
        return build(self.SERVICE, self.SERVICE_VERSION, http=http)

    def start_service(self):
        if not self.service:
            self.service = self._create_service()
        return self

    def query(self, sql):
        return self.service.query().sql(sql=sql).execute()

    def insert(self, data):
        sql = INSERT_QUERY % (self.db_name, data.longitude, data.latitude, data.address)
        return self.query(sql)

    def bulk_delete(self):
        sql = DELETE_ALL_QUERY % self.db_name
        return self.query(sql)
