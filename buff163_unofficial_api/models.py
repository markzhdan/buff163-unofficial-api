import os
from typing import List, Dict, Union, TypeVar
from buff163_unofficial_api.exceptions import Buff163Exception

Model = TypeVar("Model", covariant=True)


class Result:
    def __init__(self, status_code: int, message: str = "", data: List[Dict] = None):
        """Result returned from low-level RestAdapter

        Args:
            status_code (int): The HTTP status code resulting from the API call.
            message (str, optional): Message providing additional info about result. Defaults to "".
            data (List[Dict], optional): Data returned from API call. Defaults to None.
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class Exterior:
    def __init__(
        self, category: str, id: int, internal_name: str, localized_name: str
    ) -> None:
        self.category = category
        self.id = id
        self.internal_name = internal_name
        self.localized_name = localized_name


class Tags:
    def __init__(
        self,
        exterior: Union[Exterior, dict],
        quality: Union[Exterior, dict],
        rarity: Union[Exterior, dict],
        type: Union[Exterior, dict],
        weapon: Union[Exterior, dict],
    ) -> None:
        self.exterior = Exterior(**exterior) if isinstance(exterior, dict) else exterior
        self.quality = Exterior(**quality) if isinstance(quality, dict) else quality
        self.rarity = Exterior(**rarity) if isinstance(rarity, dict) else rarity
        self.type = Exterior(**type) if isinstance(type, dict) else type
        self.weapon = Exterior(**weapon) if isinstance(weapon, dict) else weapon


class Info:
    def __init__(self, tags: Tags) -> None:
        self.tags = tags


class GoodsInfo:
    def __init__(
        self,
        icon_url: str,
        info: Union[Info, dict],
        original_icon_url: str,
        steam_price: str,
        steam_price_cny: str,
        **kwargs,
    ) -> None:
        self.icon_url = icon_url
        self.info = Info(**info) if isinstance(info, dict) else info
        self.original_icon_url = original_icon_url
        self.steam_price = steam_price
        self.steam_price_cny = steam_price_cny
        self.__dict__.update(kwargs)


class Item:
    def __init__(
        self,
        buy_max_price: str,
        buy_num: int,
        can_bargain: bool,
        goods_info: Union[GoodsInfo, dict],
        id: int,
        market_hash_name: str,
        market_min_price: int,
        name: str,
        quick_price: str,
        sell_min_price: str,
        sell_num: int,
        sell_reference_price: str,
        short_name: str,
        steam_market_url: str,
        transacted_num: int,
        data: bytes = bytes(),
        **kwargs,
    ) -> None:
        self.buy_max_price = buy_max_price
        self.buy_num = buy_num
        self.can_bargain = can_bargain
        self.goods_info = (
            GoodsInfo(**goods_info) if isinstance(goods_info, dict) else goods_info
        )
        self.id = id
        self.market_hash_name = market_hash_name
        self.market_min_price = market_min_price
        self.name = name
        self.quick_price = quick_price
        self.sell_min_price = sell_min_price
        self.sell_num = sell_num
        self.sell_reference_price = sell_reference_price
        self.short_name = short_name
        self.steam_market_url = steam_market_url
        self.transacted_num = transacted_num
        self.data = data
        self.__dict__.update(kwargs)

    def save_icon_to(self, path: str = "./", file_name: str = ""):
        if not self.data:
            raise Buff163Exception("No data to save")
        try:
            save_file_name = file_name if file_name else f"{self.market_hash_name}.jpg"
            save_path = os.path.join(path, save_file_name)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(self.data)

        except Exception as e:
            raise Buff163Exception(str(e)) from e
