from datetime import datetime, timedelta

import pkg_resources
import requests
import six
import urllib3
from google.protobuf.message import DecodeError
from requests.auth import HTTPBasicAuth
from yamcs.core.auth import Credentials
from yamcs.core.exceptions import (ConnectionFailure, NotFound, Unauthorized,
                                   YamcsError)
from yamcs.protobuf.web import rest_pb2


def _convert_user_credentials(session, token_url, username=None, password=None, refresh_token=None):
    """
    Converts username/password credentials to token credentials by
    using Yamcs as the authentication server.
    """
    if username and password:
        data = {'grant_type': 'password', 'username': username, 'password': password}
    elif refresh_token:
        data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    else:
        raise NotImplementedError()

    response = session.post(token_url, data=data)
    if response.status_code == 401:
        raise Unauthorized('401 Client Error: Unauthorized')
    elif response.status_code == 200:
        d = response.json()
        expiry = datetime.utcnow() + timedelta(seconds=d['expires_in'])
        return Credentials(access_token=d['access_token'],
                           refresh_token=d['refresh_token'],
                           expiry=expiry)
    else:
        raise YamcsError('{} Server Error'.format(response.status_code))


def _convert_service_account_credentials(session, token_url, client_id,
                                         client_secret, become):
    """
    Converts service account credentials to impersonated token credentials.
    """
    data = {'grant_type': 'client_credentials', 'become': become}

    response = session.post(token_url, data=data,
                            auth=HTTPBasicAuth(client_id, client_secret))
    if response.status_code == 401:
        raise Unauthorized('401 Client Error: Unauthorized')
    elif response.status_code == 200:
        d = response.json()
        expiry = datetime.utcnow() + timedelta(seconds=d['expires_in'])
        return Credentials(access_token=d['access_token'],
                           client_id=client_id,
                           client_secret=client_secret,
                           become=become,
                           expiry=expiry)
    else:
        raise YamcsError('{} Server Error'.format(response.status_code))


class BaseClient(object):

    def __init__(self, address, tls=False, credentials=None, user_agent=None,
                 on_token_update=None, tls_verify=True):
        if ':' in address:
            self.address = address
        else:
            self.address = address + ':8090'

        if tls:
            self.auth_root = 'https://{}/auth'.format(self.address)
            self.api_root = 'https://{}/api'.format(self.address)
            self.ws_root = 'wss://{}/_websocket'.format(self.address)
        else:
            self.auth_root = 'http://{}/auth'.format(self.address)
            self.api_root = 'http://{}/api'.format(self.address)
            self.ws_root = 'ws://{}/_websocket'.format(self.address)

        self.session = requests.Session()
        if not tls_verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.session.verify = False

        self.on_token_update = on_token_update
        self.credentials = credentials
        token_url = self.auth_root + '/token'
        if self.credentials and self.credentials.username:  # Convert u/p to bearer
            self.credentials = _convert_user_credentials(
                self.session,
                token_url,
                username=self.credentials.username,
                password=self.credentials.password)
            if self.on_token_update:
                self.on_token_update(self.credentials)
        if self.credentials and self.credentials.become:  # Impersonate from service account
            self.credentials = _convert_service_account_credentials(
                self.session,
                token_url,
                client_id=self.credentials.client_id,
                client_secret=self.credentials.client_secret,
                become=self.credentials.become,
            )

        if self.credentials and self.credentials.access_token:
            self._update_authorization_header()

        if not user_agent:
            dist = pkg_resources.get_distribution('yamcs-client')
            user_agent = 'yamcs-python-client v' + dist.version
        self.session.headers.update({'User-Agent': user_agent})

    def _update_authorization_header(self):
        self.session.headers.update({
            'Authorization': 'Bearer ' + self.credentials.access_token
        })

    def get_proto(self, path, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Accept'] = 'application/protobuf'
        kwargs.update({'headers': headers})
        return self.request('get', path, **kwargs)

    def put_proto(self, path, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Content-Type'] = 'application/protobuf'
        headers['Accept'] = 'application/protobuf'
        kwargs.update({'headers': headers})
        return self.request('put', path, **kwargs)

    def patch_proto(self, path, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Content-Type'] = 'application/protobuf'
        headers['Accept'] = 'application/protobuf'
        kwargs.update({'headers': headers})
        return self.request('patch', path, **kwargs)

    def post_proto(self, path, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Content-Type'] = 'application/protobuf'
        headers['Accept'] = 'application/protobuf'
        kwargs.update({'headers': headers})
        return self.request('post', path, **kwargs)

    def delete_proto(self, path, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Accept'] = 'application/protobuf'
        kwargs.update({'headers': headers})
        return self.request('delete', path, **kwargs)

    def _refresh_access_token(self):
        if self.credentials.become:
            self.credentials = _convert_service_account_credentials(
                self.session,
                self.auth_root + '/token',
                client_id=self.credentials.client_id,
                client_secret=self.credentials.client_secret,
                become=self.credentials.become)
        else:
            self.credentials = _convert_user_credentials(
                self.session,
                self.auth_root + '/token',
                refresh_token=self.credentials.refresh_token)
        self._update_authorization_header()
        if self.on_token_update:
            self.on_token_update(self.credentials)

    def request(self, method, path, **kwargs):
        path = '{}{}'.format(self.api_root, path)

        if self.credentials and self.credentials.is_expired():
            self._refresh_access_token()

        try:
            response = self.session.request(method, path, **kwargs)
        except requests.exceptions.SSLError as sslError:
            msg = 'Connection to {} failed: {}'.format(self.address, sslError)
            six.raise_from(ConnectionFailure(msg), None)
        except requests.exceptions.ConnectionError:
            raise ConnectionFailure('Connection to {} refused'.format(self.address))

        if 200 <= response.status_code < 300:
            return response

        exception_message = rest_pb2.RestExceptionMessage()
        try:
            exception_message.ParseFromString(response.content)
        except DecodeError:
            pass

        if response.status_code == 401:
            raise Unauthorized('401 Client Error: Unauthorized')
        elif response.status_code == 404:
            raise NotFound('404 Client Error: {}'.format(
                exception_message.msg))
        elif 400 <= response.status_code < 500:
            raise YamcsError('{} Client Error: {}'.format(
                response.status_code, exception_message.msg))
        raise YamcsError('{} Server Error: {}'.format(
            response.status_code, exception_message.msg))
