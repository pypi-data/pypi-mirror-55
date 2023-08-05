# Copyright 2013 OpenStack Foundation
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

"""Extensions supporting OAuth1."""

from oslo_log import log
from oslo_serialization import jsonutils
from oslo_utils import timeutils
from six.moves import http_client
from six.moves.urllib import parse as urlparse

from keystone.common import authorization
from keystone.common import controller
from keystone.common import provider_api
from keystone.common import validation
from keystone.common import wsgi
import keystone.conf
from keystone import exception
from keystone.i18n import _
from keystone import notifications
from keystone.oauth1 import core as oauth1
from keystone.oauth1 import schema
from keystone.oauth1 import validator


CONF = keystone.conf.CONF
LOG = log.getLogger(__name__)
PROVIDERS = provider_api.ProviderAPIs


def _emit_user_oauth_consumer_token_invalidate(payload):
    # This is a special case notification that expect the payload to be a dict
    # containing the user_id and the consumer_id. This is so that the token
    # provider can invalidate any tokens in the token persistence if
    # token persistence is enabled
    notifications.Audit.internal(
        notifications.INVALIDATE_USER_OAUTH_CONSUMER_TOKENS,
        payload,
    )


class ConsumerCrudV3(controller.V3Controller):
    collection_name = 'consumers'
    member_name = 'consumer'

    @classmethod
    def base_url(cls, context, path=None):
        """Construct a path and pass it to V3Controller.base_url method."""
        # NOTE(stevemar): Overriding path to /OS-OAUTH1/consumers so that
        # V3Controller.base_url handles setting the self link correctly.
        path = '/OS-OAUTH1/' + cls.collection_name
        return controller.V3Controller.base_url(context, path=path)

    @controller.protected()
    def create_consumer(self, request, consumer):
        validation.lazy_validate(schema.consumer_create, consumer)
        ref = self._assign_unique_id(self._normalize_dict(consumer))
        consumer_ref = PROVIDERS.oauth_api.create_consumer(
            ref, initiator=request.audit_initiator
        )
        return ConsumerCrudV3.wrap_member(request.context_dict, consumer_ref)

    @controller.protected()
    def update_consumer(self, request, consumer_id, consumer):
        validation.lazy_validate(schema.consumer_update, consumer)
        self._require_matching_id(consumer_id, consumer)
        ref = self._normalize_dict(consumer)
        ref = PROVIDERS.oauth_api.update_consumer(
            consumer_id, ref, initiator=request.audit_initiator
        )
        return ConsumerCrudV3.wrap_member(request.context_dict, ref)

    @controller.protected()
    def list_consumers(self, request):
        ref = PROVIDERS.oauth_api.list_consumers()
        return ConsumerCrudV3.wrap_collection(request.context_dict, ref)

    @controller.protected()
    def get_consumer(self, request, consumer_id):
        ref = PROVIDERS.oauth_api.get_consumer(consumer_id)
        return ConsumerCrudV3.wrap_member(request.context_dict, ref)

    @controller.protected()
    def delete_consumer(self, request, consumer_id):
        user_token_ref = authorization.get_token_ref(request.context_dict)
        payload = {'user_id': user_token_ref.user_id,
                   'consumer_id': consumer_id}
        _emit_user_oauth_consumer_token_invalidate(payload)
        PROVIDERS.oauth_api.delete_consumer(
            consumer_id, initiator=request.audit_initiator
        )


