import discord
from discord.ext import commands

from models.message import message_manager

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def test_message(self, ctx: commands.Context):

        # 測試 message manager 是否能印出 test
        # embed = message_manager.create("test")

        embed = discord.Embed()
        embed.title = ctx.author.display_name

        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        # 測試空字串是否能正常印出
        # embed.set_author(name="", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed, view=TestMessageView())

    @commands.command()
    @commands.is_owner()
    async def test_no_interaction(self, ctx: commands.Context):
        """
        測試 title_type = player 的 message 在不傳入 intercation 的情況下回傳的結果
        
        測試結果：
        回報了 'NoneType' object has no attribute 'user'

        這會導致訊息沒有發送出去, 因此在 create() 中, 傳入 interaction 的段落需要加上 try except 或 if 來避免訊息發送失敗
        """
        embed = message_manager.create("test_no_interaction")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def test_parameter(self, ctx: commands.Context):
        """
        測試參數是否能正確傳入，以及在缺少特定參數傳入的情況下會如何報錯
        """
        payload = {
            "level": 10,
            "experience": "unknown"
        }
        
        embed = message_manager.create("test_parameter", payload)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def test_select(self, ctx: commands.Context):
        await ctx.send('test', view=TestView())
    

    @commands.command()
    @commands.is_owner()
    async def test_modal(self, ctx: commands.Context):
        await ctx.send('test', view=TestModalView())


class TestMessageView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Test Fields", style=discord.ButtonStyle.primary, row=0)
    async def test_fields(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = message_manager.create("test_fields")
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Test Payload", style=discord.ButtonStyle.primary, row=0)
    async def test_payload(self, interaction: discord.Interaction, button: discord.ui.Button):
        payload = {
            "interaciton": interaction
        }
        embed = message_manager.create("test_payload", payload)
        await interaction.response.send_message(embed=embed)


class TestView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Select an option",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Option 1",
                description="This is option 1",
                value="1"
            ),
            discord.SelectOption(
                label="Option 2",
                description="This is option 2",
                value="2"
            ),
        ],
        row=0
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"You selected {select.values[0]}")

class TestModalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

class TestModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Test Modal")

async def setup(bot):
    await bot.add_cog(TestCog(bot))