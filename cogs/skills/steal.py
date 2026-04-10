import discord
from discord.ext import commands
from discord import app_commands

from systems import commands as elin_commnads

class Steal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.context_menu = app_commands.ContextMenu(name="偷竊", callback=self.context_steal)
        self.bot.tree.add_command(self.context_menu)

    @app_commands.command(name="偷竊", description="偷取他人的物品")
    async def command_steal(self, interaction: discord.Interaction, member: discord.Member):
        await elin_commnads.Steal().execute(interaction, member)

    async def context_steal(self, interaction: discord.Interaction, member: discord.Member):
        await elin_commnads.Steal().execute(interaction, member)

async def setup(bot):
    await bot.add_cog(Steal(bot))