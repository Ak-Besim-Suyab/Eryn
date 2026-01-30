import discord

class RoleMenuView(discord.ui.View):
    def __init__(self, session):
        super().__init__(timeout=None)
        self.session = session

    @discord.ui.button(label="顏色身分組", style=discord.ButtonStyle.primary)
    async def color_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.session.render_role_option(interaction, role_tag = "color_role", category_tag = None)

    @discord.ui.button(label="圖案身分組：麥塊", style=discord.ButtonStyle.primary)
    async def pattern_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.session.render_role_option(interaction, role_tag = "icon_role", category_tag = "minecraft")

    @discord.ui.button(label="圖案身分組：最終幻想", style=discord.ButtonStyle.primary)
    async def pattern_roles_ffxiv(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.session.render_role_option(interaction, role_tag = "icon_role", category_tag = "ffxiv")