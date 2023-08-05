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

import abc

import six


@six.add_metaclass(abc.ABCMeta)
class Provider(object):
    """Interface for credential providers that support encryption."""

    @abc.abstractmethod
    def encrypt(self, credential):
        """Encrypt a credential.

        :param str credential: credential to encrypt
        :returns: encrypted credential str
        :raises: keystone.exception.CredentialEncryptionError
        """

    @abc.abstractmethod
    def decrypt(self, credential):
        """Decrypt a credential.

        :param str credential: credential to decrypt
        :returns: credential str as plaintext
        :raises: keystone.exception.CredentialEncryptionError
        """
