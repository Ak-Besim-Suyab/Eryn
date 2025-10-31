#--- State 是用於表示當前訊息的一個類別
#--- 因為 Discord 文字遊戲理論上應為靜態顯示，在使用者交互前不需要時刻監控當前狀態
#--- 目前僅有導入時間系統時可能會需要實作 interrupted() 用於中斷當前狀態時的處理
#--- 否則正常情況下理應只需要調用 start() 即表示完成進入該狀態時的運算

class State:
    async def start(self):
        pass

    async def interrupted(self):
        pass