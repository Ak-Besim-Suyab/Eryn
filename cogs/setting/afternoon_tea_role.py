from discord.ext import commands

from ui.views import RoleSettingView

TITLE = "<:berry_pie:1484226514336612472> 下午茶身分組（圖案）"
MEDIA = "https://cdn.discordapp.com/attachments/1491046495812718672/1574822279454654544/tea.png"
TAG   = "afternoon_tea"


class AfternoonTeaRoleSettingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="afternoon_tea_role_setting")
    @commands.is_owner()
    async def afternoon_tea_role_setting(self, ctx: commands.Context):
        await ctx.send(view=RoleSettingView(title=TITLE, media=MEDIA, tag=TAG))


async def setup(bot: commands.Bot):
    await bot.add_cog(AfternoonTeaRoleSettingCog(bot))
    bot.add_view(RoleSettingView(title=TITLE, media=MEDIA, tag=TAG))
