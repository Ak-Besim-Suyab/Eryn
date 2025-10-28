from context import Context

class Entity:
	def __init__(self, entity_id: str, entity_name: str, level=1):
		self.entity_id = entity_id
		self.entity_name = entity_name
		self.level = level
		self.image = "❓"

class EntityContainer:
	def __init__(self):
		self.entitites: dict[str, Entity] = {}

	def register(self):
		data_entity = Context.loader.load("data/entities")

		for entity_id, data in data_entity.items():
			self.entitites[entity_id] = Entity(entity_id=entity_id, entity_name=data["name"], level=data["level"])

	def get_entity(self, entity_id: str) -> Entity:
		return self.entitites[entity_id]

	def get_all(self):
		return self.entitites