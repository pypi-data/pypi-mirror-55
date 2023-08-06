import requests


class VaultConnector:

    def __init__(self, settings):
        self._settings = settings

    def get_secrets(self):
        """ Fetch secrets from vault and return dict

        :return: dict: secrets
        """
        client_token = self._authenticate()
        res = requests.get(self._settings["secrets_url"],
                           headers={"X-Vault-Token": client_token})
        res.raise_for_status()
        return res.json()["data"]

    def get_db_credentials(self, vault_path):
        """ Get new database credentials

        :param vault_path: str
        :return: string with username and password
        """
        client_token = self._authenticate()
        res = requests.get(f"{self._settings['vault_address']}/v1/{vault_path}",
                           headers={"X-Vault-Token": client_token})

        res.raise_for_status()
        credentials = res.json()["data"]
        return f"{credentials['username']}:{credentials['password']}"

    def _authenticate(self):
        res = requests.post(self._settings["auth_url"],
                            json={"jwt": self._settings["token"], "role": self._settings["namespace"]})
        res.raise_for_status()
        return res.json()["auth"]["client_token"]
