# -*- coding: utf-8 -*-

"""
CredentialsFromFile module

This module holds the logic for writing user-specific credentials
to a netrc file on the user's machine when they login
"""

# Builtins
import logging
import netrc
import os
import stat

# Internals
from conjur.constants import DEFAULT_NETRC_FILE
from conjur.credentials_data import CredentialsData

class CredentialsFromFile:
    """
    CredentialsFromFile

    This class holds logic when credentials are kept in the netrc
    """
    def __init__(self, netrc_path=DEFAULT_NETRC_FILE):
        self.netrc_path = netrc_path

    def save(self, credential_data):
        """
        Method that writes user data to a netrc file
        and updates permissions on the file
        """
        if os.path.exists(self.netrc_path):
            netrc_obj = netrc.netrc(self.netrc_path)
            hosts = netrc_obj.hosts
            hosts[credential_data.machine] = (credential_data.login, None, credential_data.api_key)
            with open(DEFAULT_NETRC_FILE, "r+") as netrc_file:
                ret = ""
                for i, line in enumerate(str(netrc_obj).split('\n')):
                    if line.strip().startswith('machine') and not i==0:
                        ret += '\n'
                    ret += line + '\n'
                netrc_file.write(ret.replace('\t', ''))
        else:
            with open(self.netrc_path, "w+") as netrc_file:
                credential_data.pretty_print(netrc_file, f"machine {credential_data.machine}")
                credential_data.pretty_print(netrc_file, f"login {credential_data.login}")
                credential_data.pretty_print(netrc_file, f"password {credential_data.api_key}")

        # Ensures that the netrc file is only available its owner
        os.chmod(self.netrc_path, stat.S_IRWXU)

    def remove_credentials(self, conjurrc):
        """
        Method that removes netrc data from the file.
        Triggered during a logout
        """
        loaded_netrc = self.load(conjurrc)
        CredentialsData.remove_entry_from_file(loaded_netrc, DEFAULT_NETRC_FILE)

    def load(self, conjurrc):
        """
        Method that loads the netrc data.
        Triggered before each CLI action
        """
        # pylint: disable=logging-fstring-interpolation
        logging.debug(f"Retrieving credentials from file: {self.netrc_path}")
        loaded_netrc = {}
        netrc_host_url = ""
        netrc_obj = netrc.netrc(self.netrc_path)
        try:
            for host in netrc_obj.hosts:
                if conjurrc.appliance_url in host:
                    netrc_host_url = host
                    netrc_auth = netrc_obj.authenticators(netrc_host_url)

            login_id, _, api_key = netrc_auth

            loaded_netrc['machine'] = netrc_host_url
            loaded_netrc['api_key'] = api_key
            loaded_netrc['login_id'] = login_id

            return loaded_netrc
        except Exception:
            # pylint: disable=raise-missing-from
            raise Exception("Please log in")
