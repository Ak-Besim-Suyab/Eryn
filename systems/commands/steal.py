import discord, random

from models import Player, Status
from models.message import message_manager
from models.type import StatusType

from .command import Command

from utils import Embed

class Steal(Command):
    def __init__(self):
        super().__init__(
            skill_cooldown = 10
        )

    @Embed.emit("steal")
    @Command.is_cooldown
    async def execute(self, interaction: discord.Interaction, member: discord.Member):

        if random.random() < 0.35:
            await interaction.response.send_message("偷竊失敗！")
            return

        if member.bot:
            await interaction.response.send_message("喵喵喵！咪沒有東西可以偷！")
            return

        if interaction.user.id == member.id:
            await interaction.response.send_message("你不能偷自己的物品！")
            return

        stole_currency = random.randint(1, 5)
        experience = random.randint(1, 5)

        Player.add_balance(interaction.user.id, stole_currency)
        Player.add_experience(interaction.user.id, experience)
        Status.add(interaction.user.id, StatusType.UNLUCKY, 1)

        item_value = [
            f"金幣 +{stole_currency}"
        ]

        experience_value = [
            f"經驗值 +{experience}"
        ]

        payload = {
            "target_name": member.display_name,
            "item_value": "\n".join(item_value),
            "experience_value": "\n".join(experience_value)
        }

        return payload