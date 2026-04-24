"""
該檔案負責編寫並歸納所有與選項轉換相關的幫助函式
主要入口由事件總線請求 `SelectOptionQuery` 開始, 由 `to_options` 函式接收該請求並根據 Select 物件攜帶的 custom_id 變數進行資料檢查與轉換
"""
import discord 

from game import model

from cores import query

from system.registry import shop_registry
from system.registry import item_registry

def to_options(query: model.SelectOptionQuery) -> list[discord.SelectOption]:
    """
    .. `option_params` 接收來自 Query 攜帶的 custom_id, 並將其拆解為參數串列, 理應要有雙參數傳入
    首要參數理應是資料種類, 如 shop, inventory
    次要參數理應是資料子類, 如 shop:vendor 對應商店的 vendor 資料, inventory:item 對應玩家背包的 item 資料
    """
    option_params = query.custom_id.split(":")

    match option_params[0]:
        case "shop":
            return to_shop_options(option_params[1])
        case "inventory":
            pass
        case _:
            pass
        
    return []

def to_shop_options(shop_name: str) -> list[discord.SelectOption]:
        options = []
        shop = shop_registry.get(shop_name)
        # 錯誤預防, 如果沒有獲取到資料, 或沒有填入資料名稱, 由於 discord.ui.Select 物件在沒有選項時會出現錯誤, 因此返回無效選項
        if not shop:
            options.append(discord.SelectOption(label="Invalid Option"))
            return options
        
        for item in shop.catalog:
            i = item_registry.get(item)
            option = discord.SelectOption(
                label=i.name,
                value=i.id,
                description=i.description,
                emoji=i.emoji
            )
            options.append(option)

        return options

query.register(model.SelectOptionQuery, to_options)