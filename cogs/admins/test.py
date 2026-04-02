import discord
from discord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def test_select(self, ctx: commands.Context):
        await ctx.send('test', view=TestView())

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

async def setup(bot):
    await bot.add_cog(TestCog(bot))