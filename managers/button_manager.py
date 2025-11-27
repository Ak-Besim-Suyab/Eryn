class ButtonManager:
    def __init__(self):
        self._registry = {}

    """register button"""
    def register(self, name: str, button_class):
        self._registry[name] = button_class

    """create button object"""
    def create(self, name: str, *args, **kwargs):
        cls = self._registry.get(name)
        if cls is None:
            raise ValueError(f"Button '{name}' not be registered.")
        return cls(*args, **kwargs)

    """list all buttons"""
    def list_buttons(self):
        return list(self._registry.keys())