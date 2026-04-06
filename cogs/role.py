import discord
from discord.ext import commands
from discord import app_commands

from interface.role.main import RoleImage, RoleEmbed, RoleView

from configuration import GUILD_TH_HAVEN, GUILD_AK_BESIM

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="身分組", description="你將前往紋章院，在那裏選擇並更改你的紋章（身分組）")
    async def role(self, interaction: discord.Interaction):
        image, embed, view = RoleImage(), RoleEmbed(), RoleView()
        await interaction.response.send_message(embeds=[image, embed], view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Role(bot))