from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Insight:
    title: str
    content: str
    category: str
    embedding: Optional[List[float]] = field(default=None)
    id: Optional[int] = None
