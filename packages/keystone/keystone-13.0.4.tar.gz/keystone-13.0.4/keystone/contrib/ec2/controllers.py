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

"""Main entry point into the EC2 Credentials service.

This service allows the creation of access/secret credentials used for
the ec2 interop layer of OpenStack.

A user can create as many access/secret pairs, each of which is mapped to a
specific project.  This is required because OpenStack supports a user
belonging to multiple projects, whereas the signatures created on ec2-style
requests don't allow specification of which project the user wishes to act
upon.

To complete the cycle, we provide a method that OpenStack services can
use to validate a signature and get a corresponding OpenStack token.  This
token allows method calls to other services within the context the
access/secret was created.  As an example, Nova requests Keystone to validate
the signature of a request, receives a token, and then makes a request to
Glance to list images needed to perform the requested task.

"""

import abc
import sys
import uuid

from keystoneclient.contrib.ec2 import utils as ec2_utils
from oslo_serialization import jsonutils
import six
from six.moves import http_client

from keystone.common import authorization
from keystone.common import controller
from keystone.common import provider_api
from keystone.common import utils
from keystone.common import wsgi
import keystone.conf
from keystone import exception
from keystone.i18n import _

CRED_TYPE_EC2 = 'ec2'
CONF = keystone.conf.CONF
PROVIDERS = provider_api.ProviderAPIs


