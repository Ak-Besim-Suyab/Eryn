import discord
import asyncio

from utils.embed_builder import EmbedBuilder

from context import Context

class FinalFantasyDedicatedRuleButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "最終幻想特別說明",
            emoji = "📜",
            style = discord.ButtonStyle.secondary,
            custom_id = "ffxiv_dedicated_rule_button"
        )

    async def callback(self, interaction: discord.Interaction):

        dialogues = [
            "final_fantasy_dedicated_rule_1",
            "final_fantasy_dedicated_rule_2",
            "final_fantasy_dedicated_rule_3"
        ]

        author = interaction.client.user.display_name
        portrait = interaction.client.user.display_avatar.url
        color = 10984191

        sleep_time = 3.3

        embed_builder = EmbedBuilder()

        await interaction.response.defer(thinking=False)

        for dialogue in dialogues:
            embeds = embed_builder.create(
                dialogue = dialogue,
                author = author,
                portrait = portrait,
                color = color,
                timestamp = True
            )

            if dialogue == "final_fantasy_dedicated_rule_2":
                view = BaseView()
            else:
                view = discord.ui.View()

            async with interaction.channel.typing():
                await asyncio.sleep(sleep_time)

            await interaction.followup.send(
                embeds = embeds,
                view = view,
                allowed_mentions = discord.AllowedMentions(roles=False),
                ephemeral = True
            )

class BaseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        button_manager = Context.get_manager("button")

        button_ffxiv_global = button_manager.create("ffxiv_global_role_button")
        button_ffxiv_chinese = button_manager.create("ffxiv_chinese_role_button")
        button_ffxiv_global_spoiler = button_manager.create("ffxiv_global_spoiler_role_button")
        button_ffxiv_chinese_spoiler = button_manager.create("ffxiv_chinese_spoiler_role_button")

        button_ffxiv_global.row = 0
        button_ffxiv_chinese.row = 0
        button_ffxiv_global_spoiler.row = 1
        button_ffxiv_chinese_spoiler.row = 1

        self.add_item(button_ffxiv_global)
        self.add_item(button_ffxiv_chinese)
        self.add_item(button_ffxiv_global_spoiler)
        self.add_item(button_ffxiv_chinese_spoiler)