import discord

from context import Context

from state.combat_state import CombatState

from data.command import CommandType

    # label: button name on message.
    # style: button color, see note for more info.
    # custom_id: button keyword.
    # callback: function to invoked.

    # thread:
    # create button -> set callback -> add to view -> message(view=view)

class ButtonFactory:
    @staticmethod
    def create_button(label, style=discord.ButtonStyle.secondary, custom_id=None, callback=None):
        button = discord.ui.Button(
            label = label, 
            style = style, 
            custom_id = custom_id
        )

        if callback:
            button.callback = callback

        return button

class ButtonContainer:
    def __init__(self):
        self.buttons = {}

    def register(self):
        command_buttons = {
            CommandType.COMBAT: { 
                "label": "戰鬥", 
                "style": discord.ButtonStyle.primary, 
                "callback": self.callback_combat
            },
            CommandType.HOME: {
                "label": "返回",
                "style": discord.ButtonStyle.secondary, 
                "callback": self.callback_home
            },
        }

        for command_type, button_content in command_buttons.items():
            button = ButtonFactory.create_button(
                label=button_content["label"], 
                style=button_content["style"], 
                custom_id=command_type.value, 
                callback = button_content["callback"]
            )
            self.buttons[command_type] = button

    def get_button(self, command_type):
        return self.buttons[command_type]

    def get_all(self):
        return self.buttons

    async def callback_combat(self, interaction: discord.Interaction):
        print("hello!")

        player = Context.get_manager("player").get_player(interaction)
        combat = CombatState(interaction)

        player.state = combat.state
        await combat.start()

    async def callback_home(self, interaction: discord.Interaction):
        print("hello?")
        # player = Context.get_manager("player").get_player(interaction)
        # menu = MenuState()
        # player.state = menu.state
        # await menu.start()

class CombatButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label = "戰鬥", style = discord.ButtonStyle.primary, custom_id = "combat")
