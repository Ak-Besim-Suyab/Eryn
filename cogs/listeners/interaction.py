"""
這個類別用來監聽交互事件, 主要用來替代元件持久化並處理元件互動事件

請注意: 
互動事件會先觸發全域 on_interaction 事件, 接著才去下層尋找有沒有對應的 callback
如果不慎重複註冊函式可能會導致函式重複觸發或觸發不同的函式, 設計時需要留意 
"""
import discord
from discord.ext import commands

from game.systems import attendance
from game.systems import commemorate
from game.menus import StatMenu, LeaderboardMenu

from utils.ansi import ANSI,wrap_ansi

class InteractionListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        print("interaction triggered...")

        if interaction.type != discord.InteractionType.component:
            return
        
        # 以下實作邏輯
        custom_id = interaction.data.get("custom_id", "")

        if custom_id.startswith("market:"):
            data = custom_id.split(":")
            match data[1]:
                case "buy":
                    return
                #     shop_name = "vendor"
                #     shop_data = shop_registry.get(shop_name)

                #     # error-proofing
                #     if not shop_data:
                #         await interaction.response.send_message("商店不存在", ephemeral=True)
                #         return
                    
                #     shop_list = []
                #     for item in shop_data.item_list:
                #         item_ = item_registry.get(item)
                #         ansi_item_name = ANSI(item_.name).white()
                #         ansi_item_description = ANSI(item_.description).green()
                #         ansi_item_price = ANSI(f"{item_.price}g").gold()

                #         line = f"{item_.emoji}{ansi_item_name} {ansi_item_price} - {ansi_item_description}"

                #         shop_list.append(str(line))
                    
                #     payload = {
                #         "shop_list": wrap_ansi("\n".join(shop_list))
                #     }

                #     await DialogueView(dialog_name="merchandise").send(interaction=interaction, payloads=payload)
                #     return
                # case "help":
                #     await DialogueView(dialog_name="market_help").send(interaction=interaction, ephemeral=True)
                #     return

        if custom_id.startswith("season:"):
            # 這裡預期會有 2 節資料
            data = custom_id.split(":")
            match data[1]:
                case "commemorate":
                    await commemorate.execute(interaction)
                    return
                case "offering":
                    pass
                case "help":
                    # await DialogueView(dialog_name="commemorate_help").send(interaction=interaction, ephemeral=True)
                    return

        match custom_id:
            case "attendance_claim":
                await attendance.claim(interaction)

            case "attendance_stat":
                await StatMenu.show(interaction)
            
            case "attendance_leaderboard":
                await LeaderboardMenu.show(interaction)

            case "attendance_help":
                return
                # await DialogueView(dialog_name="attendance_help").send(interaction=interaction, ephemeral=True)
                
async def setup(bot):
    await bot.add_cog(InteractionListener(bot))