import discord

from data.enums import ResourceName, CurrencyName

from lib import resource
from lib import currency

def get_resource(user: discord.abc.User) -> dict[str, int]:
    """
    返回提供資源頁面使用的玩家資料字典
    """
    load = {}

    # 取得資源
    for res in ResourceName:
        load.update({res: resource.get(user.id, res)})

    # 取得通貨
    for cur in CurrencyName:
        load.update({cur: currency.get(user.id, cur)})

    # 取得玩家
    load.update(
        {
            "player_name"   : user.display_name,
            "player_avatar" : user.avatar.url,
        }
    )

    return load