from logging import getLogger
from os import environ

import hvac

from dagster import resource


LOGGER = getLogger(__name__)


class Vault:
    client = None

    hostname = None
    token = None

    def __init__(self):
        self.hostname = environ.get("VAULT_ADDR")
        self.token = environ.get("VAULT_TOKEN")
        self.keys = environ.get("VAULT_KEYS").split(",")

        self.client = hvac.Client(
            url=self.hostname, token=self.token, verify=False
        )

        if not self.client.sys.is_initialized():
            raise Exception("Vault not initialized")

        if self.client.sys.is_sealed():
            self.client.sys.submit_unseal_keys(self.keys)

    def get_data(self, path):
        response = self.client.secrets.kv.read_secret_version(path=path)
        return response["data"]["data"]


@resource
def vault(init_context):
    return Vault()
