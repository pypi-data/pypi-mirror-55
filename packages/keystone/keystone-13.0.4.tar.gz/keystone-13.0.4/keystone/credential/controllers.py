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

import hashlib

from oslo_serialization import jsonutils

from keystone.common import controller
from keystone.common import provider_api
from keystone.common import validation
from keystone.credential import schema
from keystone import exception
from keystone.i18n import _


PROVIDERS = provider_api.ProviderAPIs


class CredentialV3(controller.V3Controller):
    collection_name = 'credentials'
    member_name = 'credential'

    def __init__(self):
        super(CredentialV3, self).__init__()
        self.get_member_from_driver = PROVIDERS.credential_api.get_credential

    def _assign_unique_id(self, ref, trust_id=None):
        # Generates and assigns a unique identifier to
        # a credential reference.
        if ref.get('type', '').lower() == 'ec2':
            try:
                blob = jsonutils.loads(ref.get('blob'))
            except (ValueError, TypeError):
                raise exception.ValidationError(
                    message=_('Invalid blob in credential'))
            if not blob or not isinstance(blob, dict):
                raise exception.ValidationError(attribute='blob',
                                                target='credential')
            if blob.get('access') is None:
                raise exception.ValidationError(attribute='access',
                                                target='blob')
            ret_ref = ref.copy()
            ret_ref['id'] = hashlib.sha256(
                blob['access'].encode('utf8')).hexdigest()
            # Update the blob with the trust_id, so credentials created
            # with a trust scoped token will result in trust scoped
            # tokens when authentication via ec2tokens happens
            if trust_id is not None:
                blob['trust_id'] = trust_id
                ret_ref['blob'] = jsonutils.dumps(blob)
            return ret_ref
        else:
            return super(CredentialV3, self)._assign_unique_id(ref)

    @controller.protected()
    def create_credential(self, request, credential):
        validation.lazy_validate(schema.credential_create, credential)
        ref = self._assign_unique_id(self._normalize_dict(credential),
                                     request.context.trust_id)
        ref = PROVIDERS.credential_api.create_credential(ref['id'], ref)
        return CredentialV3.wrap_member(request.context_dict, ref)

    @staticmethod
    def _blob_to_json(ref):
        # credentials stored via ec2tokens before the fix for #1259584
        # need json serializing, as that's the documented API format
        blob = ref.get('blob')
        if isinstance(blob, dict):
            new_ref = ref.copy()
            new_ref['blob'] = jsonutils.dumps(blob)
            return new_ref
        else:
            return ref

    @controller.filterprotected('user_id', 'type')
    def list_credentials(self, request, filters):
        hints = CredentialV3.build_driver_hints(request, filters)
        refs = PROVIDERS.credential_api.list_credentials(hints)
        ret_refs = [self._blob_to_json(r) for r in refs]
        return CredentialV3.wrap_collection(request.context_dict, ret_refs,
                                            hints=hints)

    @controller.protected()
    def get_credential(self, request, credential_id):
        ref = PROVIDERS.credential_api.get_credential(credential_id)
        ret_ref = self._blob_to_json(ref)
        return CredentialV3.wrap_member(request.context_dict, ret_ref)

    @controller.protected()
    def update_credential(self, request, credential_id, credential):
        validation.lazy_validate(schema.credential_update, credential)
        self._require_matching_id(credential_id, credential)

        ref = PROVIDERS.credential_api.update_credential(
            credential_id, credential
        )
        return CredentialV3.wrap_member(request.context_dict, ref)

    @controller.protected()
    def delete_credential(self, request, credential_id):
        return PROVIDERS.credential_api.delete_credential(credential_id)
