import json
import logging
import requests
import sys
import os
from faas import __version__ as version


class FaasAPIClient:

    def __init__(self, access_token=None,
                 endpoint="https://api.sonra.io", refresh_token=None):
        # defaults
        self.password = None
        self.username = None
        self.user_agent = f'FaaS SDK v{version}'
        # load logger
        self.logger = logging.getLogger('root')

        # Static
        self.endpoint = endpoint
        # generate request to get access token

        # save access token
        self.access_token = access_token
        self.refresh_token = refresh_token

    def _send_request(self, endpoint, data=None, files=None,
                      method='get', multipart=False):
        url = self._generate_url(endpoint)
        headers = {}
        headers.update(self._generate_bearer_header())
        headers.update(self._generate_user_agent())
        self.logger.debug('Sending request [%s] [%s] [%s]',
                          url, data, headers)

        if (data or files) and method == 'get':
            method = 'post'

        params = {
            'headers': headers
        }

        if data:
            if multipart:
                params['data'] = data
            else:
                params['json'] = data

        if files:
            params['files'] = files

        response = requests.request(method=method, url=url, **params)
        if response.status_code != 200:
            if response.content:
                self.logger.debug(response.json())

            _errors = response.json()['errors']
            for _error in _errors:
                print(f'Error: {_error}')
                sys.exit(2)

        if response.content:
            try:
                return response.json()
            except json.decoder.JSONDecodeError:
                pass
            return response.text
        else:
            return True

    def _generate_bearer_header(self):
        return {
            'authorization': 'Bearer ' + self.access_token,
        }

    def _generate_user_agent(self):
        return {
            'User-Agent': self.user_agent
        }

    def _generate_url(self, endpoint):
        return self.endpoint + '/' + endpoint

    # authentication
    def get_access_token(self, username=None, password=None):
        if username is None:
            data = {
                'username': self.username,
                'password': self.password
            }
        else:
            data = {
                'username': username,
                'password': password
            }

        headers = {}
        headers.update(self._generate_user_agent())
        response = requests.post(self._generate_url('oauth/token'), data, headers=headers)
        if response.status_code != 200:
            return False

        response_json = response.json()
        return response_json['access_token'], response_json['refresh_token']

    # Schema source
    def list_schema_sources(self):
        return self._send_request('schema_sources')

    def get_schema_source(self, name):
        return self._send_request('schema_sources/{}'.format(name))

    def delete_schema_source(self, name):
        return self._send_request('schema_sources/{}'.format(name),
                                  method='delete')

    def create_file_schema_source(self, name, file):
        with open(file, 'rb') as fp:
            data = {
                'source_type': 'uploaded_file'
            }
            files = {
                'file': fp
            }
            return self._send_request('schema_sources/{}'.format(name),
                                      files=files, data=data, multipart=True)

    def create_s3_schema_source(self, name, path, role_arn):
        data = {
            'path': path,
            'role_arn': role_arn,
            'source_type': 's3'
        }
        return self._send_request('schema_sources/{}'.format(name),
                                  data=data, multipart=True)

    def create_http_schema_source(self, name, url):
        data = {'url': url,
                'source_type': 'http'}
        return self._send_request('schema_sources/{}'.format(name),
                                  data=data, multipart=True)

    # Data Source
    def list_data_sources(self):
        return self._send_request('data_sources')

    def get_data_source(self, name):
        return self._send_request('data_sources/{}'.format(name))

    def delete_data_source(self, name):
        return self._send_request('data_sources/{}'.format(name),
                                  method='delete')

    # ---> Get all files of certain type from the folder
    def prepare_folder_as_source(self, _folder, _type):
        with os.scandir(_folder) as _entries:
            _fffs = [_entry.path for _entry in _entries
                     if self.check_extension(_entry, _type)]
        return _fffs

    # ---> Returns file's type
    def check_extension(self, _name, _ext):
        if not os.path.isfile(_name.path):
            return False
        _extension = _name.name.split('.')[-1]
        if _extension in _ext:
            return True

    # ---> File(s) as data_source creation
    def create_file_data_source(self, name, _type, _file):
        if isinstance(_file, str):
            _file = [_file]
        # Check whether source is a folder
        if len(_file) == 1 and _file[0][-1] == os.path.sep:
            _file = self.prepare_folder_as_source(_file[0], _type)
        data = {
            'data_type': _type,
            'source_type': 'uploaded_file'
        }
        _files = list()
        for _f in _file:
            _files.append(('file', open(_f, 'rb')))

        _r = self._send_request('data_sources/{}'.format(name),
                                data=data, files=_files, multipart=True)
        for _f in _files:
            _f[1].close()
        return _r

    def create_s3_data_source(self, name, _type, path, role_arn):
        data = {
            'path': path,
            'role_arn': role_arn,
            'data_type': _type,
            'source_type': 's3'
        }
        return self._send_request('data_sources/{}'.format(name),
                                  data=data, multipart=True)

    # -------> HTTP data_source creation
    def create_source_http(self, _name, _url, _type):
        data = {
            'url': _url,
            'data_type': _type,
            'source_type': 'http'
        }
        return self._send_request('data_sources/{}'.format(_name),
                                  data=data, multipart=True)

    # Conversions
    def create_conversion(self, name, data_source, schema_source=None,
                          target="download_link", _append=None,
                          _use_stats='true'):
        data = {
            'data_source': data_source,
            'schema_source': schema_source,
            'target': target,
            'append': _append,
            'use_stats': _use_stats
        }
        return self._send_request('conversions/{}'.format(name),
                                  data=data, multipart=True)

    def list_conversions(self):
        return self._send_request('conversions')

    def get_conversion(self, name):
        return self._send_request('conversions/{}'.format(name))

    def delete_conversion(self, name):
        return self._send_request('conversions/{}'.format(name),
                                  method='delete')

    # webhooks
    def create_webhook(self, name, url):
        data = {
            'url': url
        }
        return self._send_request('webhooks/{}'.format(name),
                                  data=data, multipart=True)

    def list_webhooks(self):
        return self._send_request('webhooks')

    def get_webhook(self, name):
        return self._send_request('webhooks/{}'.format(name))

    def delete_webhook(self, name):
        return self._send_request('webhooks/{}'.format(name),
                                  method='delete')

    # Target connections
    def list_target_connections(self):
        return self._send_request('target_connections')

    def get_target_connection(self, name):
        return self._send_request('target_connections/{}'.format(name))

    def delete_target_connection(self, name):
        return self._send_request('target_connections/{}'.format(name),
                                  method='delete')

    def create_s3_target_connection(self, name, path, role_arn):
        data = {
            'path': path,
            'role_arn': role_arn,
            'target_type': 's3'
        }
        return self._send_request('target_connections/{}'.
                                  format(name), data=data, multipart=True)

    def create_postgresql_target_connection(self, name, host,
                                            username, password, database, schema):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'schema': schema,
            'target_type': 'postgresql'
        }
        return self._send_request('target_connections/{}'.format(name),
                                  data=data, multipart=True)

    def create_mysql_target_connection(self, name, host, username,
                                       password, database):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'target_type': 'mysql'
        }
        return self._send_request('target_connections/{}'.format(name),
                                  data=data, multipart=True)

    def create_snowflake_target_connection(self, name, host,
                                           username, password, database, schema=None, warehouse=None,
                                           role=None):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'schema': schema,
            'warehouse': warehouse,
            'role': role,
            'target_type': 'snowflake'
        }
        return self._send_request('target_connections/{}'.format(name),
                                  data=data, multipart=True)

    def create_sqlserver_target_connection(self, name, host, username,
                                           password, database):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'target_type': 'sqlserver'
        }
        return self._send_request('target_connections/{}'.format(name),
                                  data=data, multipart=True)

    def create_oracle_target_connection(self, name, host, username,
                                        password, database):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'target_type': 'oracle'
        }
        return self._send_request('target_connections/{}'.
                                  format(name), data=data, multipart=True)

    def create_redshift_target_connection(self, name, host,
                                          username, password, database):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'target_type': 'redshift'
        }
        return self._send_request('target_connections/{}'.
                                  format(name), data=data, multipart=True)
