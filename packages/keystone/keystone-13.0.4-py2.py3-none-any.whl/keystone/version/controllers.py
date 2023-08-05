# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_serialization import jsonutils
from six.moves import http_client
import webob

from keystone.common import extension
from keystone.common import json_home
from keystone.common import wsgi
from keystone import exception


MEDIA_TYPE_JSON = 'application/vnd.openstack.identity-%s+json'

_VERSIONS = []

# NOTE(blk-u): latest_app will be set by keystone.version.service.loadapp(). It
# gets set to the application that was just loaded. loadapp() gets called once
# for the public app if this is the public instance or loadapp() gets called
# for the admin app if it's the admin instance. This is used to fetch the /v3
# JSON Home response. The /v3 JSON Home response is the same whether it's the
# admin or public service so either admin or public works.
latest_app = None


def request_v3_json_home(new_prefix):
    if 'v3' not in _VERSIONS:
        # No V3 support, so return an empty JSON Home document.
        return {'resources': {}}

    req = webob.Request.blank(
        '/v3', headers={'Accept': 'application/json-home'})
    v3_json_home_str = req.get_response(latest_app).body
    v3_json_home = jsonutils.loads(v3_json_home_str)
    json_home.translate_urls(v3_json_home, new_prefix)

    return v3_json_home


class Extensions(wsgi.Application):
    """Base extensions controller to be extended by public and admin API's."""

    # extend in subclass to specify the set of extensions
    @property
    def extensions(self):
        return None

    def get_extensions_info(self, request):
        return {'extensions': {'values': list(self.extensions.values())}}

    def get_extension_info(self, request, extension_alias):
        try:
            return {'extension': self.extensions[extension_alias]}
        except KeyError:
            raise exception.NotFound(target=extension_alias)


class AdminExtensions(Extensions):
    @property
    def extensions(self):
        return extension.ADMIN_EXTENSIONS


class PublicExtensions(Extensions):
    @property
    def extensions(self):
        return extension.PUBLIC_EXTENSIONS


def register_version(version):
    _VERSIONS.append(version)


class MimeTypes(object):
    JSON = 'application/json'
    JSON_HOME = 'application/json-home'


def v3_mime_type_best_match(request):

    # accept_header is a WebOb MIMEAccept object so supports best_match.
    accept_header = request.accept

    if not accept_header:
        return MimeTypes.JSON

    SUPPORTED_TYPES = [MimeTypes.JSON, MimeTypes.JSON_HOME]
    return accept_header.best_match(SUPPORTED_TYPES)


class Version(wsgi.Application):

    def __init__(self, version_type, routers=None):
        self.endpoint_url_type = version_type
        self._routers = routers

        super(Version, self).__init__()

    def _get_identity_url(self, context, version):
        """Return a URL to keystone's own endpoint."""
        url = self.base_url(context, self.endpoint_url_type)
        return '%s/%s/' % (url, version)

    def _get_versions_list(self, context):
        """The list of versions is dependent on the context."""
        versions = {}
        if 'v2.0' in _VERSIONS:
            versions['v2.0'] = {
                'id': 'v2.0',
                'status': 'deprecated',
                'updated': '2016-08-04T00:00:00Z',
                'links': [
                    {
                        'rel': 'self',
                        'href': self._get_identity_url(context, 'v2.0'),
                    }, {
                        'rel': 'describedby',
                        'type': 'text/html',
                        'href': 'https://docs.openstack.org/'
                    }
                ],
                'media-types': [
                    {
                        'base': 'application/json',
                        'type': MEDIA_TYPE_JSON % 'v2.0'
                    }
                ]
            }

        if 'v3' in _VERSIONS:
            versions['v3'] = {
                'id': 'v3.10',
                'status': 'stable',
                'updated': '2018-02-28T00:00:00Z',
                'links': [
                    {
                        'rel': 'self',
                        'href': self._get_identity_url(context, 'v3'),
                    }
                ],
                'media-types': [
                    {
                        'base': 'application/json',
                        'type': MEDIA_TYPE_JSON % 'v3'
                    }
                ]
            }

        return versions

    def get_versions(self, request):

        req_mime_type = v3_mime_type_best_match(request)
        if req_mime_type == MimeTypes.JSON_HOME:
            v3_json_home = request_v3_json_home('/v3')
            return wsgi.render_response(
                body=v3_json_home,
                headers=(('Content-Type', MimeTypes.JSON_HOME),))

        versions = self._get_versions_list(request.context_dict)
        return wsgi.render_response(
            status=(http_client.MULTIPLE_CHOICES,
                    http_client.responses[http_client.MULTIPLE_CHOICES]),
            body={
                'versions': {
                    'values': list(versions.values())
                }
            })

    def get_version_v2(self, request):
        versions = self._get_versions_list(request.context_dict)
        if 'v2.0' in _VERSIONS:
            return wsgi.render_response(body={
                'version': versions['v2.0']
            })
        else:
            raise exception.VersionNotFound(version='v2.0')

    def _get_json_home_v3(self):

        def all_resources():
            for router in self._routers:
                for resource in router.v3_resources:
                    yield resource

        return {
            'resources': dict(all_resources())
        }

    def get_version_v3(self, request):
        versions = self._get_versions_list(request.context_dict)
        if 'v3' in _VERSIONS:
            req_mime_type = v3_mime_type_best_match(request)

            if req_mime_type == MimeTypes.JSON_HOME:
                return wsgi.render_response(
                    body=self._get_json_home_v3(),
                    headers=(('Content-Type', MimeTypes.JSON_HOME),))

            return wsgi.render_response(body={
                'version': versions['v3']
            })
        else:
            raise exception.VersionNotFound(version='v3')