class V2TokenDataHelper(provider_api.ProviderAPIMixin, object):
    """Create V2 token data."""

    def v3_to_v2_token(self, v3_token_data, token_id):
        """Convert v3 token data into v2.0 token data.

        This method expects a dictionary generated from
        V3TokenDataHelper.get_token_data() and converts it to look like a v2.0
        token dictionary.

        :param v3_token_data: dictionary formatted for v3 tokens
        :param token_id: ID of the token being converted
        :returns: dictionary formatted for v2 tokens
        :raises keystone.exception.Unauthorized: If a specific token type is
            not supported in v2.

        """
        token_data = {}
        # Build v2 token
        v3_token = v3_token_data['token']

        # NOTE(lbragstad): Version 2.0 tokens don't know about any domain other
        # than the default domain specified in the configuration.
        domain_id = v3_token.get('domain', {}).get('id')
        if domain_id and CONF.identity.default_domain_id != domain_id:
            msg = ('Unable to validate domain-scoped tokens outside of the '
                   'default domain')
            raise exception.Unauthorized(msg)

        token = {}
        token['expires'] = v3_token.get('expires_at')
        token['issued_at'] = v3_token.get('issued_at')
        token['audit_ids'] = v3_token.get('audit_ids')
        if v3_token.get('bind'):
            token['bind'] = v3_token['bind']
        token['id'] = token_id

        if 'project' in v3_token:
            # v3 token_data does not contain all tenant attributes
            tenant = PROVIDERS.resource_api.get_project(
                v3_token['project']['id'])
            # Drop domain specific fields since v2 calls are not domain-aware.
            token['tenant'] = controller.V2Controller.v3_to_v2_project(
                tenant)
        token_data['token'] = token

        # Build v2 user
        v3_user = v3_token['user']

        user = controller.V2Controller.v3_to_v2_user(v3_user)

        if 'OS-TRUST:trust' in v3_token:
            v3_trust = v3_token['OS-TRUST:trust']
            # if token is scoped to trust, both trustor and trustee must
            # be in the default domain. Furthermore, the delegated project
            # must also be in the default domain
            msg = _('Non-default domain is not supported')
            if CONF.trust.enabled:
                try:
                    trust_ref = PROVIDERS.trust_api.get_trust(v3_trust['id'])
                except exception.TrustNotFound:
                    raise exception.TokenNotFound(token_id=token_id)
                trustee_user_ref = PROVIDERS.identity_api.get_user(
                    trust_ref['trustee_user_id'])
                if (trustee_user_ref['domain_id'] !=
                        CONF.identity.default_domain_id):
                    raise exception.Unauthorized(msg)
                trustor_user_ref = PROVIDERS.identity_api.get_user(
                    trust_ref['trustor_user_id'])
                if (trustor_user_ref['domain_id'] !=
                        CONF.identity.default_domain_id):
                    raise exception.Unauthorized(msg)
                if trust_ref.get('project_id'):
                    project_ref = PROVIDERS.resource_api.get_project(
                        trust_ref['project_id'])
                    if (project_ref['domain_id'] !=
                            CONF.identity.default_domain_id):
                        raise exception.Unauthorized(msg)

            token_data['trust'] = {
                'impersonation': v3_trust['impersonation'],
                'id': v3_trust['id'],
                'trustee_user_id': v3_trust['trustee_user']['id'],
                'trustor_user_id': v3_trust['trustor_user']['id']
            }

        if 'OS-OAUTH1' in v3_token:
            msg = ('Unable to validate Oauth tokens using the version v2.0 '
                   'API.')
            raise exception.Unauthorized(msg)

        if 'OS-FEDERATION' in v3_token['user']:
            msg = _('Unable to validate Federation tokens using the version '
                    'v2.0 API.')
            raise exception.Unauthorized(msg)

        # Set user roles
        user['roles'] = []
        role_ids = []
        for role in v3_token.get('roles', []):
            role_ids.append(role.pop('id'))
            user['roles'].append(role)
        user['roles_links'] = []

        token_data['user'] = user

        # Get and build v2 service catalog
        token_data['serviceCatalog'] = []
        if 'tenant' in token:
            catalog_ref = PROVIDERS.catalog_api.get_catalog(
                user['id'], token['tenant']['id'])
            if catalog_ref:
                token_data['serviceCatalog'] = self.format_catalog(catalog_ref)

        # Build v2 metadata
        metadata = {}
        metadata['roles'] = role_ids
        # Setting is_admin to keep consistency in v2 response
        metadata['is_admin'] = 0
        token_data['metadata'] = metadata

        return {'access': token_data}

    @classmethod
    def format_catalog(cls, catalog_ref):
        """Munge catalogs from internal to output format.

        Internal catalogs look like::

          {$REGION: {
              {$SERVICE: {
                  $key1: $value1,
                  ...
                  }
              }
          }

        The legacy api wants them to look like::

          [{'name': $SERVICE[name],
            'type': $SERVICE,
            'endpoints': [{
                'tenantId': $tenant_id,
                ...
                'region': $REGION,
                }],
            'endpoints_links': [],
           }]

        """
        if not catalog_ref:
            return []

        services = {}
        for region, region_ref in catalog_ref.items():
            for service, service_ref in region_ref.items():
                new_service_ref = services.get(service, {})
                new_service_ref['name'] = service_ref.pop('name')
                new_service_ref['type'] = service
                new_service_ref['endpoints_links'] = []
                service_ref['region'] = region

                endpoints_ref = new_service_ref.get('endpoints', [])
                endpoints_ref.append(service_ref)

                new_service_ref['endpoints'] = endpoints_ref
                services[service] = new_service_ref

        return list(services.values())


