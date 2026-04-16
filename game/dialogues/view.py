import discord
from .color import ColorType
from .registry import dialogue_registry

class DialogueView(discord.ui.View):
    def __init__(self, dialog_name: str):
        super().__init__(timeout=None)

        self.dialogues = dialogue_registry.get(dialog_name)
        self.page = 1


    async def send(self, interaction: discord.Interaction):

        # 如果是連續對話，需要清除舊元件
        # if self.children:
        #     self.clear_items()

        page = self.dialogues.get_page(self.page)
        if page is None:
            await interaction.response.send_message("對話文本出錯，已結束對話，請聯絡管理員檢查。", ephemeral=True)
            return

        embed = discord.Embed()
        embed.title = page.title
        embed.description = page.description

        if page.color:
            embed.color = self.get_color(page.color)
        else:
            embed.color = None

        components = page.components
        if components:
            for component in components:
                button = discord.ui.Button(
                    label=component.label, 
                    emoji=component.emoji,
                    style=self.get_style(component.style), 
                )
                button.callback = self.get_callback(component.callback, button)
                self.add_item(button)

        if self.page == 1 or page.is_newtab:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, view=self)
            await interaction.response.send_message(embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    def get_callback(self, callback: str, button: discord.ui.Button) -> callable:
        async def callback_function(interaction: discord.Interaction):

            match callback:
                case "test":
                    await interaction.response.send_message("測試成功！", ephemeral=True)
                case "turn":
                    button.disabled = True
                    await interaction.response.edit_message(view=self)

                    self.page = self.page + 1
                    await self.send(interaction)
                case _:
                    await interaction.response.send_message("沒有找到對應的回呼函式，這是個錯誤嗎？請聯絡管理員檢查。", ephemeral=True)

        return callback_function


    def get_style(self, style: str) -> discord.ButtonStyle:
        """這個方法會根據字串獲取對應 discord.ButtonStyle"""
        match style:
            case "primary":
                return discord.ButtonStyle.primary
            case "secondary":
                return discord.ButtonStyle.secondary
            case "danger":
                return discord.ButtonStyle.danger
            case "link":
                return discord.ButtonStyle.link


    def get_color(self, color: str) -> discord.Color:
        """這個方法會根據字串獲取對應 discord.Color"""
        match color:
            case ColorType.GOLD:
                return discord.Color.gold()
            case ColorType.DARK_GOLD:
                return discord.Color.dark_gold()
            case ColorType.LIGHT_GREY:
                return discord.Color.light_grey()
            case ColorType.DARK_GREY:
                return discord.Color.dark_grey()
            case ColorType.DARK_THEME:
                return discord.Color.dark_theme()
"""
繼承 discord.ui.View 的目的是為了在 interaction.response.edit_message 時可以將自己傳進去

dialog = DialogueView() <- 這裡在內部將要輸出的 embed 和 view 組裝好
dialog.send() <- 替代 interaction.response.send_message 

await interaction.response.edit_message(view=self)

對話輸出有幾種方向:

:: 連續對話 - 按下按鈕或選擇後, callback 會調用 self.view 來檢查現在是哪一頁，然後翻頁輸出 self.view.send
:: 新的對話 - 按下按鈕或選擇後, callback 則是直接宣告新的 view
:: 其他 - 接上別的方法作為接口

以上輸出都應該考慮設計成能夠根據需求 edit 或 send 新的對話
"""