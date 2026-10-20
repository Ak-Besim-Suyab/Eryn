"""
這個類別用來監聽交互事件, 主要用來替代元件持久化並處理元件互動事件

請注意: 
互動事件會先觸發全域 on_interaction 事件, 接著才去下層尋找有沒有對應的 callback
如果不慎重複註冊函式可能會導致函式重複觸發或觸發不同的函式, 設計時需要留意 
"""
import discord
from discord.ext import commands

from cores import event_bus
from data.schema.event import SelectEvent, ButtonEvent

class InteractionListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):

        if interaction.type != discord.InteractionType.component:
            return
        
        custom_id = interaction.data.get("custom_id", "")
        component_type = interaction.data.get("component_type", 0)

        # 攔截事件請求
        match component_type:
            # 按鈕事件
            case 2: 
                event = ButtonEvent(id = custom_id, interaction = interaction, custom_id = custom_id)
                await event_bus.publish(event = event, event_name = custom_id)

            # 下拉式選單事件
            case 3:
                values = interaction.data.get("values", [])
                if not values:
                    return

                event = SelectEvent(id = custom_id, interaction = interaction, values = values, custom_id = custom_id)
                await event_bus.publish(event = event, event_name = custom_id)
                
async def setup(bot: commands.Bot):
    await bot.add_cog(InteractionListener(bot))