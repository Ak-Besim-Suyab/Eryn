from models.inventory import Inventory
from models.skill import SkillContainer

from context import Context

class Player:
	def __init__(self, ID: int, name: str):
		self.ID = ID
		self.name = name
		self.gold = 0
		self.turn = 0
		self.location = 'forest'

		self.inventory = Inventory(ID)
		self.skill = SkillContainer(ID)

		self.restore_data()

	def __repr__(self):
		return f"<Player {self.name} {self.ID}>"

	def restore_data(self):
		data_manager = Context.get_manager("data")
		data_manager.load_player_data(self)

	def update(self):
		# data in models.player.py
		player_data = {
			"name": self.name,
			"gold": self.gold,
			"turn": self.turn,
			"location": self.location
		}

		skill_data = {}
		skills = Context.get_skill_entry()
		for name in skills:
			skill_data[f"{name}_level"] = getattr(self.skill, name).level
			skill_data[f"{name}_experience"] = getattr(self.skill, name).experience

		data_manager = Context.get_manager("data")
		data_manager.save_data("players", self.ID, player_data)
		data_manager.save_data("skills", self.ID, skill_data)
		data_manager.save_data("items", self.ID, self.inventory.items)