from dataclasses import dataclass, field

import random

@dataclass
class Line:
    lines: list = field(default_factory=list)

    def random(self):
        return random.choice(self.lines)