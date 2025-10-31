import discord

from context import Context

from state.state_machine import state_machine

from data.command import CommandType

    # label: button name on message.
    # style: button color, see note for more info.
    # custom_id: button keyword.
    # callback: function to invoked.

    # thread:
    # create button -> set callback -> add to view -> message(view=view)

class ButtonContainer:
    def __init__(self):
        self.registry = {
            CommandType.COMBAT: CombatButton,
            CommandType.RETURN: ReturnButton,
        }

    def get_button(self, command_type):
        button = self.registry.get(command_type)
        if not button:
            print(f"[ButtonContainer] Unregistered button type: {command_type}")
            return None

        return button()

    def get_all(self):
        return [cls() for cls in self.registry.values()]

class CombatButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label = "戰鬥", style = discord.ButtonStyle.primary, custom_id = CommandType.COMBAT)

    async def callback(self, interaction: discord.Interaction):
        print("hello!")

        player = Context.get_manager("player").get_player(interaction)
        combat_state = state_machine.create("combat", interaction)

        if self.view.target:
            target = self.view.target
        else:
            print("[ButtonContainer] Target not found, Need to fix.")
            return

        await combat_state.start(target)

class DialogueButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label = "對話", style = discord.ButtonStyle.primary, custom_id = CommandType.DIALOGUE)

    async def callback(self, interaction: discord.Interaction):
        print("this is dialogue button!")

class TameButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label = "馴服", style = discord.ButtonStyle.primary, custom_id = CommandType.TAME)

    async def callback(self, interaction: discord.Interaction):
        print("this is tame button!")

class ReturnButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label = "返回", style = discord.ButtonStyle.secondary, custom_id = CommandType.RETURN)

    async def callback(self, interaction: discord.Interaction):
        print("this is return button!")
        # player = Context.get_manager("player").get_player(interaction)
        # menu = MenuState()
        # player.state = menu.state
        # await menu.start()
