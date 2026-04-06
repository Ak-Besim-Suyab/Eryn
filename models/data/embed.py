import discord
from dataclasses import dataclass
from cores.manager import Manager

@dataclass
class Embed:
    id: str
    title: str
    description: list
    color: str

class EmbedManager(Manager[Embed]):
    def __init__(self):
        super().__init__(
            model = Embed,
            path = "assets/shops"
        )

    def create(cls, embed_id: str):
        embed = discord.Embed()
        pass

embed_manager = EmbedManager()

# embed_manager.create(EmbedType.DAILY_REWARD)

"""
{
    "id": "daily_reward",
    "title": "每日簽到",
    "description": [
        "咪！旅人可以在每天 12 點過後，點擊下方的按鈕進行簽到！",
        "",
        "> 點擊「狀態」可以查看個人狀態",
        "> 點擊「排名」可以查看等級與經驗值排名",
    ],
    "color": "discord.gold"
}
"""