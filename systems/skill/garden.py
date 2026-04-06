import discord
import random
from collections import Counter

from cores.skill import Skill

from models.player import Player
from models.inventory import Inventory
from models.skill import Skill as skill_database
from models.type import SkillType
from models.region import region_manager
from models.resource import resource_manager

from cores.logger import logger

class GardenSkill(Skill):
    def __init__(self):
        super().__init__(
            skill_cooldown = 3
        )

    async def cast(self, interaction: discord.Interaction):

        cooling, remaining = self.is_cooldown(interaction.user.id)
        if cooling:
            await interaction.response.send_message(f"❌ 技能冷卻中，請等待 {remaining:.1f} 秒後再試。", ephemeral=True)
            return

        region = region_manager.get(Player.get_region(interaction.user.id))

        # 這裡是來自不同資源的抽取集合，因此仍需要將這些字典合併
        result = Counter()
        if region.resources is None:
            await interaction.response.send_message("❌ 由於沒有資源，使用技能得不到任何東西。", ephemeral=True)
            return
        
        for res in region.resources:
            resource = resource_manager.get(res)
            result.update(resource.roll())
    
        for item_id, quantity in result.items():
            Inventory.add_item(interaction.user.id, item_id, quantity)
            logger.debug(f"抽取成功，總計獲得 {quantity} 個 {item_id}")

        from interface.action.embed import GardenEmbed
        from interface.action.view import GardenView

        embed = GardenEmbed(interaction, result)
        view = GardenView()

        experience = random.randint(3, 6)

        Player.add_experience(interaction.user.id, experience)
        skill_database.add_experience(interaction.user.id, SkillType.GARDENING, 5)

        exp_lines = [
            f"+{experience} 經驗值",
            f"+5 園藝經驗值"
        ]

        embed.add_field(name="獲得經驗值：", value="\n".join(exp_lines), inline=False)

        file = discord.File('assets/images/skill_scoreboard.png', filename="skill_scoreboard.png")
        embed.set_image(url="attachment://skill_scoreboard.png")

        # 這裡印出訊息, 如果回應已經完成, 使用 followup 發送新回應
        if interaction.response.is_done():
            await interaction.followup.send(file=file, embed=embed, view=view)
        else:
            await interaction.response.send_message(file=file, embed=embed, view=view)

garden_skill = GardenSkill()