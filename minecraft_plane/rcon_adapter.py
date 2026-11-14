"""Safe RCON / Console Adapter for executing validated AllayOps actions."""

from __future__ import annotations

from dataclasses import dataclass

from shared_interfaces.schemas import ActionProposal


@dataclass(frozen=True)
class CommandExecutionResult:
    """Result of executing (or dry-running) a Minecraft server command."""

    success: bool
    command: str
    response: str
    dry_run: bool


class SafeRconAdapter:
    """Translates whitelisted ActionProposals into bounded Minecraft commands.

    By default `dry_run=True` so tests and chaos benchmarks never mutate a live
    server unless explicitly configured with live RCON credentials.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 25575, dry_run: bool = True) -> None:
        self.host = host
        self.port = port
        self.dry_run = dry_run
        self.executed_history: list[CommandExecutionResult] = []

    def translate_action(self, proposal: ActionProposal) -> str:
        """Map a whitelisted ActionProposal to a deterministic Minecraft command."""
        action = proposal.action_type
        params = proposal.parameters

        mapping: dict[str, str] = {
            "save_all": "save-all flush",
            "tick_freeze": "tick freeze",
            "tick_unfreeze": "tick unfreeze",
            "say_alert": f"say [AllayOps] {params.get('message', 'Automated health notice')}",
            "clear_tnt_bounded": (
                f"kill @e[type=minecraft:tnt,distance=..{int(params.get('radius', 32))}]"
            ),
            "clear_items_bounded": (
                f"kill @e[type=minecraft:item,distance=..{int(params.get('radius', 32))}]"
            ),
            "set_view_distance": f"say [AllayOps] Recommend view-distance={params.get('value', 8)}",
            "graceful_restart": "save-all flush",
        }
        if action not in mapping:
            raise ValueError(f"Unsupported action_type for RCON translation: {action}")
        return mapping[action]

    def execute(self, proposal: ActionProposal) -> CommandExecutionResult:
        """Execute (or dry-run) a translated Minecraft command."""
        cmd = self.translate_action(proposal)
        if self.dry_run:
            result = CommandExecutionResult(
                success=True,
                command=cmd,
                response=f"[DRY-RUN {self.host}:{self.port}] Executed: {cmd}",
                dry_run=True,
            )
            self.executed_history.append(result)
            return result

        # Live RCON socket integration point (e.g. via mcrcon when enabled)
        raise NotImplementedError(
            "Live RCON transport is disabled in skeleton mode. Enable mcrcon adapter when ready."
        )
