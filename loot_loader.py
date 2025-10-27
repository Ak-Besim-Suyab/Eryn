import json

class LootLoader:
    #--- 讀取資料表
    def load(self, file_path):
        path = f"{file_path}.json"
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
                print(f'Error cause: {e}')