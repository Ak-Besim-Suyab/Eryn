"""
這個類別是全域的事件發布、訂閱總線
其他類別會實作打包資料的事件 (event) 並發布 (publish) 至感興趣的監聽者 (listener)
"""
import inspect
from typing import Callable, Any

class EventBus:
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
                if inspect.iscoroutinefunction(listener):
                    await listener(event)
                else:
                    listener(event)

_instance = EventBus()
subscribe = _instance.subscribe
publish = _instance.publish