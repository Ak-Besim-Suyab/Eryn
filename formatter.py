class Formatter:
    def __init__(self, schemas: dict):
        self.schemas = schemas

    def format(self, event_type, data):
        if event_type not in self.schemas:
            raise ValueError(f"[Formatter] 未註冊的事件類型: {event_type}")

        schema = self.schemas[event_type]
        expected_keys = schema.get("expected_keys", {})
        for i, entry in enumerate(data):
            # 檢測欄位跟型別
            for key, tp in expected_keys.items():
                if key not in entry:
                    raise KeyError(f"[Formatter] 第 {i+1} 筆缺少欄位 {key} ({event_type.name})")
                if not isinstance(entry[key], tp):
                    raise TypeError(f"[Formatter] 第 {i+1} 筆欄位 {key} 類型錯誤，需 {tp.__name__}，得 {type(entry[key]).__name__}")

        line_template = schema["line_template"]
        lines = [line_template.format(**entry) for entry in data]

        field_name = schema["field_name"]
        value = "\n".join(lines)
        inline = schema["inline"]

        return field_name, value, inline