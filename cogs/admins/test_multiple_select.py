import discord
from discord.ext import commands
from discord import app_commands

class MultipleSelectTestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="multiple_select_test", description="測試")
    async def execute_multiple_select_test(self, interaction: discord.Interaction):
        await interaction.response.send_message("測試", view=TestView())
        
class TestView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        # 🌟 1. 建立變數來儲存兩個選單的結果
        self.selection_1 = None
        self.selection_2 = None

        self.add_item(TestSelect())
        self.add_item(AnotherTestSelect())

    # 🌟 2. 建立一個統一的檢查與執行中心
    async def check_and_execute(self, interaction: discord.Interaction):
        # 檢查是否兩個變數都有值了（使用者兩個都選過了）
        if self.selection_1 is not None and self.selection_2 is not None:
            
            # 這裡放你的「後續邏輯」
            result_text = f"成功！你同時選擇了 **{self.selection_1}** 和 **{self.selection_2}**，開始執行後續邏輯！"
            
            # 可以選擇更新原訊息，或是發送新訊息
            await interaction.response.edit_message(content=result_text, view=None) # view=None 可以順便把選單清掉
            
        else:
            # 如果只選了一個，Discord 仍需要一個回應，否則會顯示「此互動失敗」
            # 我們使用 defer() 來默默承認這個互動，不改變畫面
            await interaction.response.defer()
            

class TestSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Option 1", description="This is option 1"),
            discord.SelectOption(label="Option 2", description="This is option 2"),
        ]
        super().__init__(placeholder="Select an option (1 or 2)", min_values=1, max_values=1, options=options)

    # 🌟 3. 實作 callback，將資料回傳給大腦 (TestView)
    async def callback(self, interaction: discord.Interaction):
        # self.values[0] 就是玩家選中的值
        # 透過 self.view 存取父節點 TestView，把值存進去
        self.view.selection_1 = self.values[0]
        
        # 呼叫大腦檢查是否都選完了
        await self.view.check_and_execute(interaction)


class AnotherTestSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Option 3", description="This is option 3"),
            discord.SelectOption(label="Option 4", description="This is option 4"),
        ]
        super().__init__(placeholder="Select an option (3 or 4)", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # 一樣將值存回父節點
        self.view.selection_2 = self.values[0]
        
        # 呼叫大腦檢查是否都選完了
        await self.view.check_and_execute(interaction)


async def setup(bot):
    await bot.add_cog(MultipleSelectTestCog(bot))