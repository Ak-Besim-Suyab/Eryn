import discord
from discord.ext import commands
from discord import app_commands

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="身分組", description="你將前往紋章院，在那裏選擇並更改你的紋章（身分組）")
    async def role(self, interaction: discord.Interaction):
        pass

async def setup(bot):
    await bot.add_cog(Role(bot))