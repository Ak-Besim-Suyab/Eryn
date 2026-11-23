import discord
from discord import ui
from discord.ext import commands

from cogs.setting.role_setting import RoleSelect

MEDIA = "https://cdn.discordapp.com/attachments/1491046495812718672/1574496239456882840/ffxiv_evercold.png"

class FFXIVRoleSettingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ffxiv_role_setting")
    @commands.is_owner()
    async def ffxiv_role_setting(self, ctx: commands.Context):
        await ctx.send(view=FFXIVRoleSettingView())


class FFXIVRoleSettingView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        select = RoleSelect(custom_id="select_finalfantasy_role", tag="final_fantasy")

        c = discord.ui.Container()

        c.add_item(discord.ui.MediaGallery().add_item(media=MEDIA))
        c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))

        c.add_item(
            discord.ui.TextDisplay(
                "\n".join(
                    [
                        "## <:ffxiv_mentor:1484220305617715300> Final Fantasy XIV 身分組（圖案）",
                        "> 請注意：同類型的圖案身分組同時只會套用 1 個。",
                    ]
                )
            )   
        )
        c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        c.add_item(ui.ActionRow(select))

        self.add_item(c)


async def setup(bot: commands.Bot):
    await bot.add_cog(FFXIVRoleSettingCog(bot))
