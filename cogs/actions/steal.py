import discord
from discord.ext import commands
from discord import app_commands

from game import action
from utils import messenger

class StealCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.context_menu = app_commands.ContextMenu(name="偷竊", callback=self.execute)
        self.bot.tree.add_command(self.context_menu)

    @app_commands.command(name="偷竊", description="偷取他人的物品")
    async def steal(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        await self.execute(interaction, member)

    async def execute(self, interaction: discord.Interaction, member: discord.Member):
        event = await action.steal(interaction, member)
        await messenger.send(event, interaction)

async def setup(bot):
    await bot.add_cog(StealCog(bot))