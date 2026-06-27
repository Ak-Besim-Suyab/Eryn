import discord
from discord.ext import commands
from discord import ui
from discord import SeparatorSpacing

class AnnounceChannelCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def announce_channel(self, ctx: commands.Context):
        await ctx.send(view=AnnounceChannelView())

class AnnounceChannelView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        img_bard_camping = ui.Thumbnail(media="https://cdn.discordapp.com/attachments/1491046495812718672/1509239237625516052/people_camping_cropped.png")
        img_port = ui.Thumbnail(media="https://cdn.discordapp.com/attachments/1491046495812718672/1509252869029892216/port_cropped.png")
        img_aquarium = ui.Thumbnail(media="https://cdn.discordapp.com/attachments/1491046495812718672/1509266166772928713/aquarium_cropped.png")
        img_street = ui.Thumbnail(media="https://cdn.discordapp.com/attachments/1491046495812718672/1509428048704045147/strees_cropped.png")
        img_coffee = ui.Thumbnail(media="https://cdn.discordapp.com/attachments/1491046495812718672/1509438153444819145/coffee_cropped.png")

        title = ui.TextDisplay(content="## 頻道索引 💡")

        content = [
            "社群有非常多實用的頻道提供大家自由使用，每個頻道都有對應的主題或使用方式，發送訊息或貼文前請記得查看頂部資訊、置頂訊息或本篇說明。"
        ]

        content_camping = [
            "### 🍁 露營區",
            "露營區是生活頻道分類，日常主題與非遊戲主題會歸類在這裡，"
            "旅人可以在這些頻道和大家聊日常，分享喜歡的事物，發送有趣的內容，或者傾訴自己的煩惱，不論任何話題都非常歡迎！",
            "",
            "- <#1192264849904898079>",
            "- <#1190027756482859042>",
            "- <#1190043435009331230>",
            "- <#1193755536265588848>",
            "- <#1192992822798860370>",
            "- <#1191867955500298250>",
            "- <#1251863209695117382>",
            "- <#1193179228452171836>",
        ] 

        content_river = [
            "### ⚓ 避風港與河道",
            "避風港是遊戲頻道分類，與遊戲有關的主題會歸類在這裡，旅人可以在這裡和大家討論或分享任何遊戲資訊；"
            "社群也有安排幾個小遊戲機器人，平常無聊的話也可以在社群裡玩小遊戲。",
            "",
            "河道則是將討論度較高的遊戲分出來做為單獨的分類，讓大家可以更方便地討論特定主題、整理與找查資料。"
            "大部分頻道都有身分組限制，想加入討論的話請務必領取身分組哦！",
            "",
            "- <#1192490635266109530>",
            "- <#1226069418170257503>",
            "- <#1190028199070023731>",
            "- <#1299374498524430467>",
            "- <#1419230462164861018>",
        ]

        content_aquarium = [
            "### 🎥 海百合劇院",
            "海百合劇院是影視頻道分類，旅人可以在這裡和大家討論喜歡或感興趣的動畫、漫畫、電影等各種形式的影視作品；除此之外，社群成員偶爾也會自發性舉辦動畫或電影的放映活動，非常歡迎大家來同樂。",
            "",
            "- <#1387744964334587994>",
            "- <#1224231424433852446>",
            "- <#1409164952723521677>",
            "- <#1251845986804961340>",
        ]

        content_street = [
            "### 🍻 海岸線旁",
            "海岸線旁是公用的語音頻道分類，旅人可以隨時隨地進來這裡，您可以在這邊掛網、邀請親朋好友進來聊天，也可以舉辦各式各樣的活動！",
            "",
            "- <#1296063137962786846>",
            "- <#1296893788148600913>",
        ]

        content_coffee = [
            "### ☕ 寧靜街道",
            "寧靜街道是特別給喜歡安靜氛圍的人準備的頻道分類，寧靜街道裡的頻道皆設定為無法打開麥克風說話，您不會被突如其來的語音打擾，"
            "非常適合旅人和小夥伴們在這裡掛網、讀書、工作和創作。",
            "",
            "- <#1223878258983047209>",
            "- <#1393199318726344704>",
        ]

        separator = ui.Separator(spacing=SeparatorSpacing.large)

        container = ui.Container()
        container.add_item(title)
        container.add_item(ui.TextDisplay(content="\n".join(content)))
        container.add_item(separator)
        container.add_item(ui.Section("\n".join(content_camping), accessory=img_bard_camping))
        container.add_item(separator)
        container.add_item(ui.Section("\n".join(content_river), accessory=img_port))
        container.add_item(separator)
        container.add_item(ui.Section("\n".join(content_aquarium), accessory=img_aquarium))
        container.add_item(separator)
        container.add_item(ui.Section("\n".join(content_street), accessory=img_street))
        container.add_item(separator)
        container.add_item(ui.Section("\n".join(content_coffee), accessory=img_coffee))

        self.add_item(container)

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceChannelCog(bot))