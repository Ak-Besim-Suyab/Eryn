import discord
from discord.ext import commands

from models import init_all_databases
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
            "cogs.attendance",
            "cogs.leveling",
            "cogs.role",
            "cogs.market",
            "cogs.region",
            "cogs.play",
            "cogs.setting",

            "cogs.listeners.join",
            "cogs.listeners.message",

            "cogs.admins.boot",
            "cogs.admins.member",
            "cogs.admins.house",
            "cogs.admins.test",
            "cogs.admins.announce",

            "cogs.actions.steal",

            "cogs.menus.stat",
            "cogs.menus.inventory",
            "cogs.menus.leaderboard",
        ]

        for extension in extensions:
            await self.load_extension(extension)

        synced_global = await self.tree.sync()
        logger.info(f'Synced {len(synced_global)} commands to Global')