import discord

from systems.reward_service import RewardService
from systems.stat_service import StatService


class DailyView(discord.ui.View):
    id = "daily"

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="簽到", style=discord.ButtonStyle.primary, emoji="🎁",custom_id="claim")
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await RewardService().claim(interaction)

    @discord.ui.button(label="狀態", style=discord.ButtonStyle.primary, emoji="📜", custom_id="stat")
    async def stat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await StatService().view(interaction)

    @discord.ui.button(label="排名", style=discord.ButtonStyle.primary, emoji="🏅", custom_id="leaderboard")
    async def leaderboard_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        leaderboard = interaction.client.get_cog("Leaderboard")
        if leaderboard is None:
            await interaction.response.send_message("排名功能目前無法使用，請稍後再試。", ephemeral=True)
            return
        await leaderboard.show_leaderboard(interaction)

    @discord.ui.button(label="說明", style=discord.ButtonStyle.secondary, custom_id="daily_intro")
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass