"""
設定指定玩家的屬性數值
"""
from data.enums import AttributeName
from lib import attribute

PLAYER_ID = 1184440057596235817
ATTRIBUTE_ID = AttributeName.PERCEPTION
VALUE = 20

if __name__ == "__main__":
    success = attribute.set(PLAYER_ID, ATTRIBUTE_ID, VALUE)
    current = attribute.get(PLAYER_ID, ATTRIBUTE_ID)
    print(f"設定結果：{success}（玩家 {PLAYER_ID} 的 {ATTRIBUTE_ID} = {current}）")
