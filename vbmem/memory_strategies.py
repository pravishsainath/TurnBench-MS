from __future__ import annotations

import json
from typing import Any, Dict

from vbmem.turnbench_belief_tracker import TurnBenchBeliefTracker


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


class VerifiedBeliefMemoryStrategy(MemoryStrategy):
    def __init__(self) -> None:
        self.tracker: TurnBenchBeliefTracker | None = None

    def on_game_start(self, game: Any) -> None:
        self.tracker = TurnBenchBeliefTracker(game.setup.setup_id)

    def on_observation(self, obs: Any) -> None:
        if not self.tracker:
            return
        self.tracker.update(obs["verifier_id"], obs["guess_code"], obs["result"])

    def build_memory_text(self) -> str:
        if not self.tracker:
            return "{}"
        return json.dumps(self.tracker.to_dict(), ensure_ascii=False, indent=2)


class BeliefPromptUnverifiedStrategy(MemoryStrategy):
    def __init__(self) -> None:
        self.observations: list[Dict[str, Any]] = []

    def on_observation(self, obs: Any) -> None:
        self.observations.append(obs)

    def build_memory_text(self) -> str:
        return json.dumps({"observations": self.observations}, ensure_ascii=False)


def create_memory_strategy(name: str) -> MemoryStrategy:
    normalized = (name or "full_history").lower()
    if normalized == "verified_belief_memory":
        return VerifiedBeliefMemoryStrategy()
    if normalized == "belief_prompt_unverified":
        return BeliefPromptUnverifiedStrategy()
    return FullHistoryStrategy()
