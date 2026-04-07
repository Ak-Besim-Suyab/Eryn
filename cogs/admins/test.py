import discord
from discord.ext import commands

from models.message import message_manager

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def test_message(self, ctx: commands.Context):
        embed = message_manager.create("test")
        await ctx.send(embed=embed, view=TestMessageView())


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