from dataverk_vault.connectors.vault import VaultConnector
from dataverk_vault.context.settings import read_environment_settings


def read_secrets():
    settings = read_environment_settings()
    vault_conn = VaultConnector(settings)
    return vault_conn.get_secrets()


def get_database_creds(vault_path):
    settings = read_environment_settings()
    vault_conn = VaultConnector(settings)
    return vault_conn.get_db_credentials(vault_path)
