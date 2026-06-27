from discord.ext import commands
from discord import ui
from discord import SeparatorSpacing

class AnnounceRuleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def announce_rule(self, ctx: commands.Context):
        await ctx.send(view=AnnounceRuleView())

class AnnounceRuleView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        title_content = "## Th Haven 社群守則 ⚖️"

        header_content = [
            "社群致力於提供完善且良好的遊戲與交流環境，以及自由發表、著重隱私的空間，因此希望來到這裡的旅人都能共同維護這個小地方，讓良好的風氣延續下去。"
            "假如有任何事故在社群裡發生，請務必優先聯絡管理員處理，切勿私自解決；此外，隱私權問題皆從重處理。",
        ]

        rule_manner = [
            "### 🪔 保持禮貌",
            "旅人們來自世界各地，因此希望大家交流時都能以互相尊重與包容的心態進行。"
            "交流時請保持禮貌，並且社群會適當地接受輕度的政治、宗教、種族等等以及限制級的敏感話題；"
            "儘管接受，過於裸露的色情圖文與影音，血腥、暴力、仇恨言論、殘酷描寫等令人感到不適的內容仍嚴禁發布，此外也嚴禁對特定主題過度宣揚或批判。",
        ]

        rule_right = [
            "### 🪔 尊重隱私與個人權利",
            "旅人活動時，請以不造成其他成員困擾為前提，並尊重成員個人與團體之間的權利；"
            "嚴禁在社群內進行任何形式的騷擾、霸凌、歧視，以及任何可能分裂團體、影響聲譽、侵犯隱私的行為。",
            "",
            "社群設有小火堆、小酒館與小屋等高度個人化頻道，在大部分情況下將定義為私人空間；"
            "請勿在未經同意的情況下發布其他成員在這些頻道內發送的任何個人資訊、對話、圖片等內容。"
        ]

        rule_spoiler = [
            "### 🪔 劇透防範",
            "本社群有許多劇情向相關的遊戲、動漫和電影討論，為保障大家的體驗，若有必要發布暴雷內容時請善用防雷標籤，或者在允許暴雷內容的頻道發布，語音頻道也適用此規則；"
            "除此之外，嚴禁有目的性地、惡意地發布暴雷內容，此舉將視為破壞他人權益。"
        ]

        rule_website = [
            "### 🪔 留意外部網址",
            "台灣詐騙猖獗，為保護個人資產，請勿隨意輕信並點擊任何成員以任何形式提供的可疑檔案或網址。"
            "社群會主動確認發布在頻道內的外部連結來源是否安全，若發現可疑內容時，管理員會視情況手動刪除，恕不通知。"
        ]

        rule_safety = [
            "### 🪔 線下聚安全",
            "社群成員偶爾會自發性舉辦線下聚會，大家可以自由參加；"
            "但請注意，任何線下聚會均無法受到社群的規範、約束與保護，同意並與社群成員赴約前，請務必再三確認參加的活動是否安全、成員是否足夠信任。",
            "",
            "赴約前也請務必告知身邊熟識的朋友或家人，並且在活動過程中保持警覺，切勿飲用來路不明的飲料或食物；"
            "若不慎發生任何問題或糾紛，當事人請立刻報警、聯絡管理員或向任何具備公信力的第三方申請處理。",
        ]

        header_image = ui.Thumbnail(media="https://cdn.discordapp.com/attachments/1491046495812718672/1509102625994444915/cat_staring_at_mouse.jpg")

        title = ui.TextDisplay(content=title_content)
        header = ui.Section("\n".join(header_content), accessory=header_image)

        rule_manner_text = ui.TextDisplay(content="\n".join(rule_manner))
        rule_right_text = ui.TextDisplay(content="\n".join(rule_right))
        rule_spoiler_text = ui.TextDisplay(content="\n".join(rule_spoiler))
        rule_website_text = ui.TextDisplay(content="\n".join(rule_website))
        rule_safety_text = ui.TextDisplay(content="\n".join(rule_safety))

        separator = ui.Separator(spacing=SeparatorSpacing.large)

        container = ui.Container()
        container.add_item(title)
        container.add_item(separator)
        container.add_item(header)
        container.add_item(separator)
        container.add_item(rule_manner_text)
        container.add_item(separator)
        container.add_item(rule_right_text)
        container.add_item(separator)
        container.add_item(rule_spoiler_text)
        container.add_item(separator)
        container.add_item(rule_website_text)
        container.add_item(separator)
        container.add_item(rule_safety_text)

        self.add_item(container)

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceRuleCog(bot))