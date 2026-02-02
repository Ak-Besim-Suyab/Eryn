import discord

from session.role_session import RoleSession

class RoleSettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="設定 身分組", style=discord.ButtonStyle.primary)
    async def role_setting(self, interaction: discord.Interaction, button: discord.ui.Button):
        await RoleSession().start(interaction)

    @discord.ui.button(label="設定 名片", style=discord.ButtonStyle.primary)
    async def card_setting(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("名片設定功能尚未開放，敬請期待！", ephemeral=True)