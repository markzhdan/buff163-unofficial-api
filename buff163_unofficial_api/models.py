from datetime import datetime
import os
from typing import Any, List, Dict, Optional, Union, TypeVar
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


class GoodsInfoItem:
    def __init__(
        self,
        can_3_d_inspect: bool,
        can_display_inspect: bool,
        can_inspect: bool,
        can_preview: bool,
        can_preview_upload: bool,
        can_search_by_patch: bool,
        can_search_by_sticker: bool,
        can_search_by_tournament: bool,
        can_specific_buy: bool,
        can_specific_paintwear_buy: bool,
        icon_url: str,
        info: Info,
        item_id: None,
        normal_icon_url: str,
        original_icon_url: str,
        specific: List[Any],
        specific_paintwear_buying_choices: List[List[str]],
        steam_price: str,
        steam_price_cny: str,
    ) -> None:
        self.can_3_d_inspect = can_3_d_inspect
        self.can_display_inspect = can_display_inspect
        self.can_inspect = can_inspect
        self.can_preview = can_preview
        self.can_preview_upload = can_preview_upload
        self.can_search_by_patch = can_search_by_patch
        self.can_search_by_sticker = can_search_by_sticker
        self.can_search_by_tournament = can_search_by_tournament
        self.can_specific_buy = can_specific_buy
        self.can_specific_paintwear_buy = can_specific_paintwear_buy
        self.icon_url = icon_url
        self.info = info
        self.item_id = item_id
        self.normal_icon_url = normal_icon_url
        self.original_icon_url = original_icon_url
        self.specific = specific
        self.specific_paintwear_buying_choices = specific_paintwear_buying_choices
        self.steam_price = steam_price
        self.steam_price_cny = steam_price_cny


class PaintseedFilter:
    def __init__(self, name: str, placeholder: str, search: bool, type: str) -> None:
        self.name = name
        self.placeholder = placeholder
        self.search = search
        self.type = type


class RelativeGood:
    def __init__(
        self,
        goods_id: int,
        goods_name: str,
        is_change: bool,
        sell_min_price: str,
        sell_num: int,
        tag: str,
        tag_name: str,
    ) -> None:
        self.goods_id = goods_id
        self.goods_name = goods_name
        self.is_change = is_change
        self.sell_min_price = sell_min_price
        self.sell_num = sell_num
        self.tag = tag
        self.tag_name = tag_name


class ShareData:
    def __init__(self, content: str, thumbnail: str, title: str, url: str) -> None:
        self.content = content
        self.thumbnail = thumbnail
        self.title = title
        self.url = url


class ListList:
    def __init__(self, title: str, value: str) -> None:
        self.title = title
        self.value = value


class SortByFieldsList:
    def __init__(
        self, attribute: str, default_value: str, list: List[ListList]
    ) -> None:
        self.attribute = attribute
        self.default_value = default_value
        self.list = list


class SortByFields:
    def __init__(self, list: List[SortByFieldsList], title: str) -> None:
        self.list = list
        self.title = title


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


class SpecificItem:
    def __init__(
        self,
        allow_bundle_inventory: bool,
        appid: int,
        asset_tags: List[Any],
        asset_tags_buy_order: List[Any],
        asset_tags_history: List[Any],
        bookmarked: bool,
        buy_num: int,
        can_buy: bool,
        can_sort_by_heat: bool,
        container_type: str,
        containers: List[str],
        description: None,
        fade_choices: List[List[int]],
        game: str,
        goods_info: GoodsInfoItem,
        has_buff_price_history: bool,
        has_bundle_inventory_order: bool,
        has_fade_name: bool,
        has_paintwear_rank: bool,
        has_related: bool,
        has_rune: bool,
        id: int,
        is_container: bool,
        item_id: None,
        market_hash_name: str,
        market_min_price: int,
        name: str,
        paintseed_filters: List[PaintseedFilter],
        paintseed_filters_buy_order: List[Any],
        paintseed_filters_history: List[Any],
        paintwear_choices: List[List[str]],
        paintwear_range: List[str],
        quick_price: int,
        rank_types: List[Any],
        recent_sold_count: int,
        relative_goods: List[RelativeGood],
        sell_min_price: str,
        sell_num: int,
        sell_reference_price: str,
        share_data: ShareData,
        short_name: str,
        show_game_cms_icon: bool,
        sort_by_fields: SortByFields,
        steam_market_url: str,
        super_short_name: str,
        support_name_tag: bool,
        transacted_num: int,
        user_show_count: int,
        wiki_link: None,
        has_rent_order: bool,
        rent_day_choices: List[int],
        rent_num: int,
        rent_sort_by_fields: SortByFields,
        support_charm: bool,
        buy_max_price: int = None,
        buy_min_price_limit: int = None,
        is_charm: bool = None,
    ) -> None:
        self.allow_bundle_inventory = allow_bundle_inventory
        self.appid = appid
        self.asset_tags = asset_tags
        self.asset_tags_buy_order = asset_tags_buy_order
        self.asset_tags_history = asset_tags_history
        self.bookmarked = bookmarked
        self.buy_max_price = buy_max_price
        self.buy_min_price_limit = buy_min_price_limit
        self.buy_num = buy_num
        self.can_buy = can_buy
        self.can_sort_by_heat = can_sort_by_heat
        self.container_type = container_type
        self.containers = containers
        self.description = description
        self.fade_choices = fade_choices
        self.game = game
        self.goods_info = goods_info
        self.has_buff_price_history = has_buff_price_history
        self.has_bundle_inventory_order = has_bundle_inventory_order
        self.has_fade_name = has_fade_name
        self.has_paintwear_rank = has_paintwear_rank
        self.has_related = has_related
        self.has_rune = has_rune
        self.id = id
        self.is_container = is_container
        self.item_id = item_id
        self.market_hash_name = market_hash_name
        self.market_min_price = market_min_price
        self.name = name
        self.paintseed_filters = paintseed_filters
        self.paintseed_filters_buy_order = paintseed_filters_buy_order
        self.paintseed_filters_history = paintseed_filters_history
        self.paintwear_choices = paintwear_choices
        self.paintwear_range = paintwear_range
        self.quick_price = quick_price
        self.rank_types = rank_types
        self.recent_sold_count = recent_sold_count
        self.relative_goods = relative_goods
        self.sell_min_price = sell_min_price
        self.sell_num = sell_num
        self.sell_reference_price = sell_reference_price
        self.share_data = share_data
        self.short_name = short_name
        self.show_game_cms_icon = show_game_cms_icon
        self.sort_by_fields = sort_by_fields
        self.steam_market_url = steam_market_url
        self.super_short_name = super_short_name
        self.support_name_tag = support_name_tag
        self.transacted_num = transacted_num
        self.user_show_count = user_show_count
        self.wiki_link = wiki_link

