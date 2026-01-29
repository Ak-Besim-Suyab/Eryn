import discord

class RoleMenuView(discord.ui.View):
    def __init__(self, session):
        super().__init__(timeout=None)
        self.session = session

    @discord.ui.button(label="顏色身分組", style=discord.ButtonStyle.primary)
    async def color_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.session.render_role("color_role", interaction)

    @discord.ui.button(label="圖案身分組", style=discord.ButtonStyle.primary)
    async def pattern_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.session.render_role("icon_role", interaction)