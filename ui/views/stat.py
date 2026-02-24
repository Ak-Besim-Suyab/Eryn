import discord

from session.role_session import RoleSession

class StatView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label="設定身分組", style=discord.ButtonStyle.primary)
    async def set_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        await RoleSession().start(interaction)
