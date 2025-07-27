from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NewsItem:
    """Represents a single F1 news item."""
    title: str
    content: str
    url: str
    source: str
    author: Optional[str] = None
    timestamp: Optional[datetime] = None
    tags: Optional[list] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class RaceResult:
    """Represents a race result for a driver."""
    position: int
    driver: str
    team: str
    time: str
    points: int
    fastest_lap: str = ""


@dataclass
class RaceResults:
    """Represents complete race results."""
    race_name: str
    date: datetime
    circuit: str
    results: list[RaceResult]