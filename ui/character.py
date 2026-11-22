import discord

from lib import view
from lib import information
# from data.schema.event import ButtonEvent
from ui.button import RESOURCE_BUTTON

async def character_tab(interaction: discord.Interaction):
    v = (view
         .create("character_tab", **information.get(interaction.user))
         .add_item(discord.ui.ActionRow(RESOURCE_BUTTON)))

    await interaction.response.send_message(view=v, ephemeral=True)

# async def on_character_tab(event: ButtonEvent): await character_tab(event.interaction)