import discord
from game import model
from game import ui
from systems import sessions

class View(discord.ui.View):
    """
    Note: 
        視圖物件 (View) 應當只作為資料載體。
        在整個對話生命週期，只有該視圖可以向下傳遞，目前最好的做法應是將週期內需要使用的會話物件 (Session) 保存在該視圖裡。
        週期內的資料與邏輯皆由會話管理，視圖僅負責保存、輸出與傳遞。
    """
    def __init__(self, model: model.View, session: sessions.DialogueSession):

        self.model = model
        self.session = session

        super().__init__(timeout=model.timeout)

        if model.buttons:
            for button in model.buttons:
                btn = ui.Button(button)
                self.add_item(btn)
        
        if model.selects:
            for select in model.selects:
                sel = ui.Select(select)
                self.add_item(sel)