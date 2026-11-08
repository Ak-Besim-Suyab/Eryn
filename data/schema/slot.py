from dataclasses import dataclass

@dataclass
class Slot:
    """
    id    : 欄位識別碼, 用於內部邏輯
    serial: 欄位編號, 用於排序顯示
    name  : 欄位名稱, 用於介面顯示
    """
    id: str
    serial: int
    name: str