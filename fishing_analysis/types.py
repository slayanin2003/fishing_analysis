from dataclasses import dataclass


@dataclass
class UserRequest:
    ip: str
    url: str
    valid: int = field(default_factory=int)