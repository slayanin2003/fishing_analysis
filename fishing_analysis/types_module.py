from dataclasses import dataclass, field


@dataclass
class UserRequest:
    ip: str
    url: str
    valid: int = field(default_factory=int)