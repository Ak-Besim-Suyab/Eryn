import discord

from systems.reward_service import RewardService
from systems.stat_service import StatService

class DailyEmbed(discord.Embed):
    def __init__(self):
        super().__init__()

        description = [
            "咪！旅人可以在每天 12 點過後，點擊下方的按鈕進行簽到！",
            "",
            "> 點擊「狀態」可以查看個人狀態",
            "> 點擊「排名」可以查看等級與經驗值排名",
        ]

        self.title = "每日簽到"
        self.description = "\n".join(description)
        self.color = discord.Color.gold()


class DailyView(discord.ui.View):
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

    @discord.ui.button(label="這是什麼？", style=discord.ButtonStyle.secondary, custom_id="daily_reward_help")
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        lines = [
            "咪，這裡是社群的每日簽到處！",
            "以下是關於這個簽到處的常見 Q&A：",
        ]

        embed = discord.Embed(
            title="Elin",
            description="\n".join(lines),
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=interaction.client.user.avatar.url)

        embed.add_field(
            name="Q：簽到可以幹嘛？",
            value="A：社群使用經驗值機制代表成員的活躍度，旅人可以透過發送訊息或待在語音頻道裡累積經驗值。為了照顧到不好在這裡意思活動，可能會經常潛水的旅人，簽到也能在某種程度上幫助旅人累積經驗值",
            inline=False
        )

        embed.add_field(
            name="Q：不簽到會怎麼樣嗎？",
            value="A：基於上述提到的等級機制，現在社群清理不活躍的成員時將會以此為參考。由於條件很寬鬆，基本上旅人只要偶爾有發送訊息或待在語音頻道裡，不進行簽到也能輕鬆滿足活躍條件",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)