import discord
from discord.ext import commands
from discord import app_commands

from game.dialogues import DialogueView

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="測試", description="測試")
    async def execute_test(self, interaction: discord.Interaction):
        dialogue = DialogueView(dialog_name="test_dialog")
        await dialogue.send(interaction)

async def setup(bot):
    await bot.add_cog(TestCog(bot))