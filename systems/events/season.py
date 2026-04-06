import discord
import random
import time

from cores.skill import Skill

from models.player import Player
from models.inventory import Inventory
from models.data.item import item_manager
from cores.logger import logger

class SeasonEvent(Skill):
    def __init__(self):
        super().__init__(
            skill_cooldown = 3
        )

        self.max_consume = 10
        self.offers = [
            "apple",
            "grape",
            "rose_red",
            "rose_white",
            "rose_yellow",
        ]

    async def mourn(self, interaction: discord.Interaction):

        cooling, remaining = self.is_cooldown(interaction.user.id)
        if cooling:
            await interaction.response.send_message(f"❌ 太頻繁地祭拜意義不大，請等待 {remaining:.1f} 秒後再試", ephemeral=True)
            return
        
        experience = random.randint(1, 9)
        currency = random.randint(1, 9)

        Player.add_experience(interaction.user.id, experience)
        Player.add_balance(interaction.user.id, currency)

        loot_lines = [
            f"+{experience} 經驗值",
            f"+{currency} 金幣"
        ]

        embed = discord.Embed()
        embed.description = "> *你緬懷逝去的靈魂，內心得到平靜*"
        embed.color = discord.Color.dark_gold()

        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.add_field(name="獲得獎勵：", value="\n".join(loot_lines), inline=False)

        bonus_chance = 0.19
        bonus_experience = 0

        if random.random() < bonus_chance:
            bonus_experience = random.randint(9, 90)
            Player.add_experience(interaction.user.id, bonus_experience)

            lines = [
                "唔哦哦哦！",
                "> *你感受到莊嚴且神聖的力量在內心深處溢流而出*",
            ]

            embed.add_field(name="", value="\n".join(lines), inline=False)
            embed.add_field(name="獲得額外獎勵：", value=f"+{bonus_experience} 經驗值", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        logger.info(f"{interaction.user.display_name} 在緬懷活動中總共獲得 {experience + bonus_experience} 經驗值")

    async def pre_offer(self, interaction: discord.Interaction):
        # 輸出預期
        # 你有以下物品可以供奉：
        # 每次供奉最多消耗 10 個
        # 要供奉嗎？
        
        lines = []
        for offer in self.offers:
            item = item_manager.get(offer)
            if item is not None:
                inventory_item = Inventory.get_item(interaction.user.id, offer)
                if inventory_item is not None and inventory_item.quantity > 0:
                    lines.append(f"{item.image}{item.name} x{inventory_item.quantity}")
        
        if not lines:
            await interaction.response.send_message("❌ 你目前沒有任何可以供奉的物品", ephemeral=True)
            return

        descriptions = [
            "你有以下物品可以供奉，每次最多會消耗 10 個。",
            "要供奉嗎？",
        ]
        
        embed = discord.Embed()
        embed.description = "\n".join(descriptions)
        embed.color = discord.Color.gold()

        embed.add_field(name="可以供奉的物品：", value="\n".join(lines), inline=False)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        from interface.season_event import PreOfferView
        view = PreOfferView()
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


    async def offer(self, interaction: discord.Interaction):
        
        lines = []
        total_experience = 0

        for offer in self.offers:
            item = item_manager.get(offer)
            if item is not None:
                inventory_item = Inventory.get_item(interaction.user.id, offer)
                if inventory_item is not None and inventory_item.quantity > 0:
                    consume = min(inventory_item.quantity, self.max_consume)
                
                    result = Inventory.remove_item(interaction.user.id, offer, consume)
                    if result:
                        lines.append(f"{item.image}{item.name} -{consume}")

                        experience = random.randint(1, 9) * consume
                        Player.add_experience(interaction.user.id, experience)
                        total_experience += experience
        
        if not lines:
            await interaction.response.send_message("❌ 你目前任何沒有可以供奉的物品", ephemeral=True)
            return
        
        embed = discord.Embed()
        embed.description = "> 你為已故的亡魂哀悼，鮮花與供品在陣陣微光中消逝。"
        embed.color = discord.Color.gold()

        embed.add_field(name="供奉物品：", value="\n".join(lines), inline=False)
        embed.add_field(name="獲得獎勵：", value=f"+{total_experience} 經驗值", inline=False)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


season_event = SeasonEvent()