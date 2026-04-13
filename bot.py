import discord
from discord.ext import commands

# from interface.season_event import SeasonEventView
# from interface.role.announcement import RoleAnnouncementView

from ui.views import (
    MarketView,
    MarketChooseView,
    DailyView
    )

from models import init_all_databases
from cores.logger import logger

from utils.managers import view_manager

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

class Elin(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):

        init_all_databases()

        extensions = [
            "cogs.admin",
            "cogs.daily",
            "cogs.leveling",
            "cogs.role",
            "cogs.stat",
            "cogs.leaderboard",
            "cogs.market",
            "cogs.inventory",
            "cogs.region",
            "cogs.play",
            "cogs.setting",
            "cogs.listeners.join",
            "cogs.listeners.message",
            "cogs.admins.member",
            "cogs.admins.house",
            "cogs.admins.test",
            "cogs.admins.notice",
            "cogs.actions.steal",
        ]

        for extension in extensions:
            await self.load_extension(extension)

        self.add_view(DailyView())
        # self.add_view(SeasonEventView())
        # self.add_view(RoleAnnouncementView())

        view_manager.add(MarketView.id, MarketView)
        view_manager.add(MarketChooseView.id, MarketChooseView)
        view_manager.add(DailyView.id, DailyView)

        synced_global = await self.tree.sync()
        logger.info(f'Synced {len(synced_global)} commands to Global')