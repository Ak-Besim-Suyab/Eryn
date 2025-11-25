import discord

from context import Context

from data.command import CommandType

from ui.views.about_bot_view import AboutBotView

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

        page1 = discord.Embed(
            title="Eryn Bot — 說明（1/2）",
            description=(
                "Eryn 是一個以採集、挖掘、技能、動物馴養為核心的 Discord RPG Bot。\n"
                "本 Bot 使用 Python + SQLite + discord.py 製作，採用模組化架構與可擴充的 JSON / 資料庫系統。"
            ),
            color=discord.Color.teal()
        )
        page1.set_footer(text="本訊息只有你能看見")
        page1.set_thumbnail(url=interaction.user.display_avatar.url)

        page2 = discord.Embed(
            title="Eryn Bot — 專案資訊（2/2）",
            description=(
                "GitHub 專案：\n"
                "<https://github.com/Ak-Besim-Suyab/Eryn>\n\n"
                "你可以在那裡查看最新程式碼、架構、模組、遊戲資料。"
            ),
            color=discord.Color.teal()
        )
        page2.set_footer(text="本訊息只有你能看見")

        pages = [page1, page2]

        view = AboutBotView(pages)

        await interaction.response.send_message(
            embed=pages[0],
            view=view,
            ephemeral=True
        )