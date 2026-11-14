"""Lightweight asynchronous-safe Control Bus connecting AllayOps planes."""

from __future__ import annotations

import json
from collections import deque
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from shared_interfaces.schemas import utc_now_iso


@dataclass(frozen=True)
class ControlEvent:
    """Envelope emitted onto the AllayOps Control Bus."""

    event_type: str
    source_plane: str
    payload: dict[str, Any]
    timestamp: str = field(default_factory=utc_now_iso)


class EventDrivenControlBus:
    """In-memory zero-drop ring buffer with optional JSONL audit persistence."""

    def __init__(self, max_buffer: int = 1000, audit_path: Path | None = None) -> None:
        self._buffer: deque[ControlEvent] = deque(maxlen=max_buffer)
        self._subscribers: dict[str, list[Callable[[ControlEvent], None]]] = {}
        self._audit_path = audit_path

    def subscribe(self, event_type: str, handler: Callable[[ControlEvent], None]) -> None:
        """Register a synchronous subscriber for a given event_type (or '*')."""
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event: ControlEvent) -> None:
        """Record an event in the ring buffer, persist if configured, and notify listeners."""
        self._buffer.append(event)
        if self._audit_path is not None:
            self._audit_path.parent.mkdir(parents=True, exist_ok=True)
            with self._audit_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(asdict(event)) + "\n")

        for handler in self._subscribers.get(event.event_type, []):
            handler(event)
        for handler in self._subscribers.get("*", []):
            handler(event)

    def recent_events(self, limit: int = 50) -> list[ControlEvent]:
        """Return up to `limit` most recent events."""
        if limit <= 0:
            return []
        return list(self._buffer)[-limit:]
