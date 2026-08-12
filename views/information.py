import discord
from discord import ui
from discord import SeparatorSpacing

from datetime import datetime, timezone

from models import Player
from models import Statistic

class Information:

    @staticmethod
    async def show(interaction: discord.Interaction):

        member = interaction.user
        player = Player.get_or_create_player(member.id)
        statistic = Statistic.get_or_create_stat(member.id)

        if not isinstance(member, discord.Member):
            return

        container = ui.Container()
        separator = ui.Separator()

        now = datetime.now(timezone.utc)
        join_times = now - member.joined_at
        join_days = join_times.days

        # 請留意這裡的日期轉換佔位符，大小寫會顯示不同的時間格式
        description = [
            f"## {member.display_name} 的護照",
            f"> - **等級 {player.level}**",
            f"> - **經驗值 {player.experience} / {player.get_required_exp(player.level)}**",
        ]

        # 處理加入時間資訊
        time_line = [
            f"### 加入時間",
            f"> - **{member.joined_at.strftime(f"於 %Y 年 %m 月 %d 日加入，總共經過 {join_days} 天**")}",
        ]

        # 處理小屋持有資訊
        house_line = [
            f"### 持有小屋",
        ]

        if not player.houses:
            house_line.append("> *尚未擁有任何小屋*")
        else:
            for house in player.houses:
                house_line.append(f"> - <#{house.id}>")

        # 處理成員統計資訊
        stat_line = [
            f"### 統計",
            f"> - **累計簽到：{statistic.total_daily_claims} 天**",
            f"> - **累計發送訊息：{statistic.total_message_send} 則**",
            f"> - **累計語音時間：{statistic.total_voice_time} 分**",
        ]

        title = ui.Section("\n".join(description), accessory=ui.Thumbnail(media=member.display_avatar.url))
        container.add_item(title)
        container.add_item(separator)
        container.add_item(ui.TextDisplay(content="\n".join(time_line)))
        container.add_item(separator)
        container.add_item(ui.TextDisplay(content="\n".join(house_line)))
        container.add_item(separator)
        container.add_item(ui.TextDisplay(content="\n".join(stat_line)))

        view = ui.LayoutView(timeout=None)
        view.add_item(container)

        await interaction.response.send_message(view=view, ephemeral=True)

# singletons declaration ---------------------------------------

_instance = Information()

show = _instance.show