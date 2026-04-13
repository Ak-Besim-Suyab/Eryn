import discord, random
from collections import Counter

from cores import Action

from models import Player, Inventory, Skill
from models.region import region_manager
from models.resource import resource_manager
from models.message import message_manager
from models.data.item import item_manager

from cores.logger import logger
from utils import cooldown

class GardenSkill(Action):
    def __init__(self):
        super().__init__()

    @cooldown(seconds = 3.0)
    async def cast(self, interaction: discord.Interaction):
        pass
#         region = region_manager.get(Player.get_region(interaction.user.id))

#         # 這裡是來自不同資源的抽取集合，因此仍需要先將這些字典合併，才能順利往下執行
#         result = Counter()
#         if region.resources is None:
#             await interaction.response.send_message("❌ 由於沒有資源，使用技能得不到任何東西。", ephemeral=True)
#             return
        
#         for res in region.resources:
#             resource = resource_manager.get(res)
#             result.update(resource.roll())

#         item_value = []
#         for item_id, quantity in result.items():
#             item = item_manager.get(item_id)
#             item_value.append(f"{item.image}{item.name} x{quantity}")

#             Inventory.add_item(interaction.user.id, item_id, quantity)

#             logger.debug(f"抽取成功，總計獲得 {quantity} 個 {item_id}")

#         experience = random.randint(3, 6)
#         garden_experience = random.randint(3, 6)

#         Player.add_experience(interaction.user.id, experience)
#         Skill.add_experience(interaction.user.id, SkillType.GARDENING, garden_experience)

#         payload = {
#             "item_value": "\n".join(item_value),
#             "experience": experience,
#             "garden_experience": garden_experience,
#         }

#         embed = message_manager.create("garden", payload=payload, interaction=interaction)

#         from interface.action.view import GardenView
#         view = GardenView()

#         # 這裡印出訊息, 如果回應已經完成, 使用 followup 發送新回應
#         if interaction.response.is_done():
#             await interaction.followup.send(embed=embed, view=view)
#         else:
#             await interaction.response.send_message(embed=embed, view=view)

# garden_skill = GardenSkill()