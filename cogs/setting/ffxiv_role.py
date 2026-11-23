from discord.ext import commands

from ui.views import RoleSettingView

TITLE = "<:ffxiv_mentor:1484220305617715300> Final Fantasy XIV 身分組（圖案）"
MEDIA = "https://cdn.discordapp.com/attachments/1491046495812718672/1574496239456882840/ffxiv_evercold.png"
POOL  = "final_fantasy"


class FFXIVRoleSettingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ffxiv_role_setting")
    @commands.is_owner()
    async def ffxiv_role_setting(self, ctx: commands.Context):
        await ctx.send(view=RoleSettingView(title=TITLE, media=MEDIA, pool=POOL))


async def setup(bot: commands.Bot):
    await bot.add_cog(FFXIVRoleSettingCog(bot))
    bot.add_view(RoleSettingView(title=TITLE, media=MEDIA, pool=POOL))
