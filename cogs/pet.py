import discord
from discord import app_commands
from discord.ext import commands

from database.dummy import Dummy, dummy_database

from utils.embed_builder import EmbedBuilder
from utils.logger import logger

from context import Context
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

class PetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="摸貓咪", description="摸摸管家，增加親密度！")
    async def pet(self, interaction: discord.Interaction):

        dummy_id = 0

        with dummy_database.atomic():
            dummy = Dummy.fetch(dummy_id)
            dummy.pet_count += 1
            dummy.save()

        embed_builder = EmbedBuilder()
        embeds = embed_builder.create("pet", author = "Eryn",
            parameters = {
                "pet_count": dummy.pet_count
            }
        )

        await interaction.response.send_message(embeds=embeds)
        logger.info(f'command pet used.')

async def setup(bot):
    await bot.add_cog(PetCog(bot))