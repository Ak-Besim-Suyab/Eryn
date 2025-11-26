import discord

from context import Context

from data.command import CommandType

from ui.views.about_bot_view import AboutBotView

class ButtonManager:
    def __init__(self):
        self.registry = {
            CommandType.COMBAT: CombatButton,
            CommandType.RETURN: ReturnButton,
        }

        self.registry["about_bot"] = AboutBotButton

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
        self.player_manager = Context.get_manager("player")
        self.state_machine = Context.state_machine
        super().__init__(label = "戰鬥", style = discord.ButtonStyle.primary, custom_id = CommandType.COMBAT)

    async def callback(self, interaction: discord.Interaction):
        player = self.player_manager.get_player(interaction)
        combat_state = self.state_machine.create("combat", interaction)

        getattr(self.view, "target", None)
        if self.view.target:
            await combat_state.start(self.view.target)
        else:
            print("[ButtonContainer] Target not found, Need to fix.")
            return

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