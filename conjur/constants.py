# -*- coding: utf-8 -*-

"""
Constants module

This module holds all constants used across the codebase
"""

# Builtins
import os
import platform

# The OS the CLI is run on is determined by the following:
# See https://stackoverflow.com/questions/1854/python-what-os-am-i-running-on
# pylint: disable=no-member
if os.name != "posix" and platform.system() == "Windows":
    INTERNAL_FILE_PREFIX="_"

else:
    INTERNAL_FILE_PREFIX="."

DEFAULT_NETRC_FILE_NAME = INTERNAL_FILE_PREFIX + "netrc"

DEFAULT_CONFIG_FILE = os.path.expanduser(os.path.join('~', '.conjurrc'))
DEFAULT_NETRC_FILE = os.path.expanduser(os.path.join('~', DEFAULT_NETRC_FILE_NAME))
DEFAULT_CERTIFICATE_FILE = os.path.expanduser(os.path.join('~', "conjur-server.pem"))
CREDENTIAL_HOST_PATH = "/authn"

PASSWORD_COMPLEXITY_CONSTRAINTS_MESSAGE = "The password must contain at least 12 characters: " \
                                          "2 uppercase, 2 lowercase, 1 digit, 1 special character"

# For testing purposes
TEST_HOSTNAME = "https://conjur-https"
