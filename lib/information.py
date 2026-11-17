import discord
from discord import ui

from datetime import datetime, timezone

from models import Player
from models import Statistic

from data import CONTAINERS
from data import REGIONS

from lib import builder
from lib import player

async def get_information_view(interaction: discord.Interaction, member: discord.Member = None):

    member = interaction.user if member is None else member

    _player, _ = Player.get_or_create(id = member.id)
    statistic = Statistic.get_or_create_stat(member.id)

    if not isinstance(member, discord.Member):
        return

    # 取得加入時間與經過天數
    now = datetime.now(timezone.utc)
    join_times = now - member.joined_at
    join_days = join_times.days

    houses = []

    if not _player.houses:
        houses.append("> *尚未擁有任何小屋*")
    else:
        for house in _player.houses:
            houses.append(f"> - <#{house.id}>")

    # 請留意這裡的日期轉換佔位符，大小寫會顯示不同的時間格式
    kwargs = {
        "level": _player.level,
        "experience": _player.experience,
        "required_experience": player.get_required_exp(_player.level),

        "join_time": member.joined_at.strftime(f"於 %Y 年 %m 月 %d 日加入這裡，總共經過 {join_days} 天"),

        "total_daily": statistic.total_daily,
        "total_message": statistic.total_message,
        "total_voice": statistic.total_voice,

        "houses": "\n".join(houses),

        "display_name": member.display_name,
        "display_avator": member.avatar.url
    }

    view = ui.LayoutView(timeout = None).add_item(builder.build_container(CONTAINERS.get("information"), **kwargs))

    return view

def get(member: discord.Member):

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
    info = {
        "level": _player.level,
        "experience": _player.experience,
        "required_experience": player.get_required_exp(_player.level),
        "region": REGIONS.get(_player.region).name,

        "join_time": member.joined_at.strftime(f"於 %Y 年 %m 月 %d 日加入這裡，已經過 **{join_days}** 天"),

        "total_daily": statistic.total_daily,
        "total_message": statistic.total_message,
        "total_voice": statistic.total_voice,
        "turn": _player.turn,

        "houses": "\n".join(houses),

        "display_name": member.display_name,
        "display_avator": member.avatar.url
    }

    return info