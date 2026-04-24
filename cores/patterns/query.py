from typing import Callable

from game import model

class Query:
    """
    .. Description::
        以下類別已應用查詢總線
        - `ask` :class:`game.ui.select`
        - `register` :class:`system.handlers.option_trasformer`

    .. Note::
        方法內包含對重複註冊的檢查, 如果重複註冊將彈出錯誤
    """
    def __init__(self):
        self._handlers: dict[str, Callable] = {}

    def register(self, query: model.Query, handler: Callable):
        """
        .. Description::
            `query`
                為查詢類別, 該類別應該繼承自 `model.Query`，並且攜帶必要的參數以供 `handler` 使用
            `handler` 
                為處理函式, 該函式接受與 `query` 類別對應的參數並返回結果
        """
        if query in self._handlers:
            raise ValueError(f"已存在名為 {query} 的查詢，無法重複註冊")
        self._handlers[query] = handler

    def ask(self, query: model.Query, *args, **kwargs):
        query_type = type(query)
        handler = self._handlers.get(query_type)
        if not handler:
            raise ValueError(f"找不到名為 {query_type.__name__} 的查詢")
        return handler(query, *args, **kwargs)

# singleton declaration ---------------------------------------
_instance = Query()
register = _instance.register
ask = _instance.ask