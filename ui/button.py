import discord

from context import Context

from data.command import CommandType

    # label: button name on message.
    # style: button color, see note for more info.
    # custom_id: button keyword.
    # callback: function to invoked.

    # thread:
    # create button -> set callback -> add to view -> message(view=view)

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

#-----------------------------------
# normal button
#-----------------------------------

class AboutBotButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="關於 Eryn",
            style=discord.ButtonStyle.secondary,
            custom_id="about_bot"
        )

    async def callback(self, interaction: discord.Interaction):
        # 如果你要自訂內容，這裡之後再改就好
        text = (
            "**Eryn Discord Bot**\n"
            "由 Python + SQLite + Discord.py 構成的遊戲系統。\n\n"
            "功能：挖礦、採集、馴養、技能、事件、背包 UI...\n"
            "GitHub：<https://github.com/Ak-Besim-Suyab/Eryn>\n\n"
            "本訊息僅你可見。"
        )
        await interaction.response.send_message(text, ephemeral=True)
