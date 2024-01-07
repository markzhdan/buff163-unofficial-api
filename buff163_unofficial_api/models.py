import os
from enum import Enum
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


class Category(Enum):
    NONE = "weapon_none"
    BUTTERFLY = "weapon_knife_butterfly"
    M9_BAYONET = "weapon_knife_m9_bayonet"
    KARAMBIT = "weapon_knife_karambit"
    SKELETON = "weapon_knife_skeleton"
    BAYONET = "weapon_bayonet"
    TALON = "weapon_knife_widowmaker"
    NOMAD = "weapon_knife_outdoor"
    FLIP = "weapon_knife_flip"
    STILETTO = "weapon_knife_stiletto"
    CLASSIC = "weapon_knife_css"
    URSUS = "weapon_knife_ursus"
    HUNTSMAN = "weapon_knife_tactical"
    PARACORD = "weapon_knife_cord"
    SURVIVAL = "weapon_knife_canis"
    FALCHION = "weapon_knife_falchion"
    SHADOW_DAGGERS = "weapon_knife_push"
    BOWIE = "weapon_knife_survival_bowie"
    GUT = "weapon_knife_gut"
    NAVAJA = "weapon_knife_gypsy_jackknife"
    DEAGLE = "weapon_deagle"
    ELITE = "weapon_elite"
    FIVESEVEN = "weapon_fiveseven"
    GLOCK = "weapon_glock"
    P228 = "weapon_p228"
    USP = "weapon_usp"
    AK47 = "weapon_ak47"
    AUG = "weapon_aug"
    AWP = "weapon_awp"
    FAMAS = "weapon_famas"
    G3SG1 = "weapon_g3sg1"
    GALIL = "weapon_galil"
    GALILAR = "weapon_galilar"
    M249 = "weapon_m249"
    M3 = "weapon_m3"
    M4A1 = "weapon_m4a1"
    MAC10 = "weapon_mac10"
    MP5NAVY = "weapon_mp5navy"
    P90 = "weapon_p90"
    SCOUT = "weapon_scout"
    SG550 = "weapon_sg550"
    SG552 = "weapon_sg552"
    TMP = "weapon_tmp"
    UMP45 = "weapon_ump45"
    XM1014 = "weapon_xm1014"
    BIZON = "weapon_bizon"
    MAG7 = "weapon_mag7"
    NEGEV = "weapon_negev"
    SAWEDOFF = "weapon_sawedoff"
    TEC9 = "weapon_tec9"
    TASER = "weapon_taser"
    HKP2000 = "weapon_hkp2000"
    MP7 = "weapon_mp7"
    MP9 = "weapon_mp9"
    NOVA = "weapon_nova"
    P250 = "weapon_p250"
    SCAR17 = "weapon_scar17"
    SCAR20 = "weapon_scar20"
    SG556 = "weapon_sg556"
    SSG08 = "weapon_ssg08"
    KNIFEGG = "weapon_knifegg"
    KNIFE = "weapon_knife"
    FLASHBANG = "weapon_flashbang"
    HEGRENADE = "weapon_hegrenade"
    SMOKEGRENADE = "weapon_smokegrenade"
    MOLOTOV = "weapon_molotov"
    DECOY = "weapon_decoy"
    INCGRENADE = "weapon_incgrenade"
    C4 = "weapon_c4"
    SPORT = "weapon_sport_gloves"
    SPECIALIST = "weapon_specialist_gloves"
    MOTO = "weapon_moto_gloves"
    DRIVER = "weapon_driver_gloves"
    HAND_WRAPS = "weapon_hand_wraps"
    BROKEN_FANG = "weapon_brokenfang_gloves"
    HYDRA = "weapon_hydra_gloves"
    BLOODHOUND = "weapon_bloodhound_gloves"
