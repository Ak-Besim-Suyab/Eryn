import discord
from discord.ext import commands
from discord import app_commands

from game.actions import steal

class StealCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.context_menu = app_commands.ContextMenu(name="偷竊", callback=self.steal)
        self.bot.tree.add_command(self.context_menu)

    @app_commands.command(name="偷竊", description="偷取他人的物品")
    async def command(self, interaction: discord.Interaction, member: discord.Member):
        await self.steal(interaction, member)

    async def steal(self, interaction: discord.Interaction, member: discord.Member):
        await steal.execute(interaction, member)

async def setup(bot):
    await bot.add_cog(StealCog(bot))