import discord
from discord.ext import commands
from discord import app_commands

from ui.view import EquipmentView

class EquipmentCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="裝備", description="查看裝備")
    async def equipment(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=EquipmentView(interaction.user))

async def setup(bot: commands.Bot):
    await bot.add_cog(EquipmentCog(bot))