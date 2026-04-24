import discord

from system import registry
from game import model
from game import ui

class Context:
    """
    該類別為負責連結連續指令與元件的上下文容器，命名來源於 discord.py 傳統文字指令傳入的參數。

    .. `message_id`: 訊息提取
    .. `page`: 連續對話的文本頁數，用於控制文本輸出的順序。
    """
    def __init__(self, message_name: str):
        self.message_name = message_name
        self.messages = registry.message.get(message_name)
        self.page = 1

    async def send(self, interaction: discord.Interaction):
        """
        最主要的訊息輸出函式。
        """
        page = self.messages.get_page(self.page)
        if page is None:
            await interaction.response.send_message("對話文本似乎有誤，已結束對話，請聯絡管理員檢查。", ephemeral=True)
            return

        embeds = await self._create_embeds(page.embeds) if page.embeds else []
        
        view = ui.View(page.view, self)

        await interaction.response.send_message(embeds=embeds, view=view, ephemeral=page.ephemeral)

    async def _create_embeds(self, embeds: list[model.Embed]):
        """將訊息元件中的 Embed 轉換為 ui.Embed"""
        _embeds = []
        for embed in embeds:
            _embed = ui.Embed(embed)
            _embeds.append(_embed)
        return _embeds

    #     if self.page == 1 or page.is_newtab:
    #         if interaction.response.is_done():
    #             # 更新舊訊息狀態時, 訊息會被標記為 is_done, 需要改用 followup
    #             await interaction.followup.send(embeds=embeds, view=self, ephemeral=ephemeral)
    #         else:
    #             await interaction.response.send_message(embeds=embeds, view=self, ephemeral=ephemeral)
    #     else:
    #         if interaction.response.is_done():
    #             await interaction.edit_original_response(embeds=embeds, view=self, ephemeral=ephemeral)
    #         else:
    #             await interaction.response.edit_message(embeds=embeds, view=self, ephemeral=ephemeral)
        
    #     if page.auto:
    #         self.page = self.page + 1
    #         if self.dialogues.get_page(self.page) is None:
    #             return
            
    #         async with interaction.channel.typing():
    #             await asyncio.sleep(page.auto_delay)

    #         await self.send(interaction=interaction, ephemeral=ephemeral)

    # def get_callback(self, callback: str, component: discord.ui.Button | discord.ui.Select) -> callable:
    #     async def callback_function(interaction: discord.Interaction):
    #         match callback:
    #             case "turn":
    #                 component.disabled = True
    #                 await interaction.response.edit_message(view=self) # 將按鈕取消時, 需要更新舊訊息狀態

    #                 self.page = self.page + 1
    #                 await self.send(interaction)

    #     return callback_function