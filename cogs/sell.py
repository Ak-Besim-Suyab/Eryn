import discord
from discord import app_commands
from discord.ext import commands

from database.inventory import Inventory
from database.player import Player
from utils.fishing_loot import FishingLootTable
from utils.logger import logger
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM


class Sell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loot_table = FishingLootTable()

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="出售", description="出售背包內所有物品")
    async def sell_command(self, interaction: discord.Interaction):
        player_id = interaction.user.id
        
        items = Inventory.get_all_items(player_id)
        
        if not items:
            await interaction.response.send_message("❌ 背包是空的，沒有物品可以出售", ephemeral=True)
            return
        
        total_value = 0
        sold_items = []
        
        for item in items:
            fish_info = self.loot_table.get_fish_info(item.item_key)
            if fish_info:
                item_value = fish_info['base_value'] * item.quantity
                total_value += item_value
                sold_items.append(f"**{fish_info['name']}** × {item.quantity} → {item_value} 金幣")
                
                Inventory.remove_item(player_id, item.item_key, item.quantity)
        
        if total_value == 0:
            await interaction.response.send_message("❌ 沒有可出售的物品", ephemeral=True)
            return
        
        Player.increase_currency(player_id, total_value)
        
        embed = discord.Embed(
            title="💰 全部出售成功",
            description=f"你出售了背包內所有物品",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="出售清單",
            value="\n".join(sold_items),
            inline=False
        )
        embed.add_field(name="總收益", value=f"+{total_value} 金幣", inline=False)
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
        logger.info(f"[出售] {interaction.user} 出售所有物品，獲得 {total_value} 金幣")


async def setup(bot):
    await bot.add_cog(Sell(bot))
