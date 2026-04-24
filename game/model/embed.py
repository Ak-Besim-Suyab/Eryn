from dataclasses import dataclass, field

@dataclass
class Author:
    name: str = ""
    icon_url: str = ""

@dataclass
class Field:
    name: str = ""
    value: str = ""
    inline: bool = False

@dataclass
class Embed:
    title: str = ""
    description: str | None = None
    color: str | None = None
    thumbnail: str | None = None
    image: str | None = None
    author: Author | None = None

    fields: list[Field] = field(default_factory = list)

    def __post_init__(self):
        if self.author and isinstance(self.author, dict):
            self.author = Author(**self.author)

        if self.fields and isinstance(self.fields, list) and isinstance(self.fields[0], dict):
            self.fields = [Field(**f) for f in self.fields]