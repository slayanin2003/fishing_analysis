from dataclasses import dataclass, field


@dataclass
class UserRequest:
    ip: str
    url: str
    valid: int = field(default_factory=int)


@dataclass
class UserFishingStats:
    ip: str
    count_fishing_requests: int
