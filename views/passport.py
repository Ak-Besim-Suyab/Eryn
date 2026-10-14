import discord
from discord import ui

from datetime import datetime, timezone

from models import Player
from models import Statistic

class Passport:
    @staticmethod
    async def show(interaction: discord.Interaction, member: discord.Member = None):

        member = interaction.user if member is None else member

        player, _ = Player.get_or_create(id = member.id)
        statistic = Statistic.get_or_create_stat(member.id)

        if not isinstance(member, discord.Member):
            return

        # 取得加入時間與經過天數
        now = datetime.now(timezone.utc)
        join_times = now - member.joined_at
        join_days = join_times.days

        # 請留意這裡的日期轉換佔位符，大小寫會顯示不同的時間格式
        description = [
            f"## {member.display_name} 的護照",
            f"> - **活躍等級 {player.level}**",
            f"> - **活躍經驗值 {player.experience} / {player.get_required_exp(player.level)}**",
            f"### 加入時間",
            f"> - **{member.joined_at.strftime(f"於 %Y 年 %m 月 %d 日加入這裡，總共經過 {join_days} 天**")}",
            f"### 統計",
            f"> - **累計簽到：{statistic.total_daily_claims} 天**",
            f"> - **累計發送訊息：{statistic.total_message_send} 則**",
            f"> - **累計語音時間：{statistic.total_voice_time} 分**",
            f"### 持有小屋",
        ]

        if not player.houses:
            description.append("> *尚未擁有任何小屋*")
        else:
            for house in player.houses:
                description.append(f"> - <#{house.id}>")

        # 宣告元件
        content = ui.Section("\n".join(description), accessory=ui.Thumbnail(media=member.display_avatar.url))

        # 宣告元件容器
        container = ui.Container()
        container.accent_color = discord.Color.light_theme()
        container.add_item(content)

        # 宣告視圖
        view = ui.LayoutView()
        view.add_item(container)

        await interaction.response.send_message(view=view, ephemeral=True)

# 宣告單例 -------------

_instance = Passport()

show = _instance.show