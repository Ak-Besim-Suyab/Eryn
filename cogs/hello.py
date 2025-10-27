import discord
from discord.ext import commands
from discord import app_commands

from context import Context

GUILD_TH_HAVEN = discord.Object(id=1193049715638538280)
GUILD_AK_BESIM = discord.Object(id=1190027756482859038)

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="hello", description="打招呼，或者測試一些東西！",)
    async def hello(self, interaction: discord.Interaction):
        interaction.client.dispatch("call_something", " --- This is a message for testing ---", interaction)
        await interaction.response.send_message("您好，這是個測試訊息！")

async def setup(bot):
    await bot.add_cog(Hello(bot))