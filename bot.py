import discord
from discord.ext import commands

from lib import select as select_handler
from lib import button as button_handler

from models import init_databases
from cores.logger import logger

from cogs.buildings.sanctuary import SanctuaryView
from cogs.world_map import WorldMapView

class Elin(commands.Bot):
    def __init__(self):

        intents = discord.Intents.default()
        intents.voice_states = True
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):

        init_databases()

        extensions = [
            # 常態指令
            "cogs.character_tab",
            "cogs.stash",
            "cogs.leaderboard",
            "cogs.loop",
            "cogs.item",
            "cogs.fishing",
            "cogs.equipment",
            "cogs.world_map",

            # 建築
            "cogs.buildings.sanctuary",

            # 設定（圖案身分組）
            "cogs.setting.ffxiv_role",
            "cogs.setting.minecraft_role",
            "cogs.setting.pikmin_role",
            "cogs.setting.afternoon_tea_role",
            "cogs.setting.plurk_role",

            # 設定（顏色身分組）
            "cogs.setting.gradient_role",
            "cogs.setting.flower_role",
            "cogs.setting.food_role",

            # 隨機抽取系統
            "cogs.rock_paper_scissors",
            "cogs.fortune_stick",

            # 監聽事件
            "cogs.listeners.interaction",
            "cogs.listeners.message",
            "cogs.listeners.reaction",
            "cogs.listeners.thread_fixing",
            "cogs.listeners.voice",
            "cogs.listeners.member_event",
            "cogs.listeners.dice",

            # 管理員指令
            "cogs.admins.announce",
            "cogs.admins.boot",
            "cogs.admins.house",
            "cogs.admins.give",

            # 單元測試用
            "cogs.admins.unittest",
        ]

        for extension in extensions:
            await self.load_extension(extension)

        # register event
        select_handler.register() 
        button_handler.register()

        self.add_view(SanctuaryView())
        self.add_view(WorldMapView())

        synced_global = await self.tree.sync()
        logger.info(f'Synced {len(synced_global)} commands to Global')