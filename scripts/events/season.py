# import discord
# import random


# from models.player import Player
# from models.inventory import Inventory
# from models.data.item import item_manager
# from cores.logger import logger

# class SeasonEvent(Command):
#     def __init__(self):
#         super().__init__(
#             skill_cooldown = 2
#         )

#         self.max_consume = 10
#         self.offers = [
#             "apple",
#             "grape",
#             "rose_red",
#             "rose_white",
#             "rose_yellow",
#         ]

#     async def pre_offer(self, interaction: discord.Interaction):
#         # 輸出預期
#         # 你有以下物品可以供奉：
#         # 每次供奉最多消耗 10 個
#         # 要供奉嗎？
        
#         lines = []
#         for offer in self.offers:
#             item = item_manager.get(offer)
#             if item is not None:
#                 inventory_item = Inventory.get_item(interaction.user.id, offer)
#                 if inventory_item is not None and inventory_item.quantity > 0:
#                     lines.append(f"{item.image}{item.name} x{inventory_item.quantity}")
        
#         if not lines:
#             await interaction.response.send_message("❌ 你目前沒有任何可以供奉的物品", ephemeral=True)
#             return

#         descriptions = [
#             "你有以下物品可以供奉，每次最多會消耗 10 個。",
#             "要供奉嗎？",
#         ]
        
#         embed = discord.Embed()
#         embed.description = "\n".join(descriptions)
#         embed.color = discord.Color.gold()

#         embed.add_field(name="可以供奉的物品：", value="\n".join(lines), inline=False)
#         embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

#         from interface.season_event import PreOfferView
#         view = PreOfferView()
        
#         await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


#     async def offer(self, interaction: discord.Interaction):
        
#         lines = []
#         total_experience = 0

#         for offer in self.offers:
#             item = item_manager.get(offer)
#             if item is not None:
#                 inventory_item = Inventory.get_item(interaction.user.id, offer)
#                 if inventory_item is not None and inventory_item.quantity > 0:
#                     consume = min(inventory_item.quantity, self.max_consume)
                
#                     result = Inventory.remove_item(interaction.user.id, offer, consume)
#                     if result:
#                         lines.append(f"{item.image}{item.name} -{consume}")

#                         experience = random.randint(1, 9) * consume
#                         Player.add_experience(interaction.user.id, experience)
#                         total_experience += experience
        
#         if not lines:
#             await interaction.response.send_message("❌ 你目前任何沒有可以供奉的物品", ephemeral=True)
#             return
        
#         embed = discord.Embed()
#         embed.description = "> 你為已故的亡魂哀悼，鮮花與供品在陣陣微光中消逝。"
#         embed.color = discord.Color.gold()

#         embed.add_field(name="供奉物品：", value="\n".join(lines), inline=False)
#         embed.add_field(name="獲得獎勵：", value=f"+{total_experience} 經驗值", inline=False)
#         embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        
#         await interaction.response.send_message(embed=embed, ephemeral=True)


# season_event = SeasonEvent()