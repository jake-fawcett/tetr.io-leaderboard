import unittest

from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.v2019_08_01.models import GenericResource
from tests import load_configuration


class storageAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        to_remove = "[]',"
        client = get_client_from_cli_profile(ResourceManagementClient)
        cls.config = load_configuration(cls)
        stripped_resource = str(cls.config["storageID"]["value"])
        stripped_resource = stripped_resource.lower()
        stripped_resource = stripped_resource.split(",")[0]
        for i in to_remove:
            stripped_resource = stripped_resource.replace(i, "")
        cls.resource = client.resources.get_by_id(resource_id=stripped_resource, api_version="2019-06-01")

    def config(self):
        return self.__class__.config

    def resource(self) -> GenericResource:
        to_remove = "[]' "
        for i in to_remove:
            self.__class__.resource = str(self.__class__.resource).replace(i, "")
        return self.__class__.resource

    def test_is_location_allowed(self):
        locations = ["uksouth", "ukwest"]
        self.assertIn(self.resource.location, locations, f"Location must be one of {locations}")

    def test_is_tls_set_correctly(self):
        self.assertEqual("TLS1_2", self.resource.properties["minimumTlsVersion"], "Storage Account is not set to TLS1_2!")

    def test_is_https_accepted_only(self):
        self.assertEqual(True, self.resource.properties["supportsHttpsTrafficOnly"], "Storage account accepts HTTP!")

    def test_is_accessTier_hot(self):
        self.assertEqual("Hot", self.resource.properties["accessTier"], "Storage account accesTier is not Hot!")

    def test_is_sku_tier_valid(self):
        self.assertEqual("Standard_LRS", self.resource.sku.name, "Storage account sku tier is not valid!")


if __name__ == "__main__":
    unittest.main()
