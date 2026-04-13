from dataclasses import dataclass, asdict


@dataclass
class Message:
    title: str = None


@dataclass
class Payload:
    message: Message = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ActionPayload(Payload):
    sender_name: str = None
    target_name: str = None
    experience: int = None
    currency: int = None