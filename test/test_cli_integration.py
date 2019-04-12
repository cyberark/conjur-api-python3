import os
import uuid
import unittest

import requests

from .util.cli_helpers import integration_test, invoke_cli

from conjur_api_python3.version import __version__


class CliIntegrationTest(unittest.TestCase):
    REQUIRED_ENV_VARS = {
        'CONJUR_ACCOUNT': 'account',
        'CONJUR_AUTHN_LOGIN': 'user',
        'CONJUR_AUTHN_API_KEY': 'api-key',
    }

    HTTP_ENV_VARS = {
        'CONJUR_HTTP_APPLIANCE_URL': 'url',
    }

    HTTPS_ENV_VARS = {
        'CONJUR_HTTPS_APPLIANCE_URL': 'url',
    }

    HTTPS_CA_BUNDLE_ENV_VAR = { 'CONJUR_CA_BUNDLE': 'ca-bundle' }

    DEFINED_VARIABLE_ID = 'one/password'

    def setup_cli_params(self, env_vars, *params):
        self.cli_auth_params = ['--debug']

        cli_params_map = {**self.REQUIRED_ENV_VARS, **env_vars}
        for required_env_var, param_name in cli_params_map.items():
            self.assertIsNotNone(os.environ[required_env_var],
                    'ERROR: {} env var must be available for this test to work!'.format(required_env_var))
            self.assertGreater(len(os.environ[required_env_var]), 0,
                    'ERROR: {} env var must have a valid value for this test to work!'.format(required_env_var))

            self.cli_auth_params += ['--{}'.format(param_name), os.environ[required_env_var]]

        self.cli_auth_params += params

        return self.cli_auth_params

    def set_variable(self, variable_id, value):
        return invoke_cli(self, self.cli_auth_params,
            ['variable', 'set', variable_id, value])

    def get_variable(self, variable_id):
        return invoke_cli(self, self.cli_auth_params,
            ['variable', 'get', variable_id])

    @integration_test
    def test_http_cli_can_set_and_get_a_defined_variable(self):
        self.setup_cli_params(self.HTTP_ENV_VARS)
        expected_value='expected ' + uuid.uuid4().hex

        self.set_variable(CliIntegrationTest.DEFINED_VARIABLE_ID, expected_value)
        output = self.get_variable(CliIntegrationTest.DEFINED_VARIABLE_ID)

        self.assertEquals(expected_value, output)

    @integration_test
    def test_https_cli_can_set_and_get_a_defined_variable(self):
        self.setup_cli_params({
            **self.HTTPS_ENV_VARS,
            **self.HTTPS_CA_BUNDLE_ENV_VAR
        })

        expected_value='expected ' + uuid.uuid4().hex

        self.set_variable(CliIntegrationTest.DEFINED_VARIABLE_ID, expected_value)
        output = self.get_variable(CliIntegrationTest.DEFINED_VARIABLE_ID)

        self.assertEquals(expected_value, output)

    @integration_test
    def test_https_cli_can_set_and_get_a_defined_variable_if_cert_not_provided_and_verification_disabled(self):
        self.setup_cli_params(self.HTTPS_ENV_VARS, '--insecure')
        expected_value='expected ' + uuid.uuid4().hex

        self.set_variable(CliIntegrationTest.DEFINED_VARIABLE_ID, expected_value)
        output = self.get_variable(CliIntegrationTest.DEFINED_VARIABLE_ID)

        self.assertEquals(expected_value, output)

    @integration_test
    def test_https_cli_fails_if_cert_is_bad(self):
        self.setup_cli_params(self.HTTPS_ENV_VARS, '--ca-bundle', './test/test_config/https/nginx.conf')
        expected_value='expected ' + uuid.uuid4().hex

        with self.assertRaises(requests.exceptions.SSLError):
            self.set_variable(CliIntegrationTest.DEFINED_VARIABLE_ID, expected_value)

    @integration_test
    def test_https_cli_fails_if_cert_is_not_provided(self):
        self.setup_cli_params(self.HTTPS_ENV_VARS)
        expected_value='expected ' + uuid.uuid4().hex

        with self.assertRaises(requests.exceptions.SSLError):
            self.set_variable(CliIntegrationTest.DEFINED_VARIABLE_ID, expected_value)
