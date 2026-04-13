from typing import Callable, Any

class Listener:
    def __init__(self):
        self._listeners: dict[type, list[Callable]] = {}

    def subscribe(self, event_type: type, listener: Callable):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    async def publish(self, event: Any):
        event_type = type(event)
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                await listener(event)

_instance = Listener()
subscribe = _instance.subscribe
publish = _instance.publish