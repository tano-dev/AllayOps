"""Direct Preference Optimization (DPO) triplet logger for AllayOps."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from shared_interfaces.schemas import DPOPreferencePair


class DPOPreferenceLogger:
    """Appends (x, y_w, y_l) preference triplets to JSONL for offline alignment."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path

    def log_pair(
        self,
        incident_id: str,
        prompt: str,
        chosen: dict[str, Any],
        rejected: dict[str, Any],
        source: str,
    ) -> DPOPreferencePair:
        """Persist a DPO preference triplet."""
        pair = DPOPreferencePair(
            incident_id=incident_id,
            prompt=prompt,
            chosen=chosen,
            rejected=rejected,
            source=source,
        )
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(pair)) + "\n")
        return pair
