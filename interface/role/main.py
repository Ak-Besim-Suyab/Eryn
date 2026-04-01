import discord

from interface.role.image import RoleImage
from interface.role.category import RoleCategoryEmbed, RoleCategoryView

class RoleEmbed(discord.Embed):
    def __init__(self):
        super().__init__()

        description = [
            "> *你推開厚實的橡木大門，獵犬、鷹隼與雄獅的浮雕高掛在牆上。*",
            "> *直達天花板的深色書架佇立於兩側，塞滿古老的羊皮紙與陳舊書籍。*",
            "> *這裡很安靜，只有羽毛筆的書寫聲與墨水的乾燥香氣。*",
        ]

        field_lines = [
            "- 身分組（底色）",
            "- 身分組（徽記）",
        ]

        self.title = "紋章院"
        self.description = "\n".join(description)
        self.color = discord.Color.gold()

        self.add_field(name="選擇以下分類進行操作：", value="\n".join(field_lines), inline=False)


class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(RoleOption())


class RoleOption(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label="身分組（底色）", value="tinctures", emoji="🏷️"),
            discord.SelectOption(label="身分組（徽記）", value="charges", emoji="🏷️"),
        ]

        super().__init__(
            placeholder="請選擇分類", 
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        category = self.values[0]
        
        image = RoleImage()
        embed = RoleCategoryEmbed(interaction, category)
        view = RoleCategoryView(interaction, category)
        
        await interaction.response.send_message(embeds=[image, embed], view=view, ephemeral=True)