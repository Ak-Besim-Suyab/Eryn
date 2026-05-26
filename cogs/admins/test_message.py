import discord
from discord.ext import commands
from discord import app_commands

from systems import sessions

class DialogueTestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="test_message", description="測試對話")
    async def test_dialogue(self, interaction: discord.Interaction):
        session = sessions.DialogueSession("test")
        await session.send(interaction)

async def setup(bot):
    await bot.add_cog(DialogueTestCog(bot))