from cores import AssetRegistry

from game import model

class MessageRegistry(AssetRegistry[model.Message]):
    def __init__(self):
        super().__init__(
            model=model.Message, 
            path = "assets/messages"
        )

# singleton declaration has moved to __init__.py