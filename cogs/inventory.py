import json
import discord
from discord import app_commands
from discord.ext import commands

from database.inventory import Inventory
from database.player import Player
from database.skill import Skill
from database.character import Character
from utils.embed_builder import EmbedBuilder
from utils.logger import logger
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM, Context


def build_inventory_embed(user: discord.abc.User) -> discord.Embed:
    """建立背包嵌入訊息。"""
    player = Player.get_or_create_player(user.id)
    items = Inventory.get_all_items(user.id)
    fishing_progress = Skill.get_progress(user.id, 'fishing')
    character_progress = Character.get_progress(user.id)
    
    item_manager = Context.get_manager("item")

    embed = discord.Embed(
        title=f"🎒 {user.display_name} 的背包",
        color=discord.Color.green()
    )

    embed.add_field(name="💰 金幣", value=f"{player.currency} 枚", inline=False)
    levels_value = [
        f"角色：Lv.{character_progress['level']} ({character_progress['current_exp']}/{character_progress['required_exp']} EXP)",
        f"釣魚：Lv.{fishing_progress['level']} ({fishing_progress['current_exp']}/{fishing_progress['required_exp']} EXP)"
    ]
    embed.add_field(name="🏅 等級", value="\n".join(levels_value), inline=False)

    if items:
        items_text = []
        for item in items:
            item_obj = item_manager.get_item(item.item_id)
            if item_obj and 'item' in item_obj.get("tags", []):
                text = f"**{item_obj.get('display_name', item.item_id)}** × {item.quantity}"
                items_text.append(text)

        if items_text:
            embed.add_field(
                name="📦 持有物品",
                value="\n".join(items_text),
                inline=False
            )
        else:
            embed.add_field(name="📦 持有物品", value="空空如也", inline=False)
    else:
        embed.add_field(name="📦 持有物品", value="空空如也", inline=False)

    embed.set_thumbnail(url=user.display_avatar.url)

    return embed


class InventoryActionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="行動", style=discord.ButtonStyle.primary)
    async def action(self, interaction: discord.Interaction, button: discord.ui.Button):
        prompt = discord.Embed(
            title="🤔 想做什麼？",
            description="選擇一個行動",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(
            embed=prompt,
            view=InventoryActionPromptView()
        )


class InventoryActionPromptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="釣魚", style=discord.ButtonStyle.primary)
    async def go_fish(self, interaction: discord.Interaction, button: discord.ui.Button):
        from engines.fishing_engine import FishingEngine

        engine = FishingEngine()
        payload = engine.cast(interaction)

        if not payload:
            await interaction.response.edit_message(
                content="你什麼都沒釣到...",
                embed=None,
                view=None
            )
            return

        item_manager = Context.get_manager("item")
        lines = []
        
        for item in payload:
            item_obj = item_manager.get_item(item["item_id"])
            item_name = item_obj.get("display_name") if item_obj else item["item_id"]
            lines.append(f"**{item_name}**× {item['quantity']}")

        embed = discord.Embed(
            title="你釣到...",
            description="\n".join(lines),
            color=discord.Color.blue()
        )

        fishing_view = Context.get_manager("view").create("fishing_view")
        await interaction.response.edit_message(embed=embed, view=fishing_view)

    @discord.ui.button(label="返回", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = build_inventory_embed(interaction.user)
        await interaction.response.edit_message(
            embed=embed,
            view=InventoryActionView()
        )


class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="背包", description="查看你的背包與金幣")
    async def inventory_command(self, interaction: discord.Interaction):
        embed = build_inventory_embed(interaction.user)
        view = InventoryActionView()
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(InventoryCog(bot))
