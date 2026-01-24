class EventManager:
    def __init__(self):
        self._listeners = {}
    
    def subscribe(self, event_type: str, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
    
    def post(self, event_type: str, **data):
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(**data)