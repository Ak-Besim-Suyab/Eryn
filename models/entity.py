from context import Context

class Entity:
	def __init__(self, ID: str, name: str, level=1):
		self.ID = ID
		self.name = name
		self.level = level
		self.image = ""

class EntityContainer:
	def __init__(self):
		self.entitites: dict[str, Entity] = {}

	def register(self):
		data_entity = Context.loader.load("data/entities")

		for ID, data in data_entity.items():
			self.entitites[ID] = Entity(ID=ID, name=data["name"], level=data["level"])

	def get_entity(self, entity_name: str) -> Entity:
		return self.entitites[entity_name]

	def get_all(self):
		return self.entitites