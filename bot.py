import discord
from discord.ext import commands

from game.model import init_all_databases
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
            "cogs.role",
            "cogs.market",
            "cogs.setting",

            "cogs.listeners.interaction",
            "cogs.listeners.join",
            "cogs.listeners.message",
            "cogs.listeners.reaction",
            "cogs.listeners.voice",

            "cogs.admins.announce",
            "cogs.admins.boot",
            "cogs.admins.house",
            "cogs.admins.member",
            "cogs.admins.test_message",
            "cogs.admins.test_multiple_select",

            "cogs.actions.steal",

            "cogs.menus.inventory",
            "cogs.menus.leaderboard",
            "cogs.menus.stat",
        ]

        for extension in extensions:
            await self.load_extension(extension)

        synced_global = await self.tree.sync()
        logger.info(f'Synced {len(synced_global)} commands to Global')