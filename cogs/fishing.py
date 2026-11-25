import discord
from discord.ext import commands
from discord import app_commands

from data.enums import Outcome

from lib import item
from lib.util import dice
from lib import player, region
from lib.system import reward

class FishingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="釣魚", description="於所在地點釣魚")
    async def fishing(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=FishingView(interaction))

class FishingView(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()

        player_name = interaction.user.display_name

        result, outcome, items = self.roll(interaction)

        if outcome == Outcome.CRITICAL_FAILURE:
            message = f"什麼都沒釣到，甚至不小心睡著了。（{result}）"
        elif outcome == Outcome.FAILURE:
            message = f"什麼都沒釣到。（{result}）"
        else:
            message = f"成功釣到魚了！（{result}）"

        c = discord.ui.Container()
        c.add_item(discord.ui.TextDisplay(content=f"### {player_name}"))
        c.add_item(discord.ui.TextDisplay(content=f"你在附近的水域嘗試釣魚... 經過一段時間後，{message}"))

        if outcome == Outcome.SUCCESS or outcome == Outcome.CRITICAL_SUCCESS:

            content = [
                f"你獲得了：",
                f"{items}"
            ]

            c.add_item(discord.ui.TextDisplay(content="\n".join(content)))

        self.add_item(c)
    
    def roll(self, interaction: discord.Interaction):

        # 擲骰決定結果
        result = dice.roll(1, 20)[0]

        match result:
            case 20: # 大成功
                outcome = Outcome.CRITICAL_SUCCESS
            case r if r >= 5: # 成功
                outcome = Outcome.SUCCESS
            case r if r < 5: # 失敗
                outcome = Outcome.FAILURE
            case 1:  # 大失敗
                outcome = Outcome.CRITICAL_FAILURE

        # 大失敗或失敗直接跳過戰利品取得
        if outcome == Outcome.CRITICAL_FAILURE or outcome == Outcome.FAILURE:
            return result, outcome

        # 取得戰利品表
        loot_table = region.get_loot_table(player.get_region(interaction.user.id), "fishing")
        if loot_table is None:
            raise ValueError("Fishing | Loot table not found.")
        
        loots = loot_table.roll(1)

        items = []
        for (item_type, item_id), quantity in loots.items():
            reward.give(interaction.user.id, item_type, item_id, quantity)
            items.append(item.fmtstr_short(item_id, quantity))

        return result, outcome

async def setup(bot: commands.Bot):
    await bot.add_cog(FishingCog(bot))