import discord
import asyncio

from utils.embed_builder import EmbedBuilder

class FinalFantasyDedicatedRuleButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "最終幻想特別規則",
            emoji = "📜",
            style = discord.ButtonStyle.secondary,
            custom_id = "final_fantasy_dedicated_rule_button"
        )

    async def callback(self, interaction: discord.Interaction):

        keys = [
            "final_fantasy_dedicated_rule_1",
            "final_fantasy_dedicated_rule_2",
        ]

        embed_builder = EmbedBuilder()

        await interaction.response.defer(thinking=False)

        for key in keys:
            embeds = embed_builder.create(key)

            await interaction.followup.send(embeds=embeds)
            async with interaction.channel.typing():
                await asyncio.sleep(3.0)