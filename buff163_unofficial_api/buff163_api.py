import logging
from typing import Iterator, Callable
from buff163_unofficial_api.rest_adapter import RestAdapter
from buff163_unofficial_api.exceptions import Buff163Exception
from buff163_unofficial_api.models import *


class Buff163API:
    def __init__(
        self,
        hostname: str = "buff.163.com/api",
        session_cookie: str = "",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
        page_size: int = 20,
    ):
        """Buff163API default constructor.

        Args:
            hostname (str, optional): API url. Defaults to "buff.163.com/api".
            session_cookie (str, optional): Personal session cookie (like an api token). Defaults to "".
            ssl_verify (bool, optional): Set to false if having SSL/TLS cert validation issues. Defaults to True.
            logger (logging.Logger, optional): App logger. Defaults to None.
            page_size (int, optional): Items per page. Defaults to 20.
        """
        self._rest_adapter = RestAdapter(hostname, session_cookie, ssl_verify, logger)
        self._page_size = page_size

    def get_featured_market_item(self) -> Item:
        """Get first featured market item (random).

        Returns:
            Item: Overview of specific item.
        """
        return self.get_featured_market()[0]

    def get_featured_market(self, pageNum: int = 1) -> List[Item]:
        """Get entire featured item.

        Args:
            pageNum (int, optional): Which page number to get. Defaults to 1.

        Returns:
            List[Item]: List of overview of items.
        """
        result = self._rest_adapter.get(
            endpoint=f"/market/goods?game=csgo&page_num={pageNum}"
        )
        market = [Item(**item) for item in result.data["data"]["items"]]
        return market

    def fetch_image_data(self, item: Item):
        """Fetches Item icon.

        Args:
            item (Item): Specific Item from market.
        """
        item.data = self._rest_adapter.fetch_data(url=item.goods_info.icon_url)

    def _page(
        self, endpoint: str, model: Callable[..., Model], max_amt: int = 80
    ) -> Iterator[Model]:
        """Pages through set number of pages.

        Args:
            endpoint (str): API endpoint requested.
            model (Callable[..., Model]): Specific model that will be paged.
            max_amt (int, optional): Max items to get from pages. Defaults to 80.

        Yields:
            Iterator[Model]: List of specific model.
        """
        amt_yielded = 0
        curr_page = last_page = 1
        ep_params = {
            "game": "csgo",
            "page_size": self._page_size,
        }

        # Keep fetching pages until the last page
        while curr_page <= last_page:
            ep_params["page_num"] = curr_page
            result = self._rest_adapter.get(endpoint=endpoint, ep_params=ep_params)
            data = result.data["data"]

            # Increment curr_page by 1 and update the last_page based on header info returned
            last_page = data["total_page"]
            curr_page = data["page_num"] + 1
            for datam in data["items"]:
                yield model(**datam)
                amt_yielded += 1
                if amt_yielded >= max_amt:
                    last_page = 0
                    break

    def get_featured_market_paged(self, max_amt: int = 80) -> Iterator[Item]:
        """Page the featured market

        Args:
            max_amt (int, optional): Amount of Items to get. Defaults to 80.

        Returns:
            _type_: List of Items

        Yields:
            Iterator[Item]: List of Items
        """
        return self._page(endpoint="/market/goods", model=Item, max_amt=max_amt)
