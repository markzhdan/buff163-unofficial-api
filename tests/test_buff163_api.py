from unittest import TestCase
from unittest.mock import MagicMock
from buff163_unofficial_api.buff163_api import Buff163API
from buff163_unofficial_api.models import Item, Result


class TestBuff163API(TestCase):
    def setUp(self) -> None:
        self.buff163api = Buff163API(page_size=10)
        self.buff163api._rest_adapter = MagicMock()

    def test_get_featured_market_item_returns_one_item(self):
        self.buff163api._rest_adapter.get.return_value = Result(
            200, headers={}, data=[{"id": 1, "url": "example.com"}]
        )
        item = self.buff163api.get_featured_market_item()
        self.assertIsInstance(item, Item)

    def test_get_featured_market_returns_list_of_items(self):
        item_amt = 2
        self.buff163api._rest_adapter.get.return_value = Result(
            200,
            headers={},
            data=[
                {"id": 1, "url": "example.com"},
                {"id": 2, "url": "example.com"},
                {"id": 3, "url": "example.com"},
            ],
        )
        item_list = self.buff163api.get_featured_market(amt=item_amt)
        self.assertIsInstance(item_list, list)
        self.assertTrue(len(item_list), item_amt)
        self.assertIsInstance(item_list[0], Item)

    def test_get_featured_market_paged_returns_iterator_of_item(self):
        self.buff163api._rest_adapter.get.side_effect = [
            Result(
                200,
                headers={},
                data=[
                    {"id": 1, "url": "example.com"},
                    {"id": 2, "url": "example.com"},
                    {"id": 3, "url": "example.com"},
                ],
            ),
            Result(200, headers={}, data=[]),
        ]
        item_iterator = self.buff163api.get_featured_market_paged()
        item1 = next(item_iterator)
        item2 = next(item_iterator)
        item3 = next(item_iterator)
        self.assertIsInstance(item3, Item)
        with self.assertRaises(StopIteration):
            item4 = next(item_iterator)
