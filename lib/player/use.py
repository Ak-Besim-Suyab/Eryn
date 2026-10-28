import discord
from data.schema import Item

async def use(interaction: discord.Interaction, item: Item):
    print(f"成員 {interaction.user.display_name} 使用 {item.name}") # 測試回函, 實作後刪除
    await interaction.response.send_message(f"成員 {interaction.user.display_name} 使用 {item.name}") # 測試回函, 實作後刪除