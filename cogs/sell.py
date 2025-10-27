import discord
from discord.ext import commands
from discord import app_commands

from asset_manager import asset_manager
# from player_manager import player_manager

GUILD_TH_HAVEN = discord.Object(id=1193049715638538280)
GUILD_AK_BESIM = discord.Object(id=1190027756482859038)

class Sell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="sell", description="賣掉有價值的物品，默認出售全部能變賣的物品")
    async def sell(self, interaction: discord.Interaction, item:str="All", amount:int=None):
        player_manager = self.bot.get_cog("PlayerManager")
        player = player_manager.get_player(interaction.user.id, interaction.user.display_name)
        items = asset_manager.get_asset("items")

        sold = 0
        if not player.inventory.item_list: # if there has any item in inventory
            for item in player.inventory.item_list:
                if items[item]["tag"] == "misc":
                    sold = player.inventory.get_item(item) * items[item]["value"]
                    player.inventory.remove_item(item, player.inventory.get_item(item))
                    #print(player.inventory.item_list[item])
                    #print(items[item]["value"])
        else:
            print("the inventory has no item")

        #player.gold += sold

        print(sold)


        # if item == "All":
        #     for mat, key in items.items():
        #         if mat in player.inventory.item_list:
        #             if key["sellable"] == True and player.inventory.item_list[mat] != 0:
        #                 sold_gold += key["base_value"] * player.inventory.item_list[mat]
        #                 player.inventory.remove_item(mat, player.inventory.item_list[mat])
        #     await interaction.response.send_message(f"💰 你出售所有可變賣的物品，獲得 **{sold_gold} 金幣**\n你現在有 **{player.gold} 金幣**")
        # else:
        #     if item in items: # 輸入的名字在存在於遊戲內
        #         if item in player.inventory.item_list: # 物品有至少 1 個在玩家背包裡
        #             if amount is None:
        #                 sold_gold += items[item]["base_value"] * player.inventory.item_list[item]
        #                 player.inventory.remove_item(item, player.inventory.item_list[item])
        #                 await interaction.response.send_message(f"💰 你出售 {amount} {items[item]["icon"]} {items[item]["display_name"]}，獲得 **{sold_gold} gold**！\n你現在共有 **{player.gold} gold**")
        #             elif amount <= player.inventory.item_list[item]: 
        #                 sold_gold += items[item]["base_value"] * amount
        #                 player.inventory.remove_item(item, amount)
        #                 await interaction.response.send_message(f"💰 你出售 {amount} {items[item]["icon"]} {items[item]["display_name"]}，獲得 **{sold_gold} gold**！\n你現在共有 **{player.gold} gold**")
        #             else:
        #                 await interaction.response.send_message(f"想出售的數量超過背包的數量")
        #         else:
        #             await interaction.response.send_message(f"背包裡沒有該物品能出售")
        #     else:
        #         await interaction.response.send_message(f"你輸入的物品並不存在於遊戲中")

        # player.add_gold(sold_gold)
        # player.save_player()
        # asset_manager.maps
        # print("[Sell] You sell your all sellable items!") 

async def setup(bot):
    await bot.add_cog(Sell(bot))

# 確認玩家背包有該物品
# 搜尋所有標籤為 sellable 的物品
# 確認 sellable 為 true 且物品數量不為零
# 將數量乘以 base_value 然後加入玩家的 gold
# 計算總共能賣多少 gold
# 更新玩家

# 如果只有 sell 的話，彈出教學介面，以及 sell all 按鈕
# sell all 賣出所有東西
# sell item amount 賣出指定物品的數量
# sell item or sell item all 賣出指定物品的所有數量