from discord.ext import commands
from discord import ui
from discord import SeparatorSpacing

from assets import image

class AnnounceCabinCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def announce_cabin(self, ctx: commands.Context):
        await ctx.send(view=AnnounceCabinView())

class AnnounceCabinView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        img_kiki_family = ui.Thumbnail(media=image.get("kiki_family").url)
        img_kiki_help = ui.Thumbnail(media=image.get("kiki_help").url)
        img_kiki_light = ui.Thumbnail(media=image.get("kiki_light").url)
        img_kiki_sweat = ui.Thumbnail(media=image.get("kiki_sweat").url)

        title = ui.TextDisplay(content="## 個人小屋 🏕️")

        content_about = [
            "### 🚪 關於小屋",

            "社群將特別供給旅人使用的個人語音頻道稱之為小屋，小屋是本社群獨有的經營模式；每位來到這裡的旅人都可以擁有專屬於自己的小屋。",
            "",
            "旅人可以自由布置小屋並邀請親朋好友加入聊天；"
            "您甚至可以擁有複數個小屋，並在這裡建立屬於自己的小型社區，省下建立臨時群組的煩惱。",
        ]

        content_how_to_get = [
            "### 🚪 如何獲得小屋",

            "社群會在不定期維護與更新時，根據旅人的活躍度即時新增小屋，旅人只要加入社群超過一個月，且活躍度不為零即可符合條件。",
            "",
            "旅人也可以直接向管理員申請新增小屋，這個項目屬於成員權益，您可以在任何有需要的時候直接提出，無需顧慮任何問題。",
        ]

        content_right = [
            "### 🚪 使用權利",
            
            "旅人獲得小屋的同時也將擁有該小屋大部分權限，您可以隨自己的意願對小屋進行任何操作，例如：修改名稱、調整權限、設定是否公開等等。",
            "",
            "使用小屋時請注意，旅人對小屋的所有操作都均會受到社群守則的約束與保護；此外，社群保有對小屋的所有最終修改與變更權。",
        ]

        content_duty = [
            "### 🚪 社群義務",

            "當旅人開始使用小屋時，將擁有管理與維護小屋的義務；當然，這些義務並非強迫性，旅人可以自由決定使用社群資源的深度，剩餘的部分仍由社群承擔。",
            "",
            "社群的本意是希望能透過提供像小屋這樣的個人化空間，讓大家都能共同經營這個小地方。如果旅人喜歡小屋這樣的經營模式，社群也希望大家都能好好使用、珍惜並愛護這些社群資源。 ",
        ]

        separator = ui.Separator(spacing=SeparatorSpacing.large)

        container = ui.Container()
        container.add_item(title)
        container.add_item(separator)
        container.add_item(ui.Section("\n".join(content_about), accessory=img_kiki_family))
        container.add_item(separator)
        container.add_item(ui.Section("\n".join(content_how_to_get), accessory=img_kiki_help))
        container.add_item(separator)
        container.add_item(ui.Section("\n".join(content_right), accessory=img_kiki_light))
        container.add_item(separator)
        container.add_item(ui.Section("\n".join(content_duty), accessory=img_kiki_sweat))

        self.add_item(container)

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceCabinCog(bot))