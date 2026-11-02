from pydantic import BaseModel, Field
from typing import Literal, Optional

class Request(BaseModel):
    budget: int = Field(gt=0, le=100000000)
    purpose: Literal["game", "dev", "ai", "creative", "office", "daily"]
    resolution: Literal["1080p", "1440p", "4K"] = "1080p"
    cpu_preference: Literal["Intel", "AMD", "any"] = "any"
    gpu_preference: Literal["NVIDIA", "AMD", "any"] = "any"
    memory: Literal[16, 32, 64] = 32
    storage: Literal[500, 1000, 2000] = 1000
    include: list[str] = []
    game: Optional[str] = None
    notes: Optional[str] = None

