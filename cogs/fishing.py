import discord
from discord.ext import commands
from discord import app_commands

from data.enums import Outcome

from lib import item
from lib.util import dice
from lib import player, region
from lib.system import reward

from ui.button import INVENTORY_BUTTON

fishing_messages = {
    Outcome.CRITICAL_SUCCESS : "釣到了很多魚！",
    Outcome.SUCCESS          : "釣到了不少魚！",
    Outcome.FAILURE          : "什麼都沒釣到。",
    Outcome.CRITICAL_FAILURE : "什麼都沒釣到，甚至不小心睡著了。",
}

class FishingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="釣魚", description="於所在地點釣魚")
    async def fishing(self, interaction: discord.Interaction):
        result = dice.roll(20)
        await interaction.response.send_message(view=FishingResultView(interaction, result))

class FishingResultView(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction, result: dice.RollResult):
        super().__init__(timeout=None)

        self.interaction = interaction
        self.result = result
        self.render()

    def update(self, interaction: discord.Interaction, result: dice.RollResult):
        """更新互動資料與擲骰結果，並重新渲染介面"""
        self.interaction = interaction
        self.result = result
        self.render()

    def render(self):
        container = discord.ui.Container()

        accessory = discord.ui.Button(
            label=self.result.total, 
            style=discord.ButtonStyle.secondary, 
            emoji="🎲"
        )

        container.add_item(discord.ui.TextDisplay(content=f"**{self.interaction.user.display_name}**"))
        container.add_item(discord.ui.Section(f"你嘗試釣魚... 經過一段時間後，{fishing_messages[self.result.outcome]}", accessory=accessory))

        if self.result.is_success():
            items = roll_item(self.interaction)
            if items:
                container.add_item(discord.ui.Separator())
                container.add_item(discord.ui.TextDisplay(content="-# 獲得物品\n" + "\n".join(items)))

        self.clear_items()
        self.add_item(container)
        self.add_item(discord.ui.ActionRow(FishingButton(label="繼續釣（難度 5）"), INVENTORY_BUTTON))
    
    def dice_info(self):
        # NOTE: 顯示擲骰的詳細資訊，但暫時不考慮實作
        pass

class FishingButton(discord.ui.Button):
    def __init__(
        self,
        label: str = "釣魚",
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
    ):
        super().__init__(
            label=label,
            style=style,
        )

    async def callback(self, interaction: discord.Interaction):
        result = dice.roll(20, 5)

        # 同一個使用者觸發時編輯原訊息，不同使用者時發送新訊息
        if isinstance(self.view, FishingResultView) and interaction.user.id == self.view.interaction.user.id:
            await interaction.response.edit_message(view=FishingResultView(interaction, result))
        else:
            await interaction.response.send_message(view=FishingResultView(interaction, result))

def roll_item(interaction: discord.Interaction):

    # 取得戰利品表
    loot_table = region.get_loot_table(player.get_region(interaction.user.id), "fishing")
    if loot_table is None:
        raise ValueError("Fishing | Loot table not found.")
    
    loots = loot_table.roll()

    items = []
    for (item_type, item_id), quantity in loots.items():
        reward.give(interaction.user.id, item_type, item_id, quantity)
        items.append(f"{item.fmtstr_short(item_id, quantity)}")

    return items

async def setup(bot: commands.Bot):
    await bot.add_cog(FishingCog(bot))