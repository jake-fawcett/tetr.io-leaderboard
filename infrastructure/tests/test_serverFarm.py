import unittest

from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.v2019_08_01.models import GenericResource
from tests import load_configuration


class serverFarm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        to_remove = "[]',"
        client = get_client_from_cli_profile(ResourceManagementClient)
        cls.config = load_configuration(cls)
        stripped_resource = str(cls.config["serverFarmID"]["value"])
        stripped_resource = stripped_resource.lower()
        stripped_resource = stripped_resource.split(",")[0]
        for i in to_remove:
            stripped_resource = stripped_resource.replace(i, "")
        cls.resource = client.resources.get_by_id(resource_id=stripped_resource, api_version="2020-06-01")

    def config(self):
        return self.__class__.config

    def resource(self) -> GenericResource:
        to_remove = "[]' "
        for i in to_remove:
            self.__class__.resource = str(self.__class__.resource).replace(i, "")
        return self.__class__.resource

    def test_is_location_allowed(self):
        locations = ["UK South", "UK West"]
        self.assertIn(self.resource.location, locations, f"Location must be one of {locations}")

    def test_is_kind_correct(self):
        self.assertEqual("linux", self.resource.kind, "Kind is Invalid!")

    def test_is_farm_sku_name_valid(self):
        self.assertEqual("F1", self.resource.sku.name, "SKU is invalid")

    def test_is_farm_sku_tier_valid(self):
        self.assertEqual("Free", self.resource.sku.tier, "SKU Tier is invalid")

    def test_is_farm_sku_size_valid(self):
        self.assertEqual("F1", self.resource.sku.size, "SKU size is invalid")

    def test_is_farm_reserved(self):
        self.assertEqual(True, self.resource.properties["reserved"], "Farm isnt reserved!")


if __name__ == "__main__":
    unittest.main()
