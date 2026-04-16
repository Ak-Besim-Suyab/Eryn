import discord
import random

from cores import Action, event_bus

from data.event import RewardEvent
from data.payload import RewardPayload
from data.type import RewardType

from utils import cooldown

class StealAction(Action):

    def __init__(self):
        super().__init__()

    @cooldown(seconds = 3.0)
    async def execute(self, interaction: discord.Interaction, member: discord.Member):

        if member.bot:
            await interaction.response.send_message("咪沒有東西可以偷！", ephemeral=True)
            return
        
        if interaction.user.id == member.id:
            await interaction.response.send_message("你沒辦法偷自己的東西。", ephemeral=True)
            return
        
        if random.random() < 0.35:
            await interaction.response.send_message("偷竊失敗！", ephemeral=True)
            return

        user_id = interaction.user.id
        user_name = interaction.user.display_name

        # target_id = member.id
        target_name = member.display_name

        reward_payload = RewardPayload(user_id=user_id)
        reward_payload.experience = random.randint(1, 5)
        reward_payload.currency = random.randint(1, 5)

        reward_event = RewardEvent(type=RewardType.LOOT, payload=reward_payload)
        await event_bus.publish(reward_event)

        newline = "\n"
        description = [
            f"> *你將無形的手伸向{target_name}...*",
            f"> *{target_name}覺得身上的東西似乎被偷走了...*"
        ]

        embed = discord.Embed()
        embed.description = newline.join(description)
        embed.color = discord.Color.gold()

        embed.add_field(name="獲得經驗值：", value=f"經驗值 +{reward_payload.experience}", inline=False)
        embed.add_field(name="獲得金幣：", value=f"金幣 +{reward_payload.currency}", inline=False)
        embed.set_author(name = user_name, icon_url = interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

# ------------------------------
# 創建實例
# 父類有帶 timestamps 的字典用於紀錄各個玩家的上次行為時間，因此需要單例來保存狀態

_instance = StealAction()
execute = _instance.execute