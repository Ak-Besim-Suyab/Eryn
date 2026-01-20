import discord
from discord import app_commands
from discord.ext import commands

from database.inventory import Inventory
from database.player import Player
from database.skill import Skill
from utils.fishing_loot import FishingLootTable
from utils.logger import logger
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM


class FishingView(discord.ui.View):
    def __init__(self, loot_table: FishingLootTable):
        super().__init__(timeout=None)
        self.loot_table = loot_table

    @discord.ui.button(label="再釣一次", style=discord.ButtonStyle.primary, emoji="🎣")
    async def fish_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        player_id = interaction.user.id
        
        fish = self.loot_table.roll()
        
        if not fish:
            await interaction.response.send_message("❌ 釣魚系統錯誤（無可用魚種）", ephemeral=True)
            return
        
        new_quantity = Inventory.add_item(player_id, fish['item_key'], 1)
        skill_result = Skill.add_experience(player_id, fish['experience'], 'fishing')
        
        embed = discord.Embed(
            title="🎣 釣魚結果",
            description=f"你釣到了 **{fish['name']}**！",
            color=discord.Color.blue()
        )
        embed.add_field(name="獲得經驗", value=f"+{fish['experience']} EXP", inline=True)
        embed.add_field(name="背包數量", value=f"{new_quantity} 條", inline=True)
        embed.add_field(name="售價", value=f"{fish['value']} 金幣/條", inline=True)
        
        if skill_result['leveled_up']:
            embed.add_field(
                name="🎉 釣魚等級提升",
                value=f"升級到 Lv.{skill_result['level']}！",
                inline=False
            )
            logger.info(f"[釣魚] {interaction.user} 釣魚等級升到 Lv.{skill_result['level']}")
        
        embed.set_footer(text=f"目前釣魚等級：Lv.{skill_result['level']}")
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed, view=FishingView(self.loot_table))
        logger.debug(f"[釣魚] {interaction.user} 釣到 {fish['name']}，獲得 {fish['experience']} 經驗")

    @discord.ui.button(label="返回", style=discord.ButtonStyle.secondary, emoji="🔙")
    async def back_to_inventory(self, interaction: discord.Interaction, button: discord.ui.Button):
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
        
        await interaction.response.send_message(embed=embed, view=FishingView(self.loot_table))


class Fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loot_table = FishingLootTable()

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="釣魚", description="開始釣魚！")
    async def fishing_command(self, interaction: discord.Interaction):
        player_id = interaction.user.id
        
        fish = self.loot_table.roll()
        
        if not fish:
            await interaction.response.send_message("❌ 釣魚系統錯誤（無可用魚種）", ephemeral=True)
            return
        
        new_quantity = Inventory.add_item(player_id, fish['item_key'], 1)
        skill_result = Skill.add_experience(player_id, fish['experience'], 'fishing')
        
        embed = discord.Embed(
            title="🎣 釣魚結果",
            description=f"你釣到了 **{fish['name']}**！",
            color=discord.Color.blue()
        )
        embed.add_field(name="獲得經驗", value=f"+{fish['experience']} EXP", inline=True)
        embed.add_field(name="背包數量", value=f"{new_quantity} 條", inline=True)
        embed.add_field(name="售價", value=f"{fish['value']} 金幣/條", inline=True)
        
        if skill_result['leveled_up']:
            embed.add_field(
                name="🎉 釣魚等級提升",
                value=f"升級到 Lv.{skill_result['level']}！",
                inline=False
            )
            logger.info(f"[釣魚] {interaction.user} 釣魚等級升到 Lv.{skill_result['level']}")
        
        embed.set_footer(text=f"目前釣魚等級：Lv.{skill_result['level']}")
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed, view=FishingView(self.loot_table))
        logger.info(f"[釣魚] {interaction.user} 釣到 {fish['name']}，獲得 {fish['experience']} 經驗")


async def setup(bot):
    await bot.add_cog(Fishing(bot))
