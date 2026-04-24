import discord

from game import model

class Button(discord.ui.Button):
    def __init__(self, button: model.Button):

        self.button = button

        super().__init__(
            custom_id=button.custom_id,
            label=button.label, 
            emoji=button.emoji,
            style=BUTTON_STYLE.get(button.style, discord.ButtonStyle.primary)
        )

    async def callback(self, interaction: discord.Interaction):

        match self.button.callback:
            case "on_interaction":
                """該名稱的回呼凾式交由監聽事件處理, 這裡直接略過, 特別註明以便理解用法"""
                return
            case _:
                await interaction.response.send_message("沒有找到對應的回呼函式，這是個錯誤嗎？請聯絡管理員檢查。", ephemeral=True)

BUTTON_STYLE = {
    "primary"   : discord.ButtonStyle.primary,
    "secondary" : discord.ButtonStyle.secondary,
    "danger"    : discord.ButtonStyle.danger,
    "link"      : discord.ButtonStyle.link,
}