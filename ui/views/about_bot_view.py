import discord

class AboutBotView(discord.ui.View):
    def __init__(self, pages: list[discord.Embed], start_page: int = 0):
        super().__init__(timeout=None)
        self.pages = pages
        self.current_page = start_page
        self._rebuild_buttons()

    async def update_message(self, interaction: discord.Interaction):
        """更新 embed 與按鈕狀態"""
        self._rebuild_buttons()
        await interaction.response.edit_message(
            embed=self.pages[self.current_page],
            view=self
        )

    # ---------------------------------------------------------
    # 動態重建按鈕（關鍵功能）
    # ---------------------------------------------------------
    def _rebuild_buttons(self):
        """根據目前頁面決定要顯示哪些按鈕"""
        # 清除舊按鈕
        self.clear_items()

        # 第一頁「不顯示上一頁」
        if self.current_page > 0:
            self.add_item(self.PreviousButton())

        # 最後一頁「不顯示下一頁」
        if self.current_page < len(self.pages) - 1:
            self.add_item(self.NextButton())

    # ---------------------------------------------------------
    # 按鈕類別定義
    # ---------------------------------------------------------
    class PreviousButton(discord.ui.Button):
        def __init__(self):
            super().__init__(
                label="⏮ 上一頁",
                style=discord.ButtonStyle.secondary,
                custom_id="about_bot_prev"
            )

        async def callback(self, interaction: discord.Interaction):
            view: "AboutBotView" = self.view
            view.current_page -= 1
            await view.update_message(interaction)

    class NextButton(discord.ui.Button):
        def __init__(self):
            super().__init__(
                label="⏭ 下一頁",
                style=discord.ButtonStyle.primary,
                custom_id="about_bot_next"
            )

        async def callback(self, interaction: discord.Interaction):
            view: "AboutBotView" = self.view
            view.current_page += 1
            await view.update_message(interaction)
