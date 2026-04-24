"""
Controller class
"""
import discord
import asyncio
from system import registry

from data.payloads.response import BaseResponse

class Dialogue(discord.ui.View):
    def __init__(self, dialog_name: str):
        super().__init__(timeout=None)

        self.dialogues = registry.message.get(dialog_name)
        self.selected_options = {}
        self.selected_options_length = 0
        self.page = 1

    async def send(self, interaction: discord.Interaction, payloads: dict | BaseResponse = None, ephemeral: bool = False):

        # 如果是連續對話，需要清除舊元件
        # if self.children:
        #     self.clear_items()
        
        if payloads and isinstance(payloads, BaseResponse):
            payloads = payloads.to_dict()
        
        if not payloads:
            payloads = {}

        # 保存設計
        if self.page == 1 or page.is_newtab:
            if interaction.response.is_done():
                # 更新舊訊息狀態時, 訊息會被標記為 is_done, 需要改用 followup
                await interaction.followup.send(embeds=embeds, view=self, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(embeds=embeds, view=self, ephemeral=ephemeral)
        else:
            if interaction.response.is_done():
                await interaction.edit_original_response(embeds=embeds, view=self, ephemeral=ephemeral)
            else:
                await interaction.response.edit_message(embeds=embeds, view=self, ephemeral=ephemeral)
        
        if page.auto:
            self.page = self.page + 1
            if self.dialogues.get_page(self.page) is None:
                return
            
            async with interaction.channel.typing():
                await asyncio.sleep(page.auto_delay)

            await self.send(interaction=interaction, ephemeral=ephemeral)

    def get_callback(self, callback: str, component: discord.ui.Button | discord.ui.Select) -> callable:
        async def callback_function(interaction: discord.Interaction):
            match callback:
                case "turn":
                    component.disabled = True
                    await interaction.response.edit_message(view=self) # 將按鈕取消時, 需要更新舊訊息狀態

                    self.page = self.page + 1
                    await self.send(interaction)

                case "multiple_choose":
                    if isinstance(component, discord.ui.Select):
                        self.selected_options[component.custom_id] = component.values

                        await interaction.response.defer()
                    
                    if len(self.selected_options) >= self.selected_options_length:
                        await interaction.followup.send("選項已選擇完成", ephemeral=True)

        return callback_function

