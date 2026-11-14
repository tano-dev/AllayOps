"""Linear-scan Drain Log Parser for Minecraft server logs & crash reports."""

from __future__ import annotations

import re
from dataclasses import dataclass

_IP_RE = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?\b")
_UUID_RE = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
)
_HEX_RE = re.compile(r"\b0x[0-9a-fA-F]+\b")
_NUM_RE = re.compile(r"\b-?\d+(?:\.\d+)?\b")


@dataclass
class LogTemplate:
    """Clustered log template with occurrence count."""

    template: str
    count: int = 1


class DrainLogParser:
    """Compresses repetitive Minecraft logs into parameterized templates."""

    def __init__(self, similarity_threshold: float = 0.5) -> None:
        self.similarity_threshold = similarity_threshold
        self.log_groups: dict[str, LogTemplate] = {}

    @staticmethod
    def preprocess(line: str) -> str:
        """Mask dynamic literals (IPs, UUIDs, hex addresses, numbers)."""
        masked = _IP_RE.sub("<IP>", line.strip())
        masked = _UUID_RE.sub("<UUID>", masked)
        masked = _HEX_RE.sub("<HEX>", masked)
        masked = _NUM_RE.sub("<NUM>", masked)
        return masked

    def parse(self, line: str) -> str:
        """Assign a log line to an existing template or create a new one."""
        cleaned = self.preprocess(line)
        if not cleaned:
            return ""
        tokens = cleaned.split()
        best_key: str | None = None
        best_sim = -1.0

        for key, group in self.log_groups.items():
            tmpl_tokens = group.template.split()
            if len(tmpl_tokens) != len(tokens):
                continue
            matches = sum(1 for a, b in zip(tokens, tmpl_tokens, strict=True) if a == b)
            sim = matches / max(len(tokens), 1)
            if sim >= self.similarity_threshold and sim > best_sim:
                best_sim = sim
                best_key = key

        if best_key is not None:
            group = self.log_groups[best_key]
            merged = [
                a if a == b else "<*>"
                for a, b in zip(tokens, group.template.split(), strict=True)
            ]
            group.template = " ".join(merged)
            group.count += 1
            return group.template

        self.log_groups[cleaned] = LogTemplate(template=cleaned, count=1)
        return cleaned

    def summarize_for_llm(self, lines: list[str], max_templates: int = 20) -> list[str]:
        """Parse a batch of raw log lines and return top compressed templates."""
        for line in lines:
            self.parse(line)
        sorted_groups = sorted(
            self.log_groups.values(), key=lambda g: g.count, reverse=True
        )[:max_templates]
        return [f"[x{g.count}] {g.template}" for g in sorted_groups]
