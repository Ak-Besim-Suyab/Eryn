import discord
from discord.ext import commands

from game.model import init_all_databases
from cores.logger import logger

from cogs.admins import AnnounceCabinView
from cogs.admins import AnnounceChannelView
from cogs.admins import AnnounceManualView
from cogs.admins import AnnounceRoleView
from cogs.admins import AnnounceRuleView

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
            "cogs.setting",
            "cogs.test",

            "cogs.listeners.interaction",
            "cogs.listeners.message",
            "cogs.listeners.reaction",
            "cogs.listeners.voice",
            "cogs.listeners.member_event",

            "cogs.admins.announce_cabin",
            "cogs.admins.announce_channel",
            "cogs.admins.announce_manual",
            "cogs.admins.announce_role",
            "cogs.admins.announce_rule",
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

        self.add_view(AnnounceCabinView())
        self.add_view(AnnounceChannelView())
        self.add_view(AnnounceManualView())
        self.add_view(AnnounceRoleView())
        self.add_view(AnnounceRuleView())

        synced_global = await self.tree.sync()
        logger.info(f'Synced {len(synced_global)} commands to Global')