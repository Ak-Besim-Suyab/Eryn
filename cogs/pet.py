import discord
from discord import app_commands
from discord.ext import commands
import random

from database.dummy import Dummy, dummy_database
from database.player import Player, player_database

from utils.embed_builder import EmbedBuilder
from utils.logger import logger

from context import Context
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

class PetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="摸貓咪", description="摸摸管家，增加親密度！")
    async def execute(self, interaction: discord.Interaction):
        result = await pet(interaction)

        embed_builder = EmbedBuilder()

        dialogue = result["status"]
        author = "Eryn"

        if dialogue == "pet_succeed":
            embeds = embed_builder.create(dialogue=dialogue, author=author,
                parameters = {"pet_count": result["pet_count"]}
            )

            if result.get("bonus"):
                dialogue = result["bonus"]
                bonus_embeds = embed_builder.create(dialogue=dialogue,
                    parameters = {"currency": result["bonus_currency"]}
                )
                embeds += bonus_embeds

        else:
            embeds = embed_builder.create(dialogue=dialogue, author=author)

        await interaction.response.send_message(embeds=embeds, view=PetView())
        logger.info(f'command pet used.')
        
class PetView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(PetAgainButton())

class PetAgainButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label = "繼續摸", style = discord.ButtonStyle.primary)
    
    async def callback(self, interaction: discord.Interaction):
        result = await pet(interaction)

        embed_builder = EmbedBuilder()

        dialogue = result["status"]
        author = "Eryn"

        if dialogue == "pet_succeed":
            embeds = embed_builder.create(dialogue=dialogue, author=author,
                parameters = {"pet_count": result["pet_count"]}
            )

            if result.get("bonus"):
                dialogue = result["bonus"]
                bonus_embeds = embed_builder.create(dialogue=dialogue,
                    parameters = {"currency": result["bonus_currency"]}
                )
                embeds += bonus_embeds

        else:
            embeds = embed_builder.create(dialogue=dialogue, author=author)

        await interaction.response.send_message(embeds=embeds, view=PetView())
        logger.info(f'command pet used.')

async def pet(interaction: discord.Interaction):

    result = {}

    if random.random() < 0.30:
        result["status"] = "pet_fail"
        return result

    dummy_id = 0

    with dummy_database.atomic():
        dummy = Dummy.fetch(dummy_id)
        dummy.pet_count += 1
        dummy.save()

    result["status"] = "pet_succeed"
    result["pet_count"] = dummy.pet_count

    if random.random() < 0.50:
        bonus_currency = random.randint(3, 7)

        player = Player.increase_currency(interaction.user.id, bonus_currency)

        result["bonus"] = "bonus_money_event"
        result["bonus_currency"] = bonus_currency

    return result

async def setup(bot):
    await bot.add_cog(PetCog(bot))