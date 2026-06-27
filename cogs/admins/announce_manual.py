from discord.ext import commands
from discord import ui
from discord import SeparatorSpacing

class AnnounceManualCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def announce_manual(self, ctx: commands.Context):
        await ctx.send(view=AnnounceManualView())

class AnnounceManualView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        url_cat_onfire_img = "https://cdn.discordapp.com/attachments/1491046495812718672/1508877794401189959/black_cat_onfire.jpg"
        url_cat_disguise_img = "https://cdn.discordapp.com/attachments/1491046495812718672/1509037731475357866/cat_disguise.jpg"

        url_ch_rule = "https://discord.com/channels/1190027756482859038/1509068887768174633"
        url_ch_introduce_channel = "https://discord.com/channels/1190027756482859038/1208117274037190686"
        url_ch_cabin = "https://discord.com/channels/1190027756482859038/1209461581998592021"

        url_ch_camp = "https://discord.com/channels/1190027756482859038/1190043435009331230"
        url_ch_tarvern = "https://discord.com/channels/1190027756482859038/1226069418170257503"

        url_msg_attendance = "https://discord.com/channels/1190027756482859038/1472379536187326464/1507942995473858670"

        url_ch_introduce_self = "https://discord.com/channels/1190027756482859038/1192574716242825267"
        url_ch_customize = "https://discord.com/channels/1190027756482859038/customize-community"

        url_msg_additional_customize = "https://discord.com/channels/1190027756482859038/1472379536187326464/1508517762706968668"


        title = "## 歡迎來到避風港，這裡是旅居手冊 🎉"

        texts = [
            "歡迎旅人來到這個溫暖、可愛的小地方，這裡是以遊戲、動漫、電影為主，同時也包含非常多生活相關主題的 ACG 社群。",
            "",
            "在開始您的旅途之前，希望您可以花點時間閱讀這份手冊，手冊裡有許多重要的社群資訊與使用方式，能幫助您快速瞭解這裡。",
            "",
            "> 查看下列特點時，點擊「詳情」可引導至相關網頁，瞭解更多內容。",
        ]

        text_rule = [
            "### 📜 社群守則",
            "開始活動前，請務必先閱讀社群相關規定。社群的規定不多，大部分都是個人權益與安全宣導，希望大家都能共同維護友善社群！",
        ]

        link_button = ui.Button(label="詳情", url=url_ch_rule, emoji="🌐")
        section = ui.Section("\n".join(text_rule), accessory=link_button)

        text_channel = [
            "### 💡 頻道索引",
            "社群有非常完善的頻道與分類供大家自由使用，以及多種有趣且實用的功能，還有專門為社群編寫的 Discord Bot！"
        ]

        link_button_2 = ui.Button(label="詳情", url=url_ch_introduce_channel, emoji="🌐")
        section_2 = ui.Section("\n".join(text_channel), accessory=link_button_2)

        text_cabin = [
            "### 🏕️ 個人小屋",
            "社群擁有非常特別的共同經營模式，每位旅人都能擁有屬於自己的語音頻道，以及該頻道的所有權限。您可以自由裝飾、布置、並邀請最好的朋友加入遊玩！"
        ]

        link_button_3 = ui.Button(label="詳情", url=url_ch_cabin, emoji="🌐")
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

            "旅人剛開始會不好意思的話也沒關係，大家其實都相對慢熟，您可以先從文字聊天慢慢開始，尋找感興趣的遊戲或話題並加入。"
            "此外，社群也推薦旅人經常加入公開的語音頻道，即使不說話也沒關係，聽聽大家在聊什麼，也能增加熟悉感！",
        ]

        text_activity = [
            "### 🔥 保持活躍",

            "社群有獨特的經驗系統用於保持整體活躍，旅人可以通過發送訊息、按表情、在語音掛網等伺服器活動，或進行簽到、玩遊戲累積經驗。"
            "社群對活躍度的要求非常寬鬆，旅人無須為此感到壓力；社群很鼓勵大家低能量社交，偶爾露臉也沒問題！",
        ]

        text_introduce = [
            "### 👻 介紹自己",
            
            "旅人可以從身分組問卷選擇自己感興趣的遊戲與話題，讓大家在舉辦或參加活動時能即時提及您；您還可以套用外觀身分組來裝扮自己，讓自己擁有獨特風格。"
            "社群也推薦旅人到自我介紹寫下更多關於自己的事情，讓大家能更好地認識您！"
        ]

        thumbnail_chat = ui.Thumbnail(media="https://cdn.discordapp.com/attachments/1193049715638538283/1508799948806951023/8e52460d-0636-4298-9c30-c9676950736e.png")
        thumbnail_activity = ui.Thumbnail(media=url_cat_onfire_img)
        thumbnail_introduce = ui.Thumbnail(media=url_cat_disguise_img)

        btn_channel_camp = ui.Button(label="小火堆", url=url_ch_camp, emoji="🍂")
        btn_channel_tarvern = ui.Button(label="小酒館", url=url_ch_tarvern, emoji="🍺")

        row_chat = ui.ActionRow(btn_channel_camp, btn_channel_tarvern)

        button_attendance = ui.Button(label="每日簽到", url=url_msg_attendance, emoji="🎁")

        row_activity = ui.ActionRow(button_attendance)

        button_introduce = ui.Button(label="自我介紹", url=url_ch_introduce_self, emoji="📋")
        button_customize = ui.Button(label="身分組問卷", url=url_ch_customize, emoji="📝")
        button_additional_customize = ui.Button(label="外觀設定", url=url_msg_additional_customize, emoji="🎨")

        row_introduce = ui.ActionRow(button_customize, button_additional_customize, button_introduce)

        container_2 = ui.Container()
        container_2.add_item(ui.TextDisplay(content=title_2))
        container_2.add_item(seperetor)
        container_2.add_item(ui.Section("\n".join(text_chat), accessory=thumbnail_chat))
        container_2.add_item(row_chat)
        container_2.add_item(seperetor)
        container_2.add_item(ui.Section("\n".join(text_activity), accessory=thumbnail_activity))
        container_2.add_item(row_activity)
        container_2.add_item(seperetor)
        container_2.add_item(ui.Section("\n".join(text_introduce), accessory=thumbnail_introduce))
        container_2.add_item(row_introduce)

        self.add_item(container)
        self.add_item(container_2)

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceManualCog(bot))