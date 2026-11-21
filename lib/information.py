import discord

from datetime import datetime, timezone

from models import Player
from models import Statistic

from data import REGIONS
from data.enums import ResourceName, CurrencyName

from lib import player, resource
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

def get(member: discord.Member) -> dict:
    """
    返回玩家資料彙整後的字典，由於此處需要取得伺服器的加入時間，因此需要傳入`discord.Member`物件
    """

    # 取得資料
    _player, _ = Player.get_or_create(id = member.id)
    statistic = Statistic.get_or_create_stat(member.id)

    if not isinstance(member, discord.Member):
        raise ValueError

    # 取得加入時間與經過天數
    now = datetime.now(timezone.utc)
    join_times = now - member.joined_at
    join_days = join_times.days

    # 取得小屋資料
    houses = []
    if not _player.houses:
        houses.append("> *尚未擁有任何小屋*")
    else:
        for house in _player.houses:
            houses.append(f"- <#{house.id}>")

    # 彙總
    load = {
        "level": _player.level,
        "experience": _player.experience,
        "required_experience": player.get_experience_requirement(_player.level),
        "region": REGIONS.get(_player.region).name,
        
        "join_time": member.joined_at.strftime(f"於 %Y 年 %m 月 %d 日加入這裡，已經過 **{join_days:,}** 天"),

        "total_daily": statistic.total_daily,
        "total_message": statistic.total_message,
        "total_voice": statistic.total_voice,
        "turn": _player.turn,

        "houses": "\n".join(houses),

        "player_name": member.display_name,
        "player_avatar": member.avatar.url
    }

    return load