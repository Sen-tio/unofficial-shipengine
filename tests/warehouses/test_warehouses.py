import unittest
import vcr

from src.unofficial_shipengine.core.warehouses import WarehouseRequest, Warehouse
from src.unofficial_shipengine.core.common import Address


class TestWarehouses(unittest.TestCase):
    def test_create_warehouse_success(self):
        warehouse_request: WarehouseRequest = WarehouseRequest()


if __name__ == "__main__":
    unittest.main()
