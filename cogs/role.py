import discord
from discord.ext import commands
from discord import app_commands

from ui.roles.main import RoleEmbed, RoleView, RoleImage

from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="身分組", description="查看與搭配屬於你的身分組")
    async def role(self, interaction: discord.Interaction):

        embed = RoleEmbed()
        image = RoleImage()
        view = RoleView()

        # file = discord.File("C:\Eryn\images\college_of_arms.png")

        # await interaction.response.send_message(embed=embed, view=view)
        await interaction.response.send_message(embeds=[image, embed], view=view)

async def setup(bot):
    await bot.add_cog(Role(bot))