@six.add_metaclass(abc.ABCMeta)
class Ec2ControllerCommon(provider_api.ProviderAPIMixin, object):
    def check_signature(self, creds_ref, credentials):
        signer = ec2_utils.Ec2Signer(creds_ref['secret'])
        signature = signer.generate(credentials)
        # NOTE(davechen): credentials.get('signature') is not guaranteed to
        # exist, we need check it explicitly.
        if credentials.get('signature'):
            if utils.auth_str_equal(credentials['signature'], signature):
                return True
            # NOTE(vish): Some client libraries don't use the port when signing
            #             requests, so try again without port.
            elif ':' in credentials['host']:
                hostname, _port = credentials['host'].split(':')
                credentials['host'] = hostname
                # NOTE(davechen): we need reinitialize 'signer' to avoid
                # contaminated status of signature, this is similar with
                # other programming language libraries, JAVA for example.
                signer = ec2_utils.Ec2Signer(creds_ref['secret'])
                signature = signer.generate(credentials)
                if utils.auth_str_equal(credentials['signature'],
                                        signature):
                    return True
                raise exception.Unauthorized(
                    message=_('Invalid EC2 signature.'))
            else:
                raise exception.Unauthorized(
                    message=_('EC2 signature not supplied.'))
        # Raise the exception when credentials.get('signature') is None
        else:
            raise exception.Unauthorized(
                message=_('EC2 signature not supplied.'))

    @abc.abstractmethod
    def authenticate(self, context, credentials=None, ec2Credentials=None):
        """Validate a signed EC2 request and provide a token.

        Other services (such as Nova) use this **admin** call to determine
        if a request they signed received is from a valid user.

        If it is a valid signature, an OpenStack token that maps
        to the user/tenant is returned to the caller, along with
        all the other details returned from a normal token validation
        call.

        The returned token is useful for making calls to other
        OpenStack services within the context of the request.

        :param context: standard context
        :param credentials: dict of ec2 signature
        :param ec2Credentials: DEPRECATED dict of ec2 signature
        :returns: token: OpenStack token equivalent to access key along
                         with the corresponding service catalog and roles
        """
        raise exception.NotImplemented()

    def _authenticate(self, credentials=None, ec2credentials=None):
        """Common code shared between the V2 and V3 authenticate methods.

        :returns: user_ref, tenant_ref, roles_ref, catalog_ref
        """
        # FIXME(ja): validate that a service token was used!

        # NOTE(termie): backwards compat hack
        if not credentials and ec2credentials:
            credentials = ec2credentials

        if 'access' not in credentials:
            raise exception.Unauthorized(
                message=_('EC2 signature not supplied.'))

        creds_ref = self._get_credentials(credentials['access'])
        self.check_signature(creds_ref, credentials)

        # TODO(termie): don't create new tokens every time
        # TODO(termie): this is copied from TokenController.authenticate
        tenant_ref = self.resource_api.get_project(creds_ref['tenant_id'])
        user_ref = self.identity_api.get_user(creds_ref['user_id'])

        # Validate that the auth info is valid and nothing is disabled
        try:
            self.identity_api.assert_user_enabled(
                user_id=user_ref['id'], user=user_ref)
            self.resource_api.assert_domain_enabled(
                domain_id=user_ref['domain_id'])
            self.resource_api.assert_project_enabled(
                project_id=tenant_ref['id'], project=tenant_ref)
        except AssertionError as e:
            six.reraise(exception.Unauthorized, exception.Unauthorized(e),
                        sys.exc_info()[2])

        roles = self.assignment_api.get_roles_for_user_and_project(
            user_ref['id'], tenant_ref['id']
        )
        if not roles:
            raise exception.Unauthorized(
                message=_('User not valid for tenant.'))
        roles_ref = [self.role_api.get_role(role_id) for role_id in roles]

        catalog_ref = self.catalog_api.get_catalog(
            user_ref['id'], tenant_ref['id'])

        return user_ref, tenant_ref, roles_ref, catalog_ref

    def create_credential(self, request, user_id, tenant_id):
        """Create a secret/access pair for use with ec2 style auth.

        Generates a new set of credentials that map the user/tenant
        pair.

        :param request: current request
        :param user_id: id of user
        :param tenant_id: id of tenant
        :returns: credential: dict of ec2 credential
        """
        self.identity_api.get_user(user_id)
        self.resource_api.get_project(tenant_id)
        blob = {'access': uuid.uuid4().hex,
                'secret': uuid.uuid4().hex,
                'trust_id': request.context.trust_id}
        credential_id = utils.hash_access_key(blob['access'])
        cred_ref = {'user_id': user_id,
                    'project_id': tenant_id,
                    'blob': jsonutils.dumps(blob),
                    'id': credential_id,
                    'type': CRED_TYPE_EC2}
        self.credential_api.create_credential(credential_id, cred_ref)
        return {'credential': self._convert_v3_to_ec2_credential(cred_ref)}

    def get_credentials(self, user_id):
        """List all credentials for a user.

        :param user_id: id of user
        :returns: credentials: list of ec2 credential dicts
        """
        self.identity_api.get_user(user_id)
        credential_refs = self.credential_api.list_credentials_for_user(
            user_id, type=CRED_TYPE_EC2)
        return {'credentials':
                [self._convert_v3_to_ec2_credential(credential)
                    for credential in credential_refs]}

    def get_credential(self, user_id, credential_id):
        """Retrieve a user's access/secret pair by the access key.

        Grab the full access/secret pair for a given access key.

        :param user_id: id of user
        :param credential_id: access key for credentials
        :returns: credential: dict of ec2 credential
        """
        self.identity_api.get_user(user_id)
        return {'credential': self._get_credentials(credential_id)}

    def delete_credential(self, user_id, credential_id):
        """Delete a user's access/secret pair.

        Used to revoke a user's access/secret pair

        :param user_id: id of user
        :param credential_id: access key for credentials
        :returns: bool: success
        """
        self.identity_api.get_user(user_id)
        self._get_credentials(credential_id)
        ec2_credential_id = utils.hash_access_key(credential_id)
        return self.credential_api.delete_credential(ec2_credential_id)

    @staticmethod
    def _convert_v3_to_ec2_credential(credential):
        # Prior to bug #1259584 fix, blob was stored unserialized
        # but it should be stored as a json string for compatibility
        # with the v3 credentials API.  Fall back to the old behavior
        # for backwards compatibility with existing DB contents
        try:
            blob = jsonutils.loads(credential['blob'])
        except TypeError:
            blob = credential['blob']
        return {'user_id': credential.get('user_id'),
                'tenant_id': credential.get('project_id'),
                'access': blob.get('access'),
                'secret': blob.get('secret'),
                'trust_id': blob.get('trust_id')}

    def _get_credentials(self, credential_id):
        """Return credentials from an ID.

        :param credential_id: id of credential
        :raises keystone.exception.Unauthorized: when credential id is invalid
            or when the credential type is not ec2
        :returns: credential: dict of ec2 credential.
        """
        ec2_credential_id = utils.hash_access_key(credential_id)
        cred = self.credential_api.get_credential(ec2_credential_id)
        if not cred or cred['type'] != CRED_TYPE_EC2:
            raise exception.Unauthorized(
                message=_('EC2 access key not found.'))
        return self._convert_v3_to_ec2_credential(cred)

    def render_token_data_response(self, token_id, token_data):
        """Render token data HTTP response.

        Stash token ID into the X-Subject-Token header.

        """
        status = (http_client.OK,
                  http_client.responses[http_client.OK])
        headers = [('X-Subject-Token', token_id)]

        return wsgi.render_response(body=token_data,
                                    status=status,
                                    headers=headers)


