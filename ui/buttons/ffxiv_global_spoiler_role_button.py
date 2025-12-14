import discord
import asyncio

from utils.embed_builder import EmbedBuilder

class FFXIVGlobalSpoilerRoleButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "FFXIV 暴雷頻道許可（國際服）",
            emoji = "📦",
            style = discord.ButtonStyle.secondary,
            custom_id = "ffxiv_global_spoiler_role"
        )

    async def callback(self, interaction: discord.Interaction):

        role = interaction.guild.get_role(1235097809816916038)

        member = interaction.user
        await member.add_roles(role)

        if role in member.roles:
            await member.remove_roles(role, reason="身分組切換按鈕")
            await interaction.response.send_message(
                f"🗑️已替您移除 {role.mention} 身分組！",
                allowed_mentions=discord.AllowedMentions(roles=False),
                ephemeral=True
            )
        else:
            # 沒有 → 新增
            await member.add_roles(role, reason="身分組切換按鈕")
            await interaction.response.send_message(
                f"🎉已替您領取 {role.mention} 身分組！",
                allowed_mentions=discord.AllowedMentions(roles=False),
                ephemeral=True
            )