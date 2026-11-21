import discord
from discord.ext import commands
from discord import app_commands

from lib import information, view

class CharacterCardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="角色卡", description="輸入這個指令可以查看角色卡，角色卡內有關於你的各項資料、紀錄與統計")
    async def info_command(self, interaction: discord.Interaction):

        info = information.get(interaction.user)
        await interaction.response.send_message(view=view.create("information", **info), ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(CharacterCardCog(bot))