import discord

from cores import query

from game import model


class Select(discord.ui.Select):
    def __init__(self, select: model.Select):

        self.select = select

        options = query.ask(model.SelectOptionQuery(select.custom_id))
        
        if options is None:
            options = []

        super().__init__(
            custom_id=select.custom_id,
            placeholder=select.placeholder,
            min_values=select.min_values,
            max_values=select.max_values,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("test", ephemeral=True)