from buff163_unofficial_api import Buff163API
from buff163_unofficial_api.models import *

# This specific example does not need a cookie
# This is how the cookie should be formatted
cookie = "Device-Id=_; Locale-Supported=_; game=_; NTES_YD_SESS=_; S_INFO=_; P_INFO=_; remember_me=_; session=_; csrf_token=_"

buff163api = Buff163API(session_cookie=cookie)

item = buff163api.get_item(900565)

print(f"{item.market_hash_name}")
print(f"Buff163 Price: ¥ {item.sell_min_price}\n")
print(f"Steam Price: ¥ {item.goods_info.steam_price_cny}\n")
