"""
這個類別用於定義載荷 (payload) 的資料結構，載荷是事件 (event) 發布時會攜帶的資料物件，包含玩家資訊、事件訊息等。
載荷的結構會根據事件類型而有所不同，例如行動事件 (ActionEvent) 可能包含目標玩家的資訊，而獎勵事件 (RewardEvent) 則可能包含獎勵的數值。
由於 Discord 的互動元件幾乎都會有使用者主體，因此載荷中通常會包含玩家的 ID 和名稱，以便在事件處理時能夠識別是哪位玩家觸發了事件。
"""

from dataclasses import dataclass, asdict

@dataclass
class Message:
    title: str = None

@dataclass
class Payload:
    user_id: int = None
    user_name: str = None 
    message: Message = None

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class ActionPayload(Payload):
    success: bool = False
    target_id: int = None
    target_name: str = None
    reward: RewardPayload = None

@dataclass
class RewardPayload(Payload):
    experience: int = 0
    currency: int = 0

@dataclass
class DailyRewardPayload(RewardPayload):
    total_daily_claims: int = 0