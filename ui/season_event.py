import discord
import random
import time

from database.player import Player

from cores.logger import logger

class SeasonEventView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = 1.9
        self.player_timestamps = {}

        super().__init__(timeout=None)

    @discord.ui.button(label="緬懷", style=discord.ButtonStyle.primary, emoji="🕯️", custom_id="mourn")
    async def mourn(self, interaction: discord.Interaction, button: discord.ui.Button):

        now = time.time()
        if interaction.user.id in self.player_timestamps:
            elapsed = now - self.player_timestamps[interaction.user.id]
            if elapsed < self.cooldown:
                remaining = self.cooldown - elapsed
                await interaction.response.send_message(f"❌ 太頻繁地祭拜意義不大，請等待 {remaining:.1f} 秒後再試", ephemeral=True)
                return
            
        self.player_timestamps[interaction.user.id] = now

        experience = random.randint(1, 9)
        currency = random.randint(1, 9)

        Player.add_experience(interaction.user.id, experience)
        Player.add_balance(interaction.user.id, currency)

        loot_lines = [
            f"+{experience} 經驗值",
            f"+{currency} 金幣"
        ]

        embed = discord.Embed()
        embed.description = "> *你緬懷逝去的靈魂，內心得到平靜*"
        embed.color = discord.Color.dark_gold()

        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.add_field(name="獲得獎勵：", value="\n".join(loot_lines), inline=False)

        bonus_chance = 0.19
        bonus_experience = 0

        if random.random() < bonus_chance:
            bonus_experience = random.randint(9, 90)
            Player.add_balance(interaction.user.id, currency)

            lines = [
                "唔哦哦哦！",
                "> *你感受到莊嚴且神聖的力量在內心深處溢流而出*",
            ]

            embed.add_field(name="", value="\n".join(lines), inline=False)
            embed.add_field(name="獲得額外獎勵：", value=f"+{bonus_experience} Exp", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        logger.info(f"{interaction.user.display_name} 在緬懷活動中總共獲得 {experience + bonus_experience} 經驗值")

    @discord.ui.button(label="這是什麼？", style=discord.ButtonStyle.secondary, custom_id="season_event_help")
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        lines = [
            "咪，這是個糟糕版的限時活動！",
            "你可以簡單地按按鈕來獲得獎勵，並藉此緬懷我們的勇士；按鈕可以重複使用，但有短暫的冷卻時間",
        ]

        embed = discord.Embed()
        embed.title = "Elin"
        embed.description = "\n".join(lines)
        embed.color = discord.Color.gold()
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)