import yaml

class YamlLoader:
    #--- 讀取資料表
    def load(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
                print(f'Error cause: {e}')
                raise