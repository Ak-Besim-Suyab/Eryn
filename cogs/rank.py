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
        super().__init__(name="排名", description="查看所有等級排名")

    @app_commands.command(name="角色", description="查看角色等級排名")
    async def rank_character(self, interaction: discord.Interaction):
        try:
            await self._send_rank(
                interaction,
                query=Character.select().order_by(Character.level.desc()).limit(5),
                title="🏆 角色等級排名",
                get_level=lambda obj: obj.level,
                get_exp=lambda obj: obj.experience
            )
        except Exception as e:
            logger.error(f"[錯誤] 查詢角色排名失敗：{e}")
            await interaction.response.send_message("❌ 查詢失敗，請稍後再試。", ephemeral=True)

    @app_commands.command(name="釣魚", description="查看釣魚等級排名")
    async def rank_fishing(self, interaction: discord.Interaction):
        try:
            await self._send_rank(
                interaction,
                query=Skill.select().where(Skill.skill_type == "fishing").order_by(Skill.level.desc()).limit(5),
                title="🎣 釣魚等級排名",
                get_level=lambda obj: obj.level,
                get_exp=lambda obj: obj.experience
            )
        except Exception as e:
            logger.error(f"[錯誤] 查詢釣魚排名失敗：{e}")
            await interaction.response.send_message("❌ 查詢失敗，請稍後再試。", ephemeral=True)

    async def _send_rank(self, interaction: discord.Interaction, query, title: str, get_level, get_exp):
        """通用排名顯示方法"""
        results = list(query)

        if not results:
            await interaction.response.send_message("尚無玩家資料", ephemeral=True)
            return

        embed = discord.Embed(title=title, color=discord.Color.gold())

        for rank, obj in enumerate(results, 1):
            member = interaction.guild.get_member(obj.player_id) if interaction.guild else None
            player_name = member.display_name if member else f"未知玩家#{obj.player_id}"

            if rank == 1:
                medal = "🥇"
            elif rank == 2:
                medal = "🥈"
            elif rank == 3:
                medal = "🥉"
            else:
                medal = f"{rank}."
            
            level = get_level(obj)
            exp = get_exp(obj)
            
            embed.add_field(
                name=f"{medal} {player_name}",
                value=f"Lv. {level} | {exp} EXP",
                inline=False
            )

        await interaction.response.send_message(embed=embed)


class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(RankGroup())


async def setup(bot):
    await bot.add_cog(Rank(bot))
