import discord
from discord import app_commands
from discord.ext import commands

from database.character import Character
from database.skill import Skill
from utils.logger import logger
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM


@app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
class RankGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="排名", description="查看各系統排行榜")

    @app_commands.command(name="角色", description="查看角色等級排行榜（前 10 名）")
    async def rank_character(self, interaction: discord.Interaction):
        try:
            await self._send_character_rank(interaction)
        except Exception as e:
            logger.error(f"[錯誤] 查詢角色排行榜失敗：{e}")
            await interaction.response.send_message("❌ 查詢失敗，請稍後再試。", ephemeral=True)

    @app_commands.command(name="釣魚", description="查看釣魚等級排行榜（前 10 名）")
    async def rank_fishing(self, interaction: discord.Interaction):
        try:
            await self._send_skill_rank(interaction, "fishing", title="🎣 釣魚等級排行榜")
        except Exception as e:
            logger.error(f"[錯誤] 查詢釣魚排行榜失敗：{e}")
            await interaction.response.send_message("❌ 查詢失敗，請稍後再試。", ephemeral=True)

    async def _send_character_rank(self, interaction: discord.Interaction):
        top_players = Character.select().order_by(Character.level.desc()).limit(10)

        if top_players.count() == 0:
            await interaction.response.send_message("尚無玩家資料", ephemeral=True)
            return

        embed = discord.Embed(title="🏆 角色等級排行榜", color=discord.Color.gold())

        for rank, character_obj in enumerate(top_players, 1):
            member = interaction.guild.get_member(character_obj.player_id) if interaction.guild else None
            player_name = member.display_name if member else f"未知玩家#{character_obj.player_id}"
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"{rank}️⃣")
            embed.add_field(name=f"{medal} {player_name}", value=f"Lv. {character_obj.level}", inline=False)

        await interaction.response.send_message(embed=embed)

    async def _send_skill_rank(self, interaction: discord.Interaction, skill_type: str, title: str):
        top_skills = (
            Skill.select()
            .where(Skill.skill_type == skill_type)
            .order_by(Skill.level.desc())
            .limit(10)
        )

        if top_skills.count() == 0:
            await interaction.response.send_message("尚無玩家資料", ephemeral=True)
            return

        embed = discord.Embed(title=title, color=discord.Color.gold())

        for rank, skill_obj in enumerate(top_skills, 1):
            member = interaction.guild.get_member(skill_obj.player_id) if interaction.guild else None
            player_name = member.display_name if member else f"未知玩家#{skill_obj.player_id}"
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"{rank}️⃣")
            embed.add_field(name=f"{medal} {player_name}", value=f"Lv. {skill_obj.level}", inline=False)

        await interaction.response.send_message(embed=embed)


class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(RankGroup())


async def setup(bot):
    await bot.add_cog(Rank(bot))