class AccessTokenCrudV3(controller.V3Controller):
    collection_name = 'access_tokens'
    member_name = 'access_token'

    @classmethod
    def _add_self_referential_link(cls, context, ref):
        # NOTE(lwolf): overriding method to add proper path to self link
        ref.setdefault('links', {})
        path = '/users/%(user_id)s/OS-OAUTH1/access_tokens' % {
            'user_id': cls._get_user_id(ref)
        }
        ref['links']['self'] = cls.base_url(context, path) + '/' + ref['id']

    @controller.protected()
    def get_access_token(self, request, user_id, access_token_id):
        access_token = PROVIDERS.oauth_api.get_access_token(access_token_id)
        if access_token['authorizing_user_id'] != user_id:
            raise exception.NotFound()
        access_token = self._format_token_entity(request.context_dict,
                                                 access_token)
        return AccessTokenCrudV3.wrap_member(request.context_dict,
                                             access_token)

    @controller.protected()
    def list_access_tokens(self, request, user_id):
        if request.context.is_delegated_auth:
            raise exception.Forbidden(
                _('Cannot list request tokens'
                  ' with a token issued via delegation.'))
        refs = PROVIDERS.oauth_api.list_access_tokens(user_id)
        formatted_refs = ([self._format_token_entity(request.context_dict, x)
                           for x in refs])
        return AccessTokenCrudV3.wrap_collection(request.context_dict,
                                                 formatted_refs)

    @controller.protected()
    def delete_access_token(self, request, user_id, access_token_id):
        access_token = PROVIDERS.oauth_api.get_access_token(access_token_id)
        consumer_id = access_token['consumer_id']
        payload = {'user_id': user_id, 'consumer_id': consumer_id}
        _emit_user_oauth_consumer_token_invalidate(payload)
        return PROVIDERS.oauth_api.delete_access_token(
            user_id, access_token_id, initiator=request.audit_initiator
        )

    @staticmethod
    def _get_user_id(entity):
        return entity.get('authorizing_user_id', '')

    def _format_token_entity(self, context, entity):

        formatted_entity = entity.copy()
        access_token_id = formatted_entity['id']
        user_id = self._get_user_id(formatted_entity)
        if 'role_ids' in entity:
            formatted_entity.pop('role_ids')
        if 'access_secret' in entity:
            formatted_entity.pop('access_secret')

        url = ('/users/%(user_id)s/OS-OAUTH1/access_tokens/%(access_token_id)s'
               '/roles' % {'user_id': user_id,
                           'access_token_id': access_token_id})

        formatted_entity.setdefault('links', {})
        formatted_entity['links']['roles'] = (self.base_url(context, url))

        return formatted_entity


class AccessTokenRolesV3(controller.V3Controller):
    collection_name = 'roles'
    member_name = 'role'

    @controller.protected()
    def list_access_token_roles(self, request, user_id, access_token_id):
        access_token = PROVIDERS.oauth_api.get_access_token(access_token_id)
        if access_token['authorizing_user_id'] != user_id:
            raise exception.NotFound()
        authed_role_ids = access_token['role_ids']
        authed_role_ids = jsonutils.loads(authed_role_ids)
        refs = ([self._format_role_entity(x) for x in authed_role_ids])
        return AccessTokenRolesV3.wrap_collection(request.context_dict, refs)

    @controller.protected()
    def get_access_token_role(self, request, user_id,
                              access_token_id, role_id):
        access_token = PROVIDERS.oauth_api.get_access_token(access_token_id)
        if access_token['authorizing_user_id'] != user_id:
            raise exception.Unauthorized(_('User IDs do not match'))
        authed_role_ids = access_token['role_ids']
        authed_role_ids = jsonutils.loads(authed_role_ids)
        for authed_role_id in authed_role_ids:
            if authed_role_id == role_id:
                role = self._format_role_entity(role_id)
                return AccessTokenRolesV3.wrap_member(request.context_dict,
                                                      role)
        raise exception.RoleNotFound(role_id=role_id)

    def _format_role_entity(self, role_id):
        role = PROVIDERS.role_api.get_role(role_id)
        formatted_entity = role.copy()
        if 'description' in role:
            formatted_entity.pop('description')
        if 'enabled' in role:
            formatted_entity.pop('enabled')
        return formatted_entity


