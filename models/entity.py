from context import Context

class Entity:
	def __init__(self, uid: str, name: str, level=1):
		self.uid = uid
		self.name = name
		self.level = level
		self.image = "❓"

class EntityContainer:
	def __init__(self):
		self.entitites: dict[str, Entity] = {}

	def register(self):
		data_entity = Context.loader.load("data/entities")

		for uid, data in data_entity.items():
			self.entitites[uid] = Entity(uid=uid, name=data["name"], level=data["level"])

	def get_entity(self, uid: str) -> Entity:
		return self.entitites[uid]

	def get_all(self):
		return self.entitites