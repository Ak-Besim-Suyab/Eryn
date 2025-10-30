from models.inventory import Inventory
from models.skill import SkillContainer

from context import Context

class Player:
	def __init__(self, uid: int, name: str):
		self.uid = uid
		self.name = name
		self.gold = 0
		self.turn = 0
		self.location = 'forest'
		self.state = 'home'

		self.inventory = Inventory(uid)
		self.skill = SkillContainer(uid)

		self.restore_data()

	def __repr__(self):
		return f"<Player {self.name} {self.uid}>"

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
		data_manager.save_data("players", self.uid, player_data)
		data_manager.save_data("skills", self.uid, skill_data)
		data_manager.save_data("items", self.uid, self.inventory.items)