
from pydantic import BaseModel
from typing import List, Dict


class Bar(BaseModel):
    time: float
    close: float
    high: float
    low: float
    _open: float
    volume: float