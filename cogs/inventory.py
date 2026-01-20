import discord
from discord import app_commands
from discord.ext import commands

from database.inventory import Inventory
from database.player import Player
from database.skill import Skill
from utils.fishing_loot import FishingLootTable
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM


class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loot_table = FishingLootTable()

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="背包", description="查看你的背包與金幣")
    async def inventory_command(self, interaction: discord.Interaction):
        player_id = interaction.user.id
        
        player = Player.get_or_create_player(player_id)
        items = Inventory.get_all_items(player_id)
        fishing_progress = Skill.get_progress(player_id, 'fishing')
        
        embed = discord.Embed(
            title=f"🎒 {interaction.user.display_name} 的背包",
            color=discord.Color.green()
        )
        
        embed.add_field(name="💰 金幣", value=f"{player.currency_yab} 枚", inline=False)
        
        embed.add_field(
            name="🎣 釣魚等級",
            value=f"Lv.{fishing_progress['level']} ({fishing_progress['current_exp']}/{fishing_progress['required_exp']} EXP)",
            inline=False
        )
        
        if items:
            items_text = []
            for item in items:
                fish_info = self.loot_table.get_fish_info(item.item_key)
                if fish_info:
                    name = fish_info['name']
                    value = fish_info['base_value']
                    items_text.append(f"**{name}** × {item.quantity} (售價 {value}/條)")
                else:
                    items_text.append(f"**{item.item_key}** × {item.quantity}")
            
            embed.add_field(
                name="📦 持有物品",
                value="\n".join(items_text),
                inline=False
            )
        else:
            embed.add_field(name="📦 持有物品", value="空空如也", inline=False)
        
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
        embed.set_footer(text="使用 /釣魚 來釣魚 | /出售 出售所有物品")
        
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(InventoryCog(bot))
