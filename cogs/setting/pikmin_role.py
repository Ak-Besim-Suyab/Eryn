from discord.ext import commands

from ui.views import RoleSettingView

TITLE = "<:red_pikmin:1532614703367454742> 皮克敏 Pikmin 身分組（圖案）"
MEDIA = "https://cdn.discordapp.com/attachments/1491046495812718672/1574496239456882840/ffxiv_evercold.png"
POOL  = "pikmin"


class PikminRoleSettingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="pikmin_role_setting")
    @commands.is_owner()
    async def pikmin_role_setting(self, ctx: commands.Context):
        await ctx.send(view=RoleSettingView(title=TITLE, media=MEDIA, pool=POOL))


async def setup(bot: commands.Bot):
    await bot.add_cog(PikminRoleSettingCog(bot))
    bot.add_view(RoleSettingView(title=TITLE, media=MEDIA, pool=POOL))
