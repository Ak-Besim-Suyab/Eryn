import discord
from discord import ui
from discord.ext import commands

from cogs.setting.role_setting import RoleSelect

# TODO: 補上漸層身分組預覽圖片網址，留空時不會顯示圖片區塊
MEDIA = ""


class GradientRoleSettingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="gradient_role_setting")
    @commands.is_owner()
    async def gradient_role_setting(self, ctx: commands.Context):
        await ctx.send(view=GradientRoleSettingView())


class GradientRoleSettingView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        select = RoleSelect(custom_id="select_gradient_role", tag="gradient")

        c = discord.ui.Container()

        if MEDIA:
            c.add_item(discord.ui.MediaGallery().add_item(media=MEDIA))
            c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))

        c.add_item(
            discord.ui.TextDisplay(
                "\n".join(
                    [
                        "## <:prism:1508384924628025374> 漸層 Gradient 身分組（顏色）",
                        "> 請注意：同類型的顏色身分組同時只會套用 1 個。",
                    ]
                )
            )
        )
        c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        c.add_item(ui.ActionRow(select))

        self.add_item(c)


async def setup(bot: commands.Bot):
    await bot.add_cog(GradientRoleSettingCog(bot))
