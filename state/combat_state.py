from state.state import State

from data.command import CommandType
from data.event import EventType

from ui.select import ActionSelect
from ui.views.base_view import BaseView
from ui.embed import EventEmbed

from context import Context

class CombatState(State):
    def __init__(self, interaction: object):
        self.state = 'combat'
        self.interaction = interaction
        self.player = Context.get_manager("player").get_player(interaction)
        self.target = None

    async def start(self, target):
        print(target)
        print(f"{self.interaction.user.display_name}'s combat start")
        self.target = target

        action = [{
            "action_id": "attack",
            "action_name": "攻擊",
        }]

        select = ActionSelect(state=self, entries=action)
        
        view = BaseView()
        view.add_item(select)

        embed = EventEmbed(CommandType.COMBAT, self.player)
        embed.set_description(target)

        await self.interaction.response.edit_message(embed=embed, view=view)

    async def attack(self, interaction):
        print("attack!")
        dealed_damage = self.player.damage
        self.target["health"] = self.target["health"] - self.player.damage

        if self.target["health"] <= 0:
            await self.end(interaction)
            return

        content = {
            "name": self.target["name"],
            "health": self.target["health"],
            "dealed_damage": dealed_damage,
        }

        embed = EventEmbed(CommandType.ATTACK, self.player)
        embed.set_description(content)

        action = [{
            "action_id": "attack",
            "action_name": "攻擊",
        }]

        select = ActionSelect(state=self, entries=action)

        view = BaseView()
        view.add_item(select)

        await interaction.response.edit_message(embed=embed, view=view)

    async def end(self, interaction):

        content = {
            "name": self.target["name"]
        }

        embed = EventEmbed(CommandType.VICTORY, self.player)
        embed.set_description(content)

        view = BaseView()

        await interaction.response.edit_message(embed=embed, view=view)