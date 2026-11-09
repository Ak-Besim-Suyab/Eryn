import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

from lib.view import create_view

class UnitTestCog(commands.Cog):
    """ 這個 Cog 用於需要傳入互動元件的單元測試, 普通單元測試請到 scripts 進行編寫
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx: commands.Context):

        line = "**📦 鱈魚（持有： 2 個）**\n> -# 可以吃 | 可以分解"

        empty_item = ui.TextDisplay(content = "測試")

        container = ui.Container()
        container.add_item(ui.TextDisplay(content = "## 🪎 Suyab 背包"))
        container.add_item(ui.Separator(spacing = discord.SeparatorSpacing.large))
        container.add_item(ui.Section(
            "**📦 榛木釣竿（持有： 1 個）**\n> -# 無", 
            accessory = ui.Button(label = "選擇", style = discord.ButtonStyle.secondary)))
        container.add_item(ui.Section(
            "**📦 榛木釣竿（持有： 1 個）**\n> -# 無", 
            accessory = ui.Button(label = "選擇", style = discord.ButtonStyle.secondary)))
        container.add_item(ui.Section(
            "**📦 榛木釣竿（持有： 1 個）**\n> -# 無", 
            accessory = ui.Button(label = "選擇", style = discord.ButtonStyle.secondary)))
        container.add_item(ui.Section(
            "**📦 榛木釣竿（持有： 1 個）**\n> -# 無", 
            accessory = ui.Button(label = "選擇", style = discord.ButtonStyle.secondary)))
        container.add_item(ui.Section(
            "**📦 鱈魚（持有： 2 個）**\n> -# 可以吃，也可以分解為食物資源。", 
            accessory = ui.Button(label = "選擇", style = discord.ButtonStyle.secondary)))
        container.add_item(ui.Section(
            "**📦 鮭魚（持有： 5 個）**\n> -# 可以吃 | 可以分解", 
            accessory = ui.Button(label = "選擇", style = discord.ButtonStyle.secondary)))
        container.add_item(ui.Section(
            "**📦 木箱（持有： 10 個）**\n> -# 可以打開", 
            accessory = ui.Button(label = "選擇", style = discord.ButtonStyle.secondary)))
        container.add_item(ui.Section(
            line, 
            accessory = ui.Button(label = "選擇", style = discord.ButtonStyle.secondary)))

        row = ui.ActionRow()
        row.add_item(ui.Select(
            placeholder = "選擇分類",
            min_values = 1,
            max_values = 1,
            options = [
                discord.SelectOption(label = "第一個", value = "1"),
                discord.SelectOption(label = "第二個", value = "2"),
                discord.SelectOption(label = "第三個", value = "3"),
                discord.SelectOption(label = "第四個", value = "4"),
                discord.SelectOption(label = "第五個", value = "5"),
            ]
        ))
        container.add_item(row)

        row = ui.ActionRow()
        row.add_item(ui.Button(label = "上一頁", style = discord.ButtonStyle.secondary))
        row.add_item(ui.Button(label = "下一頁", style = discord.ButtonStyle.secondary))
        container.add_item(row)

        view = ui.LayoutView().add_item(container)

        for _ in range(10):
            view.add_item(empty_item)
        
        await ctx.send(view=view)

    @app_commands.command(name="測試", description="測試用指令")
    @app_commands.default_permissions(administrator=True)
    async def unittest_slash(self, interaction: discord.Interaction):

        from ui import SanctuaryView
        view = SanctuaryView()
        await interaction.response.send_message(view=view)

        # # test if create_view function works.
        # view = create_view("template")
        # await interaction.response.send_message(view=view)

        # # create fake param dict.
        # param = {
        #     "name": "Elin",
        #     "level": 1,
        #     "experience": 100
        # }

        # # test if function works with container object, string and param 
        # container = ui.Container()
        # container.add_item(ui.TextDisplay(content = "# This is Another Container Test."))
        # view = create_view(container, "template_param", **param)
        # await interaction.followup.send(view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(UnitTestCog(bot))
