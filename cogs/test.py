import discord
from discord.ext import commands
from discord import ui
from discord import SeparatorSpacing

from systems import registry

from cores import logger

minecraft_options = [
    "potato",
    "baked_potato",
    "poison_potato",
    "pufferfish",
]

final_fantasy_options = [
    "online",
    "offline",
    "afk",
    "mentor",
    "sprout",
    "vulnerability_up",
    "brink_to_death",
    "damage_down",
    "heavy",
    "doom",
    "squirrel_prayer",
    "inugami_favor",
    "graha_tia",
    "greystone",
]

afternoon_tea_options = [
    "fruit_tart",
    "lemon_pie",
    "berry_pie",
    "vanilla_roll",
    "strawberry_roll",
    "matcha_roll",
    "mont_blanc",
    "black_forest",
    "chocolate_cake",
    "buttered_toast",
    "pancake",
    "pudding",
    "ice_cream",
    "strawberry_donut",
]

plurk_options = [
    "baby_fox",
    "baby_white_fox",
    "baby_black_fox",
    "baby_wolf",
    "leopard",
    "crocodile",
    "pink_frog",
    "pome",
    "shark",
]

flower_options = [
    "rose",
    "mume",
    "hydrangea",
    "forget_me_not",
    "clary_sage",
    "lilac",
    "sakura",
    "rudbeckia",
    "clover",
]

gradient_options = [
    "abyss",
    "afterglow",
    "ash",
    "aurora",
    "autumn",
    "crimson",
    "dawn",
    "mist",
    "niello",
    "prism",
    "summer",
    "tropic",
    "twilight",
    "winter",
]

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context):
        view = TestLayoutView()
        message = await ctx.send(view=view)

class TestLayoutView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        minecraft_select = RoleSelect(
            placeholder="麥塊主題身分組（Minecraft Roles）",
            option_values=minecraft_options,
            custom_id="role_select:minecraft",
        )

        final_fantasy_select = RoleSelect(
            placeholder="最終幻想主題身分組（Final Fantasy Roles）",
            option_values=final_fantasy_options,
            custom_id="role_select:final_fantasy",
        )

        afternoon_tea_select = RoleSelect(
            placeholder="下午茶主題身分組（Afternoon Tea Roles）",
            option_values=afternoon_tea_options,
            custom_id="role_select:afternoon_tea",
        )

        plurk_select = RoleSelect(
            placeholder="噗浪主題身分組（Plurk Roles）",
            option_values=plurk_options,
            custom_id="role_select:plurk",
        )

        flower_select = RoleSelect(
            placeholder="花主題身分組（Flower Roles）",
            option_values=flower_options,
            custom_id="role_select:flower",
        )

        gradient_select = RoleSelect(
            placeholder="漸層主題身分組（Gradient Roles）",
            option_values=gradient_options,
            custom_id="role_select:gradient",
        )

        title = ui.TextDisplay(content="## 🏷️身分組設定")
        description_charges = ui.TextDisplay(content="### <:berry_pie:1484226514336612472> 請選擇想套用的圖案身分組\n> 請注意：同類型的身分組同時只會套用 1 個。")
        description_tinctures = ui.TextDisplay(content="### <:rudbeckia:1467093280071094333> 請選擇想套用的顏色身分組\n> 請注意：同類型的身分組同時只會套用 1 個。")

        container = ui.Container(title)
        container.accent_color = discord.Color.gold()

        descriptions = [
            "社群非常鼓勵旅人自由搭配屬於自己的獨特暱稱外觀，這裡有許多有趣的身分組提供選擇！",
        ]

        description = ui.TextDisplay(content="\n".join(descriptions))

        row = ui.ActionRow()
        row.add_item(minecraft_select)

        row_2 = ui.ActionRow()
        row_2.add_item(final_fantasy_select)

        row_3 = ui.ActionRow()
        row_3.add_item(afternoon_tea_select)

        row_4 = ui.ActionRow()
        row_4.add_item(plurk_select)

        row_5 = ui.ActionRow()
        row_5.add_item(flower_select)

        row_6 = ui.ActionRow()
        row_6.add_item(gradient_select)

        seperator = ui.Separator(spacing=SeparatorSpacing.large)

        components = [
            description,
            seperator,
            description_charges,
            row,
            row_2,
            row_3,
            row_4,
            seperator,
            description_tinctures,
            row_5,
            row_6,
        ]

        for comp in components:
            container.add_item(comp)

        self.add_item(container)

class RoleSelect(ui.Select):
    def __init__(self, placeholder: str, option_values: list[str], custom_id: str = None):

        options = []

        for value in option_values:
            role = registry.role.get(value)
            if role is None:
                raise ValueError(f"Role with tag '{value}' not found in registry.")

            option = discord.SelectOption(
                label=role.name,
                emoji=role.icon if role.icon else None,
                description="選擇後會套用身分組",
                value=value,
            )
            options.append(option)

        super().__init__(
            placeholder=placeholder,
            options=options,
            custom_id=custom_id,
        )
    
    async def callback(self, interaction: discord.Interaction):

        selected_role = registry.role.get(self.values[0])

        guild_roles = interaction.guild.roles

        for guild_role in guild_roles:
            if guild_role.id == selected_role.discord_id:
                role = guild_role
                break

        if role is None:
            await interaction.response.send_message("❌ 伺服器找不到該身分組，請向管理員回報！", ephemeral=True)
            return
        
        if role in interaction.user.roles:
            await interaction.response.send_message("❌ 你已套用該身分組！", ephemeral=True)
            return

        try:
            # 移除所有同分類的身分組，確保只有一個相同分類的身分組被套用
            all_roles = registry.role.get_all()

            for user_role in interaction.user.roles:
                for all_role in all_roles:
                    # 判斷使用者的身分組是否在身分組註冊表中，是的話，判斷該身分組 (使用 all_role) 是否與選擇的身分組同分類
                    if all_role.discord_id == user_role.id and all_role.category == selected_role.category:
                            await interaction.user.remove_roles(user_role)

            # 套用新選擇的身分組
            await interaction.user.add_roles(role)

            await interaction.response.edit_message(view=self.view)
            await interaction.followup.send("✅ 成功套用身分組", ephemeral=True)
        except discord.errors.Forbidden:
            await interaction.response.send_message("❌ 出現預期外的錯誤，咪沒有權限套用該身分組... 請管理員檢查權限！", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("❌ 出現預期外的錯誤，請管理員檢查！", ephemeral=True)
            logger.exception(f"使用者套用身分組時發生錯誤：{e}")

async def setup(bot):
    await bot.add_cog(TestCog(bot))

"""
筆記:
    ui.TextDisplay:: 容器元件，用於印出文本。
        content:: 要印出的文本。

    ui.Separator:: 容器元件，用於分隔不同區塊的內容。
        visible:: 設定分隔線是否可見。
        spacing:: 設定分隔線與其他元件之間的距離。

    ui.Section:: 容器元件，用於插入其他容器元件以及 Button, Thumbnail 元件。
        accessory:: 設定 Section 右側的 Button, Thumbnail 元件。

    ui.ActionRow:: 用於水平排列 Button 元件的容器。

    ui.Container:: 用於容納其他元件的容器，可以用來組織和排列內部的元件。
        Container.accent_color:: 設定容器左邊邊框的顏色。
        Container.spoiler:: 設定容器內文本是否為暴雷內容。
"""