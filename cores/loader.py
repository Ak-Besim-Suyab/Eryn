import yaml
import json
from pathlib import Path

# YAML 讀取器
class YamlLoader:
    def load(self, file_path: str):
        resolved_path = resolve_file_path(file_path)
        try:
            with open(resolved_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f'Error: YAML file not found - {resolved_path}')
            return None
        except yaml.YAMLError:
            print(f'Error: Invalid YAML format - {resolved_path}')
            return None
        except Exception as e:
            print(f'Error loading YAML {resolved_path}: {e}')
            raise

# JSON 讀取器
class JsonLoader:
    def load(self, file_path: str):
        resolved_path = resolve_file_path(file_path)
        try:
            with open(resolved_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f'Error: JSON file not found - {resolved_path}')
            return None
        except json.JSONDecodeError:
            print(f'Error: Invalid JSON format - {resolved_path}')
            return None
        except Exception as e:
            print(f'Error loading JSON {resolved_path}: {e}')
            raise

# 這個方法用於解析檔案路徑
def resolve_file_path(file_path: str) -> Path:
    path = Path(file_path)
    
    # 如果已是絕對路徑，直接返回
    if path.is_absolute():
        return path
    
    # 相對路徑：相對於專案根目錄（即本檔案的上上層）
    project_root = Path(__file__).resolve().parent.parent
    return project_root / path