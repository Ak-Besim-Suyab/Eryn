import discord
from discord.ext import commands
from discord import ui

from data import MATERIALS, LINES
from data.enums import BuildingName, MaterialName

from ui.button import BUILDING_GUIDE_BUTTON, RESOURCE_BUTTON
from lib import building
from lib import view, skill

BUILDING_NAME = BuildingName.SANCTUARY
MEDIA = "https://cdn.discordapp.com/attachments/1491046495812718672/1573663788362633267/sanctuary.png"

class SanctuaryCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def sanctuary(self, ctx: commands.Context):
        await ctx.send(view=SanctuaryView())

class SanctuaryView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout = None)

        self.render()

    def render(self):
    
        # 宣告容器
        c = discord.ui.Container()

        # 內容
        c.add_item(discord.ui.MediaGallery().add_item(media=MEDIA))
        c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        c.add_item(self.intro())
        c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))
        c.add_item(self.status())
        c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))

        # 操作
        action_row = ui.ActionRow()
        action_row.add_item(SanctuarySelect())

        c.add_item(action_row)

        # 清除舊元件
        self.clear_items()

        # 添加新元件 (這裡的按鈕在容器外，所以此時才添加)
        EFFECT_BUTTON = ui.Button(label="查看效果", style=discord.ButtonStyle.secondary, custom_id="sanctuary_effect")
        EFFECT_BUTTON.callback = self.effect_callback

        self.add_item(c)
        self.add_item(ui.ActionRow(RESOURCE_BUTTON, EFFECT_BUTTON, BUILDING_GUIDE_BUTTON))

    def intro(self) -> discord.ui.TextDisplay:

        b = building.get(BUILDING_NAME)
        
        intro = "\n".join(
            [
                f"## 聖所（Lv. {b.level}）",
                f"> *位於城鎮中心的教堂，無數信徒正在這裡祈禱，同時也有無數苦難者在等待援助。*",
                f"",
                f"- 旅行者可以提供材料以升級聖所並強化相應效果",
                f"- 所有旅行者都可以獲得來自聖所的效果",
            ]
        )
        
        return discord.ui.TextDisplay(intro)

    def status(self) -> discord.ui.TextDisplay:

        # 該建築不支援的材料
        EXCLUDED_MATERIALS = ["iron"]

        status = []

        for mat in MaterialName:

            # 檢查是否為不支援材料
            if mat in EXCLUDED_MATERIALS:
                continue

            mat = MATERIALS.get(mat)

            if not mat:
                raise ValueError(f"Material {mat} not found")

            mat_icon    = mat.icon
            mat_level   = building.get_rlevel(BUILDING_NAME, mat.id)
            mat_current = building.get_contribution(BUILDING_NAME, mat.id)
            mat_require = building.get_resource_requirement(level=mat_level)
                
            status.append(f"- {mat_icon} **{mat_current} / {mat_require}**（階級 **{mat_level}**）")

        return discord.ui.TextDisplay("\n".join(status))
    
    async def effect_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=SanctuaryEffectView(), ephemeral=True)

class SanctuaryEffectView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__()

        c = discord.ui.Container()
        c.add_item(self.effect())
        
        self.add_item(c)
    
    def effect(self) -> discord.ui.TextDisplay:

        b = building.get(BUILDING_NAME)

        build_level = b.level
        food_level  = building.get_rlevel(BUILDING_NAME, MaterialName.FOOD)
        wood_level  = building.get_rlevel(BUILDING_NAME, MaterialName.WOOD)
        stone_level = building.get_rlevel(BUILDING_NAME, MaterialName.STONE)
        
        effect = "\n".join(
            [
                f"## 效果",
                f"### 聖所",
                f"- 獲得更多經驗值（階級 {build_level}）",
                f"### 合建結果",
                f"- 來自發送訊息所獲得的經驗值提升（階級 {food_level}）",
                f"- 來自發送表情所獲得的經驗值提升（階級 {wood_level}）",
                f"- 來自語音所獲得的經驗值提升（階級 {stone_level}）",
            ]
        )

        return discord.ui.TextDisplay(effect)

class SanctuarySelect(ui.Select):
    def __init__(self):

        actions = [
            ("提供 100 食物",   "food:100",  "🥩"),
            ("提供 500 食物",   "food:500",  "🥩"),
            ("提供 1,000 食物", "food:1000", "🥩"),

            ("提供 100 木材",   "wood:100",  "🪵"),
            ("提供 500 木材",   "wood:500",  "🪵"),
            ("提供 1,000 木材", "wood:1000", "🪵"),

            ("提供 100 石材",   "stone:100",  "🪨"),
            ("提供 500 石材",   "stone:500",  "🪨"),
            ("提供 1,000 石材", "stone:1000", "🪨"),
        ]

        options = []
        for label, value, emoji in actions:
            options.append(discord.SelectOption(label = label, value = value, emoji = emoji))

        super().__init__(
            placeholder = "選擇要提供的材料", 
            options = options,
            custom_id = "sanctuary:select",
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)
 
        res, quantity = self.values[0].split(":")
        success, msg = building.add_contribution(interaction.user.id, "sanctuary", res, int(quantity))

        if success:
            building.add_experience("sanctuary", float(quantity))
            skill.add_experience(interaction.user.id, "faith", float(quantity))

        v = self.view; v.render()
        await interaction.edit_original_response(view=v)

        if not success and msg:
            kwargs = {
                "player_name": interaction.user.display_name,
                "line": LINES.get("offer_fail").random(),
            }

            v = view.create("offer_fail", **kwargs)

            await interaction.followup.send(view=v, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(SanctuaryCog(bot))