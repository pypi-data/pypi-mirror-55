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

from oslo_config import cfg
from oslo_log import versionutils

from keystone.conf import utils


enabled = cfg.BoolOpt(
    'enabled',
    default=True,
    deprecated_for_removal=True,
    deprecated_reason=utils.fmt("""
Disabling the trusts API is deprecated. This option will be removed in the
next release and trusts will always be enabled.
"""),
    deprecated_since=versionutils.deprecated.QUEENS,
    help=utils.fmt("""
Delegation and impersonation features using trusts can be optionally disabled.
"""))

allow_redelegation = cfg.BoolOpt(
    'allow_redelegation',
    default=False,
    help=utils.fmt("""
Allows authorization to be redelegated from one user to another, effectively
chaining trusts together. When disabled, the `remaining_uses` attribute of a
trust is constrained to be zero.
"""))

max_redelegation_count = cfg.IntOpt(
    'max_redelegation_count',
    default=3,
    help=utils.fmt("""
Maximum number of times that authorization can be redelegated from one user to
another in a chain of trusts. This number may be reduced further for a specific
trust.
"""))

driver = cfg.StrOpt(
    'driver',
    default='sql',
    help=utils.fmt("""
Entry point for the trust backend driver in the `keystone.trust` namespace.
Keystone only provides a `sql` driver, so there is no reason to change this
unless you are providing a custom entry point.
"""))


GROUP_NAME = __name__.split('.')[-1]
ALL_OPTS = [
    enabled,
    allow_redelegation,
    max_redelegation_count,
    driver,
]


def register_opts(conf):
    conf.register_opts(ALL_OPTS, group=GROUP_NAME)


def list_opts():
    return {GROUP_NAME: ALL_OPTS}
