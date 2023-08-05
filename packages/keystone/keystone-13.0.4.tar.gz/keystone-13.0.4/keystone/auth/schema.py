# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from keystone.common.validation import parameter_types


token_issue = {
    'type': 'object',
    'properties': {
        'identity': {
            'type': 'object',
            'properties': {
                'methods': {
                    'type': 'array',
                    'items': {'type': 'string', },
                },
                'password': {
                    'type': 'object',
                    'properties': {
                        'user': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string', },
                                'name': {'type': 'string', },
                                'password': {'type': 'string', },
                                'domain': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'string', },
                                        'name': {'type': 'string', },
                                    },
                                },
                            },
                        },
                    },
                },
                'token': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string',
                        },
                    },
                    'required': ['id', ],
                },
            },
            'required': ['methods', ],
        },
        'scope': {
            # For explicit unscoped authentication the type should not be
            # strictly string. Although keystone server specifies the value
            # to be 'unscoped', old versions of keystoneauth might still be
            # using `"scope": {'unscoped': {}}` instead of
            # `"scope": "unscoped"`
            # https://bugs.launchpad.net/keystoneauth/+bug/1637682/
            'type': ['object', 'string'],
            'properties': {
                'project': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string', },
                        'id': {'type': 'string', },
                        'domain': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string', },
                                'name': {'type': 'string', },
                            },
                        },
                    },
                },
                'domain': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string', },
                        'name': {'type': 'string', },
                    },
                },
                'OS-TRUST:trust': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string', },
                    }
                },
                'system': {
                    'type': 'object',
                    'properties': {
                        'all': parameter_types.boolean
                    }
                }
            },
        },
    },
    'required': ['identity', ],
}
