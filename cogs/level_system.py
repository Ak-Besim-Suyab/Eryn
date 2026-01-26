import discord
from discord.ext import commands

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_level_up(self, interaction: discord.Interaction, skill_name: str, new_level: int):
        embed = discord.Embed(
            title="等級提升！",
            description=f"{skill_name}等級提升至 {new_level}！",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))