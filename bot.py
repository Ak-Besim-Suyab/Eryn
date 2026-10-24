import discord
from discord.ext import commands

from lib import select as select_handler
from lib import button as button_handler

from models import init_databases
from cores.logger import logger

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

class Elin(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):

        init_databases()

        extensions = [
            "cogs.passport",
            "cogs.inventory",
            "cogs.leaderboard",
            "cogs.loop",

            # 隨機抽取表符系統
            "cogs.rock_paper_scissors",
            "cogs.fortune_stick",

            "cogs.listeners.emoji_dice",
            "cogs.listeners.interaction",
            "cogs.listeners.message",
            "cogs.listeners.reaction",
            "cogs.listeners.thread_fixing",
            "cogs.listeners.voice",
            "cogs.listeners.member_event",

            "cogs.admins.announce",
            "cogs.admins.boot",
            "cogs.admins.house",
            "cogs.admins.give",
        ]

        for extension in extensions:
            await self.load_extension(extension)

        # register event
        select_handler.register() 
        button_handler.register()

        synced_global = await self.tree.sync()
        logger.info(f'Synced {len(synced_global)} commands to Global')