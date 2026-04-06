import discord
from systems.events.season import season_event

class SeasonEventView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="緬懷", style=discord.ButtonStyle.primary, emoji="🕯️", custom_id="mourn")
    async def mourn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await season_event.mourn(interaction)

    @discord.ui.button(label="供奉", style=discord.ButtonStyle.primary, emoji="🕯️", custom_id="season_offer")
    async def season_offer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await season_event.pre_offer(interaction)

    @discord.ui.button(label="這是什麼？", style=discord.ButtonStyle.secondary, custom_id="season_event_help")
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        lines = [
            "咪，這是個糟糕版的限時活動！",
            "你可以簡單地按按鈕來獲得獎勵，並藉此緬懷我們的勇士；按鈕可以重複使用，但有短暫的冷卻時間",
        ]

        embed = discord.Embed()
        embed.title = "Elin"
        embed.description = "\n".join(lines)
        embed.color = discord.Color.gold()
        embed.set_thumbnail(url=interaction.client.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class PreOfferView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="確定", style=discord.ButtonStyle.primary, custom_id="season_offer_confirm")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await season_event.offer(interaction)
    
    @discord.ui.button(label="取消", style=discord.ButtonStyle.secondary, custom_id="season_offer_cancel")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ 你覺得不需要供奉了。", ephemeral=True)