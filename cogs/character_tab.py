import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime, timezone

from lib import player, region

from ui.button import RESOURCE_BUTTON

class CharacterTabCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="角色卡", description="查看角色卡，角色卡包含旅人的各項遊戲資訊與紀錄")
    async def character_tab(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=CharacterTabView(interaction), ephemeral=True)
        
    # 角色卡按鈕的元件事件監聽
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):

        # 檢查互動類型是否為元件，並確認有資料存在
        if interaction.type != discord.InteractionType.component or interaction.data is None:
            return

        # 檢查元件類型是否為 button
        if interaction.data.get("component_type") != 2:
            return
        
        # 檢查按鈕 custom_id 是否為 character_tab
        if interaction.data.get("custom_id") == "character_tab":
            await interaction.response.send_message(view=CharacterTabView(interaction), ephemeral=True)

class CharacterTabView(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)

        # 添加角色區塊
        container = discord.ui.Container()
        container.add_item(character_section(interaction.user))

        self.add_item(container)

        # 添加按鈕
        self.add_item(discord.ui.ActionRow(RESOURCE_BUTTON))

def character_section(member: discord.Member) -> discord.ui.Section:

    if not isinstance(member, discord.Member):
        raise ValueError("member must be a discord.Member")
    
    # 取得玩家資料
    p = player.get(member.id)
    s = player.get_statistic(member.id)

    player_name       = member.display_name
    player_level      = p.level
    player_experience = round(p.experience, 1)
    player_region     = region.get_name(p.region)
    player_turn       = p.turn

    # 取得加入時間與經過天數
    now        = datetime.now(timezone.utc)
    join_times = now - member.joined_at
    join_at    = member.joined_at.strftime(f'於 %Y 年 %m 月 %d 日加入這裡，已經過 **{join_times.days:,}** 天')

    # 取得統計
    total_daily   = s.total_daily
    total_message = s.total_message
    total_voice   = s.total_voice

    # 取得小屋
    houses = []
    if not p.houses:
        houses.append("> *尚未擁有任何小屋*")
    else:
        for house in p.houses:
            houses.append(f"- <#{house.id}>")

    tabs = "\n".join(
        [
            "## 角色卡",
            f"- 名稱：**{player_name}**",
            f"- 等級：**{player_level:,}**",
            f"- 經驗值：**{player_experience:,} / {player.get_experience_requirement(player_level):,}**",
            f"- 位置：**{player_region}**",
            f"- 回合數：**{player_turn:,}**",
            "### 加入時間",
            f"- {join_at}",
            "### 統計",
            f"- 累計簽到：**{total_daily:,}** 天",
            f"- 累計發送訊息：**{total_message:,}** 則",
            f"- 累計語音時間：**{total_voice:,}** 分鐘",
            "### 持有小屋",
            "\n".join(houses),
        ]
    )

    section = discord.ui.Section(tabs, accessory=discord.ui.Thumbnail(media=member.avatar.url))

    return section

async def setup(bot: commands.Bot):
    await bot.add_cog(CharacterTabCog(bot))