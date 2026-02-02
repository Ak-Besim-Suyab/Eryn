import discord

class RoleMenuOption(discord.ui.Select):
    def __init__(self, session):
        self.session = session
        
        options = [
            discord.SelectOption(label="顏色身分組：花", value="color_role:flower", emoji="🎨"),
            discord.SelectOption(label="顏色身分組：漸層", value="color_role:gradient", emoji="🎨"),
            discord.SelectOption(label="圖案身分組：最終幻想", value="icon_role:ffxiv", emoji="🎨"),
            discord.SelectOption(label="圖案身分組：麥塊", value="icon_role:minecraft", emoji="🎨"),
            discord.SelectOption(label="圖案身分組：噗浪", value="icon_role:plurk", emoji="🎨"),
            discord.SelectOption(label="圖案身分組：下午茶", value="icon_role:afternoon_tea", emoji="🎨"),
        ]

        super().__init__(placeholder="請選擇身分組分類", options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        role_tag, category_tag = selected.split(":")
        await self.session.render_role_option(interaction, role_tag=role_tag, category_tag=category_tag)