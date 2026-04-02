import discord
from discord.ext import commands

from interface.daily import DailyView
from interface.season_event import SeasonEventView
from interface.role.announcement import RoleAnnouncementView

from models import init_all_databases
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM
from cores.logger import logger

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
            "cogs.listeners.join",
            "cogs.listeners.message",
            "cogs.admins.member",
            "cogs.admins.house",
            "cogs.admins.test",
        ]

        for extension in extensions:
            await self.load_extension(extension)

        self.add_view(DailyView())
        self.add_view(SeasonEventView())
        self.add_view(RoleAnnouncementView())

        synced_haven = await self.tree.sync(guild=GUILD_TH_HAVEN)
        synced_besim = await self.tree.sync(guild=GUILD_AK_BESIM)

        logger.info(f'Synced {len(synced_haven)} commands to guild Th Haven')
        logger.info(f'Synced {len(synced_besim)} commands to guild Ak Besim')