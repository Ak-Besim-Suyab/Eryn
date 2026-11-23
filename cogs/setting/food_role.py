from discord.ext import commands

from ui.views import RoleSettingView

TITLE = "<:latte:1538825725971533924> 食物 Food 身分組（顏色）"
MEDIA = "https://cdn.discordapp.com/attachments/1491046495812718672/1574517682240487546/gradient_2.jpg"
POOL  = "food"


class FoodRoleSettingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="food_role_setting")
    @commands.is_owner()
    async def food_role_setting(self, ctx: commands.Context):
        await ctx.send(view=RoleSettingView(title=TITLE, media=MEDIA, pool=POOL))


async def setup(bot: commands.Bot):
    await bot.add_cog(FoodRoleSettingCog(bot))
    bot.add_view(RoleSettingView(title=TITLE, media=MEDIA, pool=POOL))
