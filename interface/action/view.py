from discord.ui import View
from .button import GardenButton

class GardenView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GardenButton())