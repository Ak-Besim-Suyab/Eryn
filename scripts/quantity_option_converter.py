import discord
from .protocol import OptionConvertible

from system.registry import option_converter_registry

class QuantityOptionConverter(OptionConvertible):
    async def to_options(self, interaction: discord.Interaction, data_name: str = None) -> list[discord.SelectOption]:

        quantity_data = [
            {
                "label": "1 個",
                "value": "1",
            },
            {
                "label": "5 個",
                "value": "5",
            },
            {
                "label": "10 個",
                "value": "10",
            },
            {
                "label": "20 個",
                "value": "20",
            },
            {
                "label": "50 個",
                "value": "50",
            },
            {
                "label": "100 個",
                "value": "100",
            },
        ]
        
        options = []
        
        for quantity in quantity_data:
            option = discord.SelectOption(
                label=quantity["label"],
                value=quantity["value"],
            )
            options.append(option)

        return options

