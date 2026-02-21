from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class BeliefState:
    hypotheses: List[str]
    candidate_codes: List[str]
    notes: str = ""
    last_update_turn: int = -1
