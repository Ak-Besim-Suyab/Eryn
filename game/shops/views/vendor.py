import discord

from models.player.model import Player
from models.inventory.model import Inventory

vendor_portrait = "https://cdn.discordapp.com/attachments/1193049715638538283/1480680097353826447/vendor_portrait.png"

class VendorEmbed(discord.Embed):
    def __init__(self):
        super().__init__()

        description = [
            "「...。」",
            "",
            "> 選擇要「購買」的物品以進行交易（可複選）"
        ]

        self.title = "雜貨商"
        self.description = "\n".join(description)
        self.color = discord.Color.gold()
        self.set_thumbnail(url=vendor_portrait)


class VendorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

        self.add_item(VendorOption())


class VendorOption(discord.ui.Select):
    def __init__(self):
        shop  = shop_manager.get("vendor")

        options = []
        for item in shop.item_list:
            item_ = item_manager.get(item)
            option = discord.SelectOption(
                label=item_.name,
                value=item_.id,
            )
            options.append(option)

        super().__init__(
            placeholder="選擇要購買的物品", 
            min_values=1,
            max_values=len(options),
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        embed = discord.Embed()
        embed.title = "雜貨商"
        embed.description = "「嗯... 成交！」"
        embed.color = discord.Color.gold()
        embed.set_thumbnail(url=vendor_portrait)

        player_embed = discord.Embed()
        player_embed.description = "> *你端詳著物品，並滿意地支付金幣。*"
        player_embed.color = discord.Color.dark_gold()
        player_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        descriptions = []
        price = 0

        # 這裡要補上如果金幣不足時的判斷
        
        for item in self.values:
            item_ = item_manager.get(item)

            description = f"{item_.image}{item_.name} x1"
            descriptions.append(description)

            price += item_.price

            Inventory.add_item(interaction.user.id, item_.id, 1)
            Player.remove_balance(interaction.user.id, item_.price)

        player_embed.add_field(name="獲得物品：", value="\n".join(descriptions), inline=False)
        player_embed.add_field(name="費用：", value=f"-{price} 金幣", inline=False)

        await interaction.response.edit_message(embeds=[embed, player_embed])