import discord

from ui.roles.theme import RoleThemeEmbed, RoleThemeView, RoleInfoEmbed

role_img = "https://cdn.discordapp.com/attachments/1193049715638538283/1483857918532128808/college_of_arms_img.png"

class RoleCategoryEmbed(discord.Embed):
    def __init__(self, interaction: discord.Interaction, category: str):
        super().__init__()

        tincture_description = [
            "> *紋章官在長桌上擺滿布料，展示著各種華麗的底色*",
            "> *這些底色或鮮豔奪目，或印象深刻，你思索著並認真選擇適合自己的底色*",
        ]
        charge_description = [
            "> 紋章官在長桌上擺滿徽記雕紋，這些雕紋繁複、有趣、富有深意",
            "> *每種徽記都代表著不同的身分與意義，你思索著並認真選擇適合自己的徽記*",
            ]

        descriptions = {
            "tinctures": tincture_description,
            "charges": charge_description
        }

        tincture_values = [
            "- 花與四季系列",
            "- 漸層與彩色系列",
        ]

        charge_values = [
            "- 最終幻想系列",
            "- 麥塊系列",
            "- 噗浪系列",
            "- 下午茶系列",
        ]

        values = {
            "tinctures": tincture_values,
            "charges": charge_values
        }

        description = "\n".join(descriptions.get(category))
        value = "\n".join(values.get(category))

        self.description = description
        self.color = discord.Color.gold()

        self.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        self.add_field(name="選擇以下主題進行操作：", value=value, inline=False)


class RoleCategoryView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, category: str):
        super().__init__(timeout=None)

        self.add_item(RoleCategoryOption(category))


class RoleCategoryOption(discord.ui.Select):
    def __init__(self, category: str):
        self.category = category
        groups = [
            {
                "category": "tinctures",
                "name": "flower",
                "display_name": "花與四季",
            },
            {
                "category": "tinctures",
                "name": "gradient",
                "display_name": "漸層與彩色",
            },
            {
                "category": "charges",
                "name": "final_fantasy",
                "display_name": "最終幻想",
            },
            {
                "category": "charges",
                "name": "minecraft",
                "display_name": "麥塊",
            },
            {
                "category": "charges",
                "name": "plurk",
                "display_name": "噗浪",
            },
            {
                "category": "charges",
                "name": "afternoon_tea",
                "display_name": "下午茶",
            },
        ]

        options = []
        for group in groups:
            if group.get("category") == category:
                option = discord.SelectOption(
                    label=group.get("display_name"), 
                    value=group.get("name"), 
                    emoji="🎨"
                )
                options.append(option)

        super().__init__(
            placeholder="請選擇主題", 
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        group = self.values[0]

        embed = RoleThemeEmbed(interaction, self.category, group)
        view = RoleThemeView(interaction, self.category, group)
        info_embed = RoleInfoEmbed()

        await interaction.response.send_message(embeds=[embed, info_embed], view=view)