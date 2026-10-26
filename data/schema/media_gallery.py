from dataclasses import dataclass, field

@dataclass
class MediaGalleryItem:
    media: str
    description: str = None
    spoiler: bool = False

@dataclass
class MediaGallery:
    type: str = "media_gallery"
    items: list[MediaGalleryItem] = field(default_factory=list)

    def __post_init__(self):
        if self.items and isinstance(self.items, list):
            for index, data in enumerate(self.items):
                if not isinstance(data, dict):
                    raise ValueError(f"components[{index}] 的資料必須為字典類型, 收到錯誤類型: {type(data)}")

                self.items[index] = MediaGalleryItem(**data)