"""
該模組用於定義邏輯運行後送出的資料類別
"""
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class BaseResponse:
    """
    base payload class, only declare function transform fields to dict.
    """
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class PlayerResponse(BaseResponse):
    """
    該類別用於請求玩家資訊, 包含以下項目：

    .. `player_id` 為必須填入項目, 用於其他窗口查詢玩家。
    .. `player_name` 為選填項目, 用於對話中顯示玩家名稱。
    .. `player_icon_url` 為選填項目, 用於對話中顯示玩家頭像, 如果對話要求 author 時。
    """
    player_id: int
    player_name: str = None 
    player_icon_url: str = None

@dataclass(frozen=True)
class ShopResponse(PlayerResponse):
    """
    該類別用於請求商店互動結果

    .. `cost`: 通常是指總花費。
    .. `items`: 購買的物品清單，以 Item 物件的形式傳入。
    """
    cost: int = 0

@dataclass(frozen=True)
class ActionPayload(BaseResponse):
    success: bool = False
    target_id: int = None
    target_name: str = None
    reward: RewardPayload = None

@dataclass(frozen=True)
class RewardPayload(BaseResponse):
    experience: int = 0
    currency: int = 0

@dataclass(frozen=True)
class DailyRewardPayload(BaseResponse):
    total_daily_claims: int = 0