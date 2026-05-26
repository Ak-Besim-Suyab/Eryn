from abc import ABC

class Query(ABC): ...

class SelectOptionQuery(Query):
    def __init__(self, custom_id: str):
        self.custom_id = custom_id
    