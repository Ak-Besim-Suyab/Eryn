import discord
from discord import app_commands
from discord.ext import commands
import random

from database.dummy import Dummy
from database.player import Player
from database.affection import Affection

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
        result = await pet(interaction.user.id)

        embed_builder = EmbedBuilder()

        embeds = embed_builder.create(
            dialogue=result["status"], 
            author="Eryn",
            parameters = {
                "pets": result.get("pets"),
                "affection": result.get("bonus_affection")
            }
        )

        if result.get("bonus"):
            bonus_embeds = embed_builder.create(
                dialogue=result["bonus"],
                parameters = {"currency": result["bonus_currency"]}
            )

            embeds += bonus_embeds

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
        result = await pet(interaction.user.id)

        embed_builder = EmbedBuilder()

        embeds = embed_builder.create(
            dialogue=result["status"], 
            author="Eryn",
            parameters = {
                "pets": result.get("pets"),
                "affection": result.get("bonus_affection")
            }
        )

        if result.get("bonus"):
            bonus_embeds = embed_builder.create(
                dialogue=result["bonus"],
                parameters = {"currency": result["bonus_currency"]}
            )

            embeds += bonus_embeds

        await interaction.response.send_message(embeds=embeds, view=PetView())
        logger.info(f'command pet used.')

async def pet(user_id: int, dummy_id: int = 0):

    base_chance = 0.7
    base_bonus_chance = 0.4

    result = {}

    if random.random() > base_chance:
        result["status"] = "pet_fail"
        return result

    pets = Dummy.increase_pets(dummy_id, 1)
    use_pet = Player.increase_use_pet(user_id, 1)

    bonus_affection = random.randint(2, 5)

    Affection.increase_affection(user_id, dummy_id, bonus_affection)

    result["status"] = "pet_succeed"
    result["pets"] = pets
    result["bonus_affection"] = bonus_affection

    if random.random() > 1 - base_bonus_chance:
        bonus_currency = random.randint(3, 7)

        player = Player.get_or_create_player(user_id)
        player.add_currency(bonus_currency)

        result["bonus"] = "bonus_money_event"
        result["bonus_currency"] = bonus_currency

    return result

async def setup(bot):
    await bot.add_cog(PetCog(bot))