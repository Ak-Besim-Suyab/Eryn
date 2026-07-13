"""
這個類別用來監聽交互事件, 主要用來替代元件持久化並處理元件互動事件

請注意: 
互動事件會先觸發全域 on_interaction 事件, 接著才去下層尋找有沒有對應的 callback
如果不慎重複註冊函式可能會導致函式重複觸發或觸發不同的函式, 設計時需要留意 
"""
import discord
from discord.ext import commands

from game.systems import attendance
from game.menus import StatMenu, LeaderboardMenu
from game import guide


class InteractionListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):

        if interaction.type != discord.InteractionType.component:
            return
        
        custom_id = interaction.data.get("custom_id", "")
        
        if custom_id.startswith("attendance:"):
            data = custom_id.split(":")
            match data[1]:
                case "claim":
                    await attendance.claim(interaction)
                    return
                case "stat":
                    await StatMenu.show(interaction)
                    return
                case "leaderboard":
                    await LeaderboardMenu.show(interaction)
                    return
        
        if custom_id.startswith("guide:"):
            data = custom_id.split(":")
            match data[1]:
                case "attendance":
                    await guide.attendance(interaction)
                    return

                
async def setup(bot):
    await bot.add_cog(InteractionListener(bot))