class OAuthControllerV3(controller.V3Controller):
    collection_name = 'not_used'
    member_name = 'not_used'

    def _update_url_scheme(self, request):
        """Update request url scheme with base url scheme."""
        url = self.base_url(request.context_dict, request.context_dict['path'])
        url_scheme = list(urlparse.urlparse(url))[0]
        req_url_list = list(urlparse.urlparse(request.url))
        req_url_list[0] = url_scheme
        req_url = urlparse.urlunparse(req_url_list)
        return req_url

    def create_request_token(self, request):
        oauth_headers = oauth1.get_oauth_headers(request.headers)
        consumer_id = oauth_headers.get('oauth_consumer_key')
        requested_project_id = request.headers.get('Requested-Project-Id')

        if not consumer_id:
            raise exception.ValidationError(
                attribute='oauth_consumer_key', target='request')
        if not requested_project_id:
            raise exception.ValidationError(
                attribute='Requested-Project-Id', target='request')

        # NOTE(stevemar): Ensure consumer and requested project exist
        PROVIDERS.resource_api.get_project(requested_project_id)
        PROVIDERS.oauth_api.get_consumer(consumer_id)

        url = self._update_url_scheme(request)
        req_headers = {'Requested-Project-Id': requested_project_id}
        req_headers.update(request.headers)
        request_verifier = oauth1.RequestTokenEndpoint(
            request_validator=validator.OAuthValidator(),
            token_generator=oauth1.token_generator)
        h, b, s = request_verifier.create_request_token_response(
            url,
            http_method='POST',
            body=request.params,
            headers=req_headers)
        if not b:
            msg = _('Invalid signature')
            raise exception.Unauthorized(message=msg)
        # show the details of the failure.
        oauth1.validate_oauth_params(b)
        request_token_duration = CONF.oauth1.request_token_duration
        token_ref = PROVIDERS.oauth_api.create_request_token(
            consumer_id,
            requested_project_id,
            request_token_duration,
            initiator=request.audit_initiator)

        result = ('oauth_token=%(key)s&oauth_token_secret=%(secret)s'
                  % {'key': token_ref['id'],
                     'secret': token_ref['request_secret']})

        if CONF.oauth1.request_token_duration > 0:
            expiry_bit = '&oauth_expires_at=%s' % token_ref['expires_at']
            result += expiry_bit

        headers = [('Content-Type', 'application/x-www-form-urlencoded')]
        response = wsgi.render_response(
            result,
            status=(http_client.CREATED,
                    http_client.responses[http_client.CREATED]),
            headers=headers)

        return response

    def create_access_token(self, request):
        oauth_headers = oauth1.get_oauth_headers(request.headers)
        consumer_id = oauth_headers.get('oauth_consumer_key')
        request_token_id = oauth_headers.get('oauth_token')
        oauth_verifier = oauth_headers.get('oauth_verifier')

        if not consumer_id:
            raise exception.ValidationError(
                attribute='oauth_consumer_key', target='request')
        if not request_token_id:
            raise exception.ValidationError(
                attribute='oauth_token', target='request')
        if not oauth_verifier:
            raise exception.ValidationError(
                attribute='oauth_verifier', target='request')

        req_token = PROVIDERS.oauth_api.get_request_token(
            request_token_id)

        expires_at = req_token['expires_at']
        if expires_at:
            now = timeutils.utcnow()
            expires = timeutils.normalize_time(
                timeutils.parse_isotime(expires_at))
            if now > expires:
                raise exception.Unauthorized(_('Request token is expired'))

        url = self._update_url_scheme(request)
        access_verifier = oauth1.AccessTokenEndpoint(
            request_validator=validator.OAuthValidator(),
            token_generator=oauth1.token_generator)
        try:
            h, b, s = access_verifier.create_access_token_response(
                url,
                http_method='POST',
                body=request.params,
                headers=request.headers)
        except NotImplementedError:
            # Client key or request token validation failed, since keystone
            # does not yet support dummy client or dummy request token,
            # so we will raise Unauthorized exception instead.
            try:
                PROVIDERS.oauth_api.get_consumer(consumer_id)
            except exception.NotFound:
                msg = _('Provided consumer does not exist.')
                LOG.warning(msg)
                raise exception.Unauthorized(message=msg)
            if req_token['consumer_id'] != consumer_id:
                msg = _('Provided consumer key does not match stored '
                        'consumer key.')
                LOG.warning(msg)
                raise exception.Unauthorized(message=msg)
        # The response body is empty since either one of the following reasons
        if not b:
            if req_token['verifier'] != oauth_verifier:
                msg = _('Provided verifier does not match stored verifier')
            else:
                msg = _('Invalid signature.')
            LOG.warning(msg)
            raise exception.Unauthorized(message=msg)
        # show the details of the failure.
        oauth1.validate_oauth_params(b)
        if not req_token.get('authorizing_user_id'):
            msg = _('Request Token does not have an authorizing user id.')
            LOG.warning(msg)
            raise exception.Unauthorized(message=msg)

        access_token_duration = CONF.oauth1.access_token_duration
        token_ref = PROVIDERS.oauth_api.create_access_token(
            request_token_id,
            access_token_duration,
            initiator=request.audit_initiator
        )

        result = ('oauth_token=%(key)s&oauth_token_secret=%(secret)s'
                  % {'key': token_ref['id'],
                     'secret': token_ref['access_secret']})

        if CONF.oauth1.access_token_duration > 0:
            expiry_bit = '&oauth_expires_at=%s' % (token_ref['expires_at'])
            result += expiry_bit

        headers = [('Content-Type', 'application/x-www-form-urlencoded')]
        response = wsgi.render_response(
            result,
            status=(http_client.CREATED,
                    http_client.responses[http_client.CREATED]),
            headers=headers)

        return response

    def _normalize_role_list(self, authorize_roles):
        roles = set()
        for role in authorize_roles:
            if role.get('id'):
                roles.add(role['id'])
            else:
                roles.add(PROVIDERS.role_api.get_unique_role_by_name(
                    role['name'])['id'])
        return roles

    @controller.protected()
    def authorize_request_token(self, request, request_token_id, roles):
        """An authenticated user is going to authorize a request token.

        As a security precaution, the requested roles must match those in
        the request token. Because this is in a CLI-only world at the moment,
        there is not another easy way to make sure the user knows which roles
        are being requested before authorizing.
        """
        validation.lazy_validate(schema.request_token_authorize, roles)
        if request.context.is_delegated_auth:
            raise exception.Forbidden(
                _('Cannot authorize a request token'
                  ' with a token issued via delegation.'))

        req_token = PROVIDERS.oauth_api.get_request_token(request_token_id)

        expires_at = req_token['expires_at']
        if expires_at:
            now = timeutils.utcnow()
            expires = timeutils.normalize_time(
                timeutils.parse_isotime(expires_at))
            if now > expires:
                raise exception.Unauthorized(_('Request token is expired'))

        authed_roles = self._normalize_role_list(roles)

        # verify the authorizing user has the roles
        user_token = authorization.get_token_ref(request.context_dict)
        user_id = user_token.user_id
        project_id = req_token['requested_project_id']
        user_roles = PROVIDERS.assignment_api.get_roles_for_user_and_project(
            user_id, project_id)
        cred_set = set(user_roles)

        if not cred_set.issuperset(authed_roles):
            msg = _('authorizing user does not have role required')
            raise exception.Unauthorized(message=msg)

        # create list of just the id's for the backend
        role_ids = list(authed_roles)

        # finally authorize the token
        authed_token = PROVIDERS.oauth_api.authorize_request_token(
            request_token_id, user_id, role_ids)

        to_return = {'token': {'oauth_verifier': authed_token['verifier']}}
        return to_return
