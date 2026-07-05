from discord.ext import commands
from discord import ui
from discord import SeparatorSpacing

from assets import image, text

class AnnounceManualCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def announce_manual(self, ctx: commands.Context):
        await ctx.send(view=AnnounceManualView())

class AnnounceManualView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        seperetor = ui.Separator(spacing=SeparatorSpacing.large)

        container = ui.Container()
        container.add_item(ui.TextDisplay(content=text.get("manual_title")))
        container.add_item(ui.Section(text.get("manual_overview"), accessory=ui.Thumbnail(image.get("broken_map"))))

        section_keys = [
            ("manual_intro_rule", 1509068887768174633),
            ("manual_intro_channel", 1208117274037190686),
            ("manual_intro_cabin", 1209461581998592021),
        ]

        for text_key, channel_key in section_keys:
            button = ui.Button(label="詳情", url=f"https://discord.com/channels/1190027756482859038/{channel_key}", emoji="🌐")
            section = ui.Section(text.get(text_key), accessory = button)
            container.add_item(seperetor)
            container.add_item(section)

        # --------------------------------------

        container_2 = ui.Container()
        container_2.add_item(ui.TextDisplay(content=text.get("explore_title")))

        chatting_row_keys = [
            ("小火堆", 1190043435009331230, "🍂"),
            ("小酒館", 1226069418170257503, "🍺"),
        ]

        activity_row_keys = [
            ("每日簽到", 1507942995473858670, "🎁")
        ]

        introduce_row_keys = [
            ("自我介紹", 1192574716242825267, "📋"),
            ("身分組問卷", "customize-community", "📝"),
            ("外觀設定", 1508517762706968668, "🎨"),
        ]

        section_keys = [
            ("explore_chatting", "over_the_garden_wall", chatting_row_keys),
            ("explore_activity", "cat_onfire", activity_row_keys),
            ("explore_introducing", "cat_disguise", introduce_row_keys)
        ]

        for text_key, image_key, row_keys in section_keys:
            container_2.add_item(seperetor)
            container_2.add_item(ui.Section(text.get(text_key), accessory=ui.Thumbnail(media=image.get(image_key))))

            row = ui.ActionRow()
            for label, channel_id, emoji in row_keys:
                url = f"https://discord.com/channels/1190027756482859038/{channel_id}"
                button = ui.Button(label=label, url=url, emoji=emoji)
                row.add_item(button)

            container_2.add_item(row)

        self.add_item(container)
        self.add_item(container_2)

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceManualCog(bot))