from cores import AssetRegistry

class MessageRegistry(AssetRegistry):
    def __init__(self):
        super().__init__(
            path = "assets/messages"
        )

# singleton declaration has moved to __init__.py