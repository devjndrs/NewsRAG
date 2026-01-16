from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Insight:
    title: str
    content: str
    category: str
    url: Optional[str] = None
    embedding: Optional[List[float]] = field(default=None)
    relevance: Optional[str] = None
    id: Optional[int] = None
