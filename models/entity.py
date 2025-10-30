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
		entity_data = Context.loader.load("data/entities")

		for uid, data in entity_data.items():
			self.entitites[uid] = Entity(uid=uid, name=data.get("name"), level=data.get("level"))

	def get_entity(self, uid: str) -> Entity:
		return self.entitites[uid]

	def get_all(self) -> dict[str, Entity]:
		return self.entitites