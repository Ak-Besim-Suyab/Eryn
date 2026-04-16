import discord

from game.systems import attendance
from game.menus import StatMenu, LeaderboardMenu

class AttendanceView(discord.ui.View):
    id = "attandance"

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="簽到", style=discord.ButtonStyle.primary, emoji="🎁",custom_id="attandance_claim")
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await attendance.claim(interaction)

    @discord.ui.button(label="狀態", style=discord.ButtonStyle.primary, emoji="📜", custom_id="attandance_stat")
    async def stat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await StatMenu.show(interaction)

    @discord.ui.button(label="排名", style=discord.ButtonStyle.primary, emoji="🏅", custom_id="attandance_leaderboard")
    async def leaderboard_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await LeaderboardMenu.show(interaction)

    @discord.ui.button(label="說明", style=discord.ButtonStyle.secondary, custom_id="attandance_intro")
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass