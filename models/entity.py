from context import Context

class Entity:
	def __init__(self, 
		uid: str, 
		name: str, 
		level: int = 1, 
		health: int = 1
		):

		self.uid = uid
		self.name = name
		self.image = "❓"
		self.level = level
		self.health = health

	def to_dict(self):
		entity_dict = {
			"uid": self.uid,
			"name": self.name,
			"image": self.image,
			"level": self.level,
			"health": self.health,
		}
		return entity_dict

class EntityContainer:
	def __init__(self):
		self.entitites: dict[str, Entity] = {}

	def register(self):
		entity_data = Context.loader.load("data/entities")

		for uid, data in entity_data.items():
			self.entitites[uid] = Entity(
				uid=uid, 
				name=data.get("name"), 
				level=data.get("level"),
				health=data.get("health")
			)

	def get_entity(self, uid: str) -> Entity:
		return self.entitites[uid]

	def get_all(self) -> dict[str, Entity]:
		return self.entitites