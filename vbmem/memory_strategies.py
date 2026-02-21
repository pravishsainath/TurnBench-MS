from __future__ import annotations
from typing import Any, Dict


class MemoryStrategy:
    def on_game_start(self, game: Any) -> None:
        return

    def on_observation(self, obs: Any) -> None:
        return

    def build_memory_text(self) -> str:
        return ""

    def get_metrics_snapshot(self) -> Dict[str, Any]:
        return {}


class FullHistoryStrategy(MemoryStrategy):
    pass