class Ec2Controller(Ec2ControllerCommon, controller.V2Controller):

    @controller.v2_ec2_deprecated
    def authenticate(self, request, credentials=None, ec2Credentials=None):
        (user_ref, project_ref, roles_ref, catalog_ref) = self._authenticate(
            credentials=credentials, ec2credentials=ec2Credentials
        )

        method_names = ['ec2credential']

        token_id, token_data = self.token_provider_api.issue_token(
            user_ref['id'], method_names, project_id=project_ref['id'])

        v2_helper = V2TokenDataHelper()
        token_data = v2_helper.v3_to_v2_token(token_data, token_id)
        return token_data

    @controller.v2_ec2_deprecated
    def get_credential(self, request, user_id, credential_id):
        if not self._is_admin(request):
            self._assert_identity(request.context_dict, user_id)
        return super(Ec2Controller, self).get_credential(user_id,
                                                         credential_id)

    @controller.v2_ec2_deprecated
    def get_credentials(self, request, user_id):
        if not self._is_admin(request):
            self._assert_identity(request.context_dict, user_id)
        return super(Ec2Controller, self).get_credentials(user_id)

    @controller.v2_ec2_deprecated
    def create_credential(self, request, user_id, tenant_id):
        if not self._is_admin(request):
            self._assert_identity(request.context_dict, user_id)
        return super(Ec2Controller, self).create_credential(
            request, user_id, tenant_id)

    @controller.v2_ec2_deprecated
    def delete_credential(self, request, user_id, credential_id):
        if not self._is_admin(request):
            self._assert_identity(request.context_dict, user_id)
            self._assert_owner(user_id, credential_id)
        return super(Ec2Controller, self).delete_credential(user_id,
                                                            credential_id)

    def _assert_identity(self, context, user_id):
        """Check that the provided token belongs to the user.

        :param context: standard context
        :param user_id: id of user
        :raises keystone.exception.Forbidden: when token is invalid

        """
        token_ref = authorization.get_token_ref(context)

        if token_ref.user_id != user_id:
            raise exception.Forbidden(_('Token belongs to another user'))

    def _is_admin(self, request):
        """Wrap admin assertion error return statement.

        :param context: standard context
        :returns: bool: success

        """
        try:
            # NOTE(morganfainberg): policy_api is required for assert_admin
            # to properly perform policy enforcement.
            self.assert_admin(request)
            return True
        except (exception.Forbidden, exception.Unauthorized):
            return False

    def _assert_owner(self, user_id, credential_id):
        """Ensure the provided user owns the credential.

        :param user_id: expected credential owner
        :param credential_id: id of credential object
        :raises keystone.exception.Forbidden: on failure

        """
        ec2_credential_id = utils.hash_access_key(credential_id)
        cred_ref = self.credential_api.get_credential(ec2_credential_id)
        if user_id != cred_ref['user_id']:
            raise exception.Forbidden(_('Credential belongs to another user'))


