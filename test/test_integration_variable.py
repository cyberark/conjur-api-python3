# -*- coding: utf-8 -*-

"""
CLI Variable Integration tests
This test file handles the main test flows for the variable command
"""
import io
import json
import os
import tempfile
import uuid
from contextlib import redirect_stderr
from unittest.mock import patch

import Utils
from conjur.constants import DEFAULT_NETRC_FILE
from .test_integration_cli import CliIntegrationTest
from .util.cli_helpers import integration_test
from test.util.test_runners.integration_test_case import IntegrationTestCaseBase
from Utils import py_utils as utils

# Not coverage tested since integration tests don't run in
# the same build step
class CliIntegrationVariableTest(IntegrationTestCaseBase):  # pragma: no cover
    DEFINED_VARIABLE_ID = 'one/password'
    capture_stream = io.StringIO()
    def __init__(self, testname, client_params=None, environment_params=None):
        super(CliIntegrationVariableTest, self).__init__(testname, client_params, environment_params)

    # *************** HELPERS ***************

    def setup_cli_params(self, env_vars, *params):
        self.cli_auth_params = ['--debug']
        self.cli_auth_params += params

        return self.cli_auth_params

    def setUp(self):
        self.setup_cli_params({})
        # Need to configure the CLI and login to perform further commands
        Utils.setup_cli(self)
        return self.invoke_cli(self.cli_auth_params,
                               ['policy', 'replace', 'root', self.environment.path_provider.get_policy_path("initial")])

    # *************** TESTS ***************

    @integration_test
    def test_variable_without_subcommand_returns_help(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable'], exit_code=0)
        self.assertIn("Usage:\n  conjur [global options] <command> <subcommand> [options] [args]", output)

    # TODO This will need to be changed when UX is finalized
    @integration_test
    def test_variable_short_with_help_returns_variable_help(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', '-h'], exit_code=0)
        self.assertIn("usage:  variable", output)

    # TODO This will need to be changed when UX is finalized
    @integration_test
    def test_variable_long_with_help_returns_variable_help(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', '--help'], exit_code=0)
        self.assertIn("usage:  variable", output)

    @integration_test
    def test_variable_get_variable_without_subcommand_raises_error(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', '-i', 'somevariable'], exit_code=1)

        self.assertIn("usage:  variable", output)

    @integration_test
    def test_variable_get_long_variable_returns_variable_value(self):
        expected_value = uuid.uuid4().hex
        Utils.set_variable(self, 'one/password', expected_value)
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', 'get', '--id=one/password'], exit_code=0)
        self.assertIn(expected_value, output)

    @integration_test
    def test_variable_get_short_variable_returns_variable_value(self):
        expected_value = uuid.uuid4().hex
        Utils.set_variable(self, 'one/password', expected_value)
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', 'get', '-i', 'one/password'], exit_code=0)
        self.assertIn(expected_value, output)

    @integration_test
    def test_variable_get_with_special_chars_returns_special_chars(self):
        self.invoke_cli(self.cli_auth_params,
                       ['policy', 'replace', 'root', self.environment.path_provider.get_policy_path("variable")])
        Utils.set_variable(self, 'variablespecialchars', '"[]{}#@^&<>~\/''\/?\;\';\'"')
        output = Utils.get_variable(self, 'variablespecialchars')
        self.assertEquals(output.strip(), '"[]{}#@^&<>~\/''\/?\;\';\'"')

    @integration_test
    def test_variable_get_variable_has_spaces_returns_variable_value(self):
        self.invoke_cli(self.cli_auth_params,
                       ['policy', 'replace', 'root', self.environment.path_provider.get_policy_path("variable")])
        Utils.assert_set_and_get(self, "some variable with spaces")

    @integration_test
    def test_unknown_variable_raises_not_found_error(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', 'get', '-i', 'unknown'], exit_code=1)
        self.assertRegex(output, "404 Client Error: Not Found for url:")

    @integration_test
    def test_cli_can_batch_get_multiple_variables(self):
        policy, variables = Utils.generate_policy_string(self)
        file_name=os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        with open(file_name, 'w+b') as temp_policy_file:
            temp_policy_file.write(policy.encode('utf-8'))
            temp_policy_file.flush()

            Utils.apply_policy(self, temp_policy_file.name)
        value_map = {}
        for variable in variables:
            value = uuid.uuid4().hex
            Utils.set_variable(self, variable, value)
            value_map[variable] = value

        batch_result_string = Utils.get_variable(self, *variables)
        batch_result = json.loads(batch_result_string)

        for variable_name, variable_value in value_map.items():
            self.assertEquals(variable_value, batch_result[variable_name])

        os.remove(file_name)

    @integration_test
    def test_batch_existing_and_nonexistent_variable_raises_error(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', 'get', '-i', 'one/password,unknown'], exit_code=1)
        self.assertIn("404 Client Error", output)

    # TODO This will need to be changed when UX is finalized
    @integration_test
    def test_subcommand_get_short_help_returns_help(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', 'get', '-h'], exit_code=0)
        self.assertIn("usage: variable", output)

    # TODO This will need to be changed when UX is finalized
    @integration_test
    def test_subcommand_get_long_help_returns_help(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', 'get', '--help'], exit_code=0)
        self.assertIn("usage: variable", output)

    @integration_test
    def test_subcommand_get_help_returns_help(self):
        with redirect_stderr(self.capture_stream):
            self.invoke_cli(self.cli_auth_params,
                            ['variable', 'get'], exit_code=1)
        self.assertIn("Error the following arguments are required:", self.capture_stream.getvalue())

    @integration_test
    def test_subcommand_set_help_returns_help(self):
        with redirect_stderr(self.capture_stream):
            self.invoke_cli(self.cli_auth_params,
                            ['variable', 'set'], exit_code=1)
        self.assertIn("Error the following arguments are required:", self.capture_stream.getvalue())

    # TODO This will need to be changed when UX is finalized
    @integration_test
    def test_subcommand_set_long_help_returns_help(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', 'set', '--help'], exit_code=0)
        self.assertIn("usage: variable set", output)

    # TODO This will need to be changed when UX is finalized
    @integration_test
    def test_subcommand_set_short_help_returns_help(self):
        output = self.invoke_cli(self.cli_auth_params,
                                 ['variable', 'set', '-h'], exit_code=0)
        self.assertIn("usage: variable set", output)

    # TODO This will need to be changed when UX is finalized
    @integration_test
    def test_subcommand_set_variable_with_values_returns_help(self):
        with redirect_stderr(self.capture_stream):
            self.invoke_cli(self.cli_auth_params,
                            ['variable', 'set', '-i', 'one/password'], exit_code=1)
        self.assertIn("Error the following arguments are required: value", self.capture_stream.getvalue())


    @integration_test
    def test_cli_can_set_and_get_a_defined_variable(self):
        Utils.assert_set_and_get(self, CliIntegrationTest.DEFINED_VARIABLE_ID)

    @integration_test
    def test_subcommand_set_variable_with_values_returns_help(self):
        with redirect_stderr(self.capture_stream):
            self.invoke_cli(self.cli_auth_params,
                            ['variable', 'set', '-i', 'one/password', '-v', 'somevalue', 'someothervalue'], exit_code=1)
        self.assertIn("Error unrecognized arguments: someothervalue", self.capture_stream.getvalue())

    '''
    Validates that when the user isn't logged in and makes a request,
    they are prompted to login first and then the command is executed
    '''
    @integration_test
    @patch('builtins.input', return_value='admin')
    def test_variable_get_without_user_logged_in_prompts_login_and_performs_get(self, mock_input):
        # TEST_ENV is set to False so we will purposely be prompted to login
        os.environ['TEST_ENV'] = 'False'
        try:
            utils.remove_file(DEFAULT_NETRC_FILE)
        except OSError:
            pass

        with patch('getpass.getpass', return_value=self.client_params.env_api_key):
            output = self.invoke_cli(self.cli_auth_params,
                                     ['variable', 'set', '-i', 'one/password', '-v', 'somevalue'], exit_code=0)

            self.assertIn("Error: You have not logged in", output)
            self.assertIn("Successfully logged in to Conjur", output)
            self.assertIn('Value set: \'one/password\'', output)
        os.environ['TEST_ENV'] = 'True'

    @integration_test
    def test_https_cli_can_set_and_get_a_defined_variable_if_verification_disabled(self):
        self.setup_cli_params({}, '--insecure')
        Utils.assert_set_and_get(self, CliIntegrationTest.DEFINED_VARIABLE_ID)