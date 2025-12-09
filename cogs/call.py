import discord
from discord import app_commands
from discord.ext import commands

from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

from utils.embed_builder import EmbedBuilder

from context import Context

class Call(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name = "呼叫", description = "呼叫管家進行對話")
    @app_commands.describe(character = "選擇角色")
    @app_commands.choices(
        character = [
            app_commands.Choice(name = "艾琳", value = "eryn")
        ]
    )

    async def call(self, interaction: discord.Interaction, character: app_commands.Choice[str]):

        key = "call_response_eryn"

        embed_builder = EmbedBuilder()
        embeds = embed_builder.create(key=key)

        view = CallView()

        await interaction.response.send_message(embeds=embeds, view=view)

class CallView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        button_manager = Context.get_manager("button")
        self.add_item(button_manager.create("final_fantasy_dedicated_rule_button"))

async def setup(bot):
    await bot.add_cog(Call(bot))