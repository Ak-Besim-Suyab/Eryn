import discord
from discord import ui
from discord.ext import commands

from cores import logger
from data import ROLES


# 各主題下拉選單設定：(placeholder, custom_id, tag)
CHARGE_SELECTS: list[tuple[str, str, str]] = [
    ("主題：麥塊 Minecraft", "select_minecraft_role", "minecraft"),
    ("主題：皮克敏 Pikmin", "select_pikmin_role", "pikmin"),
    ("主題：下午茶 Afternoon Tea", "select_afternoon_tea_role", "afternoon_tea"),
    ("主題：噗浪 Plurk", "select_plurk_role", "plurk"),
]

TINCTURE_SELECTS: list[tuple[str, str, str]] = [
    ("主題：花朵 Flower", "select_flower_role", "flower"),
    ("主題：食物 Food", "select_food_role", "food"),
]


class RoleSettingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["role_setting"])
    @commands.is_owner()
    async def role_book(self, ctx: commands.Context):
        await ctx.send(view=RoleSettingView())


class RoleSettingView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        c = discord.ui.Container(accent_color=0)

        c.add_item(
            discord.ui.TextDisplay(
                "\n".join(
                    [
                        "## 裝飾身分組設定",
                        "這裡有許多特別的裝飾身分組提供選擇，旅人可以自由搭配屬於自己的獨特暱稱！",
                    ]
                )
            )
        )
        c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))

        c.add_item(
            discord.ui.TextDisplay(
                "\n".join(
                    [
                        "### <:berry_pie:1484226514336612472> 請選擇想套用的圖案身分組",
                        "> 請注意：同類型的身分組同時只會套用 1 個。",
                    ]
                )
            )
        )
        for placeholder, custom_id, tag in CHARGE_SELECTS:
            c.add_item(ui.ActionRow(RoleSelect(custom_id=custom_id, placeholder=placeholder, tag=tag)))

        c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))

        c.add_item(
            discord.ui.TextDisplay(
                "\n".join(
                    [
                        "### <:rudbeckia:1467093280071094333> 請選擇想套用的顏色身分組",
                        "> 請注意：同類型的身分組同時只會套用 1 個。",
                    ]
                )
            )
        )
        for placeholder, custom_id, tag in TINCTURE_SELECTS:
            c.add_item(ui.ActionRow(RoleSelect(custom_id=custom_id, placeholder=placeholder, tag=tag)))

        self.add_item(c)


class RoleSelect(discord.ui.Select):
    def __init__(self, custom_id: str, placeholder: str = "選擇想套用的身分組", **filters):

        roles = ROLES.find(**filters)
        if not roles:
            raise ValueError(f"找不到符合條件的身分組，無法建立選單")

        options = [
            discord.SelectOption(
                label=role_data.name,
                emoji=role_data.icon,
                value=role_data.id,
            )
            for role_data in roles
        ]

        super().__init__(
            placeholder=placeholder,
            custom_id=custom_id,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if interaction.guild is None or not isinstance(interaction.user, discord.Member):
            await interaction.followup.send("❌ 此功能僅限在伺服器內使用。", ephemeral=True)
            return

        role_data = ROLES.get(self.values[0])
        if role_data is None:
            await interaction.followup.send("❌ 發生錯誤，找不到該身分組設定，請回報管理員！", ephemeral=True)
            return

        selected_role = interaction.guild.get_role(role_data.discord_id)
        if selected_role is None:
            await interaction.followup.send("❌ 發生錯誤，該身分組似乎不存在，請回報管理員！", ephemeral=True)
            return

        try:
            # 取得相同分類的身分組資料，用於檢查唯一身分組
            category_roles = ROLES.find(category=role_data.category)
            category_role_ids = {r.discord_id for r in category_roles}

            # 取得要移除的其他同類身分組
            removing_roles = [r for r in interaction.user.roles if r.id in category_role_ids]

            # 移除其他同類身分組，接著套用新的身分組
            if removing_roles:
                await interaction.user.remove_roles(*removing_roles, reason="套用唯一身分組，移除其他相同分類身分組")
            await interaction.user.add_roles(selected_role, reason="使用下拉式選單套用身分組")

            await interaction.followup.send("✅ 身分組套用成功，在社群頻道裡查看您的外觀吧！", ephemeral=True)
        except discord.errors.Forbidden:
            await interaction.followup.send(
                "❌ 出現預期外的錯誤，咪沒有權限套用該身分組... 請管理員檢查權限！",
                ephemeral=True,
            )
        except Exception as e:
            await interaction.followup.send("❌ 出現預期外的錯誤，請管理員檢查日誌！", ephemeral=True)
            logger.exception(f"使用者套用身分組時發生錯誤：{e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleSettingCog(bot))
