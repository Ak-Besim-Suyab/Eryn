"""
這個類別是全域的事件發布、訂閱總線
其他類別會實作打包資料的事件 (event) 並發布 (publish) 至感興趣的監聽者 (listener)
"""
import inspect
from typing import Callable
from data.schema.event import Event

__all__ = ["subscribe", "publish"]

class EventBus:
    def __init__(self):
        self._listeners: dict[tuple[Event, str], list[Callable]] = {}

    def subscribe(self, event_type: Event, event_name: str, listener: Callable):
        self._listeners.setdefault((event_type, event_name), []).append(listener)

    async def publish(self, event: Event, event_name: str = ""):
        for listener in self._listeners.get((type(event), event_name), []):
            if inspect.iscoroutinefunction(listener):
                await listener(event)
            else:
                listener(event)

_instance = EventBus()
subscribe = _instance.subscribe
publish = _instance.publish