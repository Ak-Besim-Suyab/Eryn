import discord
from discord.ext import commands
from discord import app_commands

import asyncio

from player_manager import player_manager
from map_manager import map_manager
from asset_manager import asset_manager

GUILD_TH_HAVEN = discord.Object(id=1193049715638538280)
GUILD_AK_BESIM = discord.Object(id=1190027756482859038)

#--- command
class Ranch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.livestock_timer = {}
        self.cost_time = 10
        self.item_list = asset_manager.get_asset("items")
        self.world_map = map_manager.world_map
        
        print('[Command] Ranch command initialized successfully.')

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="ranch", description="在這裡放養動物")
    async def ranch(self, interaction: discord.Interaction, item:str="All", amount:int=None):
        player = player_manager.get_player(interaction.user.id, interaction.user.display_name)
        now = asyncio.get_event_loop().time()

        # 把 livestock timer 存到 map 裡

        player_dict = {} # 建空 dict 用來存 timer, livestock 到 livestock_timer 裡
        player_dict["location"] = player.location # 這裡紀錄地圖位置

        # check timer
        if player.user_id in self.livestock_timer:
            print("player exsist.")
            print(self.livestock_timer)
            if now >= self.livestock_timer[player.user_id]["timer"]:
                print("your time has come!")
                for i, key in self.item_list.items():
                    print(key)
                    for livestock in self.livestock_timer[player.user_id]["livestocks"]: ###
                        print(livestock)
                        if "family" in key and key["family"] == livestock:
                            print("find livestock grown, take it back")
                            player.inventory.add_item(i, self.livestock_timer[player.user_id][livestock])

                del self.livestock_timer[player.user_id]
            else:
                print("your time not come yet.")
        else: # 沒有 time = 沒有動物在放養，執行放養
            livestock_bench = {} ###
            have_livestock = False
            for i, key in self.item_list.items():
                print(key)
                if "ranchable" in key and key["ranchable"] is True:
                    if i in player.inventory.item_list:
                        print("find ranchable item, put it into map.")
                        print(f"{map_name} {self.world_map[map_name]}")
                        self.world_map[map_name].add_livestock(player, i, 1)
                        player_dict[i] = 1
                        livestock_bench[i] = 1 ###
                        player.inventory.remove_item(i, 1)
                        have_livestock = True
                    else:
                        print("no item!")
            if not have_livestock:
                print("you dont have any livestock")
            else:
                player_dict["livestocks"] = livestock_bench ###

            print("no timer, create one.")
            player_dict["timer"] = now + self.cost_time
            print(player_dict["timer"])
            self.livestock_timer[player.user_id] = player_dict

        await interaction.response.send_message(f"放牧測試")

#--- button 
class RanchView(discord.ui.View):
    def __init__(self, author: discord.Member):
        super().__init__(timeout=None)

    @discord.ui.button(label="再次放牧", style=discord.ButtonStyle.primary)
    async def remine(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"放牧測試")

#--- load cog
async def setup(bot):
    await bot.add_cog(Ranch(bot))

# 獲取地圖，將小動物放到地圖並記錄玩家名稱、動物名稱與數量
# 增加存放時間