class Ec2ControllerV3(Ec2ControllerCommon, controller.V3Controller):

    collection_name = 'credentials'
    member_name = 'credential'

    def _check_credential_owner_and_user_id_match(self, request, prep_info,
                                                  user_id, credential_id):
        # NOTE(morganfainberg): this method needs to capture the arguments of
        # the method that is decorated with @controller.protected() (with
        # exception of the first argument ('context') since the protected
        # method passes in *args, **kwargs. In this case, it is easier to see
        # the expected input if the argspec is `user_id` and `credential_id`
        # explicitly (matching the :class:`.ec2_delete_credential()` method
        # below).
        ref = {}
        credential_id = utils.hash_access_key(credential_id)
        ref['credential'] = self.credential_api.get_credential(credential_id)
        # NOTE(morganfainberg): policy_api is required for this
        # check_protection to properly be able to perform policy enforcement.
        self.check_protection(request, prep_info, ref)

    def authenticate(self, context, credentials=None, ec2Credentials=None):
        (user_ref, project_ref, roles_ref, catalog_ref) = self._authenticate(
            credentials=credentials, ec2credentials=ec2Credentials
        )

        method_names = ['ec2credential']

        token_id, token_data = self.token_provider_api.issue_token(
            user_ref['id'], method_names, project_id=project_ref['id'])
        return self.render_token_data_response(token_id, token_data)

    @controller.protected(callback=_check_credential_owner_and_user_id_match)
    def ec2_get_credential(self, request, user_id, credential_id):
        ref = super(Ec2ControllerV3, self).get_credential(user_id,
                                                          credential_id)
        return Ec2ControllerV3.wrap_member(request.context_dict,
                                           ref['credential'])

    @controller.protected()
    def ec2_list_credentials(self, request, user_id):
        refs = super(Ec2ControllerV3, self).get_credentials(user_id)
        return Ec2ControllerV3.wrap_collection(request.context_dict,
                                               refs['credentials'])

    @controller.protected()
    def ec2_create_credential(self, request, user_id, tenant_id):
        ref = super(Ec2ControllerV3, self).create_credential(
            request, user_id, tenant_id)
        return Ec2ControllerV3.wrap_member(request.context_dict,
                                           ref['credential'])

    @controller.protected(callback=_check_credential_owner_and_user_id_match)
    def ec2_delete_credential(self, request, user_id, credential_id):
        return super(Ec2ControllerV3, self).delete_credential(user_id,
                                                              credential_id)

    @classmethod
    def _add_self_referential_link(cls, context, ref):
        path = '/users/%(user_id)s/credentials/OS-EC2/%(credential_id)s'
        url = cls.base_url(context, path) % {
            'user_id': ref['user_id'],
            'credential_id': ref['access']}
        ref.setdefault('links', {})
        ref['links']['self'] = url
