import discord
from discord.ext import commands
from discord import ui
from discord import SeparatorSpacing

class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context):
        await ctx.send(view=TestView())

class TestView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        url_black_cat_onfire = "https://cdn.discordapp.com/attachments/1491046495812718672/1508877794401189959/black_cat_onfire.jpg"

        title = "## 歡迎來到避風港，這裡是旅居手冊 🎉"

        texts = [
            "歡迎旅人來到這個溫暖、可愛的小地方，這裡是以遊戲、動漫、電影為主，同時也包含非常多生活相關主題的 ACG 社群。",
            "",
            "在開始您的旅途之前，希望您可以花點時間閱讀這份手冊，手冊裡有許多重要的社群資訊與使用方式，能幫助您快速瞭解這裡。",
            "",
            "> 查看下列特點時，點擊「詳情」可引導至相關網頁，瞭解更多內容。",
        ]

        url = "https://suyab42.notion.site/Th-Haven-1d766f39eca681119979c1a3d98d775b?pvs=74"
        url_2 = "https://discord.com/channels/1190027756482859038/1208117274037190686"

        text_rule = [
            "### 📜 社群守則",
            "開始活動前，請務必先閱讀社群相關規定。社群的規定不多，大部分都是個人權益與安全宣導，希望大家都能共同維護友善社群！",
        ]

        link_button = ui.Button(label="詳情", url=url, emoji="🌐")
        section = ui.Section("\n".join(text_rule), accessory=link_button)

        text_channel = [
            "### 💡 頻道與功能",
            "社群有非常完善的頻道與分類供大家自由使用，以及多種有趣且實用的功能，還有專門為社群編寫的 Discord Bot！"
        ]

        link_button_2 = ui.Button(label="詳情", url=url_2, emoji="🌐")
        section_2 = ui.Section("\n".join(text_channel), accessory=link_button_2)

        text_cabin = [
            "### 🏕️ 個人房屋",
            "社群擁有非常特別的小屋系統，每位旅人都能擁有屬於自己的小屋，以及所有小屋的權限。您可以裝飾、布置、邀請最好的朋友加入遊玩！"
        ]

        link_button_3 = ui.Button(label="詳情", url=url_2, emoji="🌐")
        section_3 = ui.Section("\n".join(text_cabin), accessory=link_button_3)

        thumbnail = ui.Thumbnail("https://cdn.discordapp.com/attachments/1193049715638538283/1508696634081677504/a83e679f85238d22925a4a07f225bd23.jpg")

        seperetor = ui.Separator(spacing=SeparatorSpacing.large)

        container = ui.Container()
        container.add_item(ui.TextDisplay(content=title))
        container.add_item(ui.Section("\n".join(texts), accessory=thumbnail))
        container.add_item(seperetor)
        container.add_item(section)
        container.add_item(seperetor)
        container.add_item(section_2)
        container.add_item(seperetor)
        container.add_item(section_3)

        title_2 = "## 準備好開始探索 🚀"

        text_chat = [
            "### 💬 從文字開始",

            "剛開始會不好意思也沒關係，大家其實都很慢熟，旅人可以先從文字頻道聊天開始，慢慢從感興趣的話題切入，或加入大家正在玩的遊戲。"
            "旅人也不必擔心自己是否會被忽略之類的問題，請保持禮貌、互相多多關照，大家都會積極回應哦！",
        ]

        text_activity = [
            "### 🔥 保持活躍",

            "為保持活絡，社群搭載了自製的活躍度系統，旅人可以透過簽到、發送訊息、在語音掛網等各種伺服器內的活動來累積。"
            "不過旅人也無須為此感到壓力，社群對活躍度的要求非常寬鬆；社群也鼓勵大家低能量社交，偶爾露露臉也沒問題！",
        ]

        text_footer = [
            "感謝旅人看到最後，希望您在這裡可以玩得愉快！",
            "如果有任何問題或建議，歡迎聯絡管理員，或使用匿名投遞箱，幫助社群變得更好！",
        ]

        thumbnail_chat = ui.Thumbnail(media="https://cdn.discordapp.com/attachments/1193049715638538283/1508799948806951023/8e52460d-0636-4298-9c30-c9676950736e.png")
        thumbnail_activity = ui.Thumbnail(media=url_black_cat_onfire)

        container_2 = ui.Container()
        container_2.add_item(ui.TextDisplay(content=title_2))
        container_2.add_item(seperetor)
        container_2.add_item(ui.Section("\n".join(text_chat), accessory=thumbnail_chat))
        container_2.add_item(seperetor)
        container_2.add_item(ui.Section("\n".join(text_activity), accessory=thumbnail_activity))
        container_2.add_item(seperetor)
        container_2.add_item(ui.TextDisplay(content="\n".join(text_footer)))

        self.add_item(container)
        self.add_item(container_2)

async def setup(bot: commands.Bot):
    await bot.add_cog(TestCog(bot))