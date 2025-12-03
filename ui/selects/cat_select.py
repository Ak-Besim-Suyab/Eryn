import discord

from context import Context

from utils.embed_builder import EmbedBuilder

class CatSelect(discord.ui.Select):
    def __init__(self):
        option_lines = [
            ("你是誰？", "about_eryn_info"),
            ("你可以做什麼？", "about_eryn_features"),
            ("關於社群規定", "about_community_rules"),
            ("關於社群功能", "about_community_features"),
            ("貓咪怎麼叫？", "how_cat_say"),
        ]

        options = [
            discord.SelectOption(label=label, value=value)
            for label, value in option_lines
        ]

        super().__init__(
            placeholder="選擇對話",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]
        bot = Context.bot

        embed_builder = EmbedBuilder()
        embeds = embed_builder.create(choice, 
            author = bot.user.display_name,
            portrait = bot.user.display_avatar.url
        )

        view = CatSelectView()

        await interaction.response.send_message(embeds=embeds, view=view, ephemeral=True)

class CatSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CatSelect())