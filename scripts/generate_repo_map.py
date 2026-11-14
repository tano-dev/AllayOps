"""Generate a lightweight repository map (docs/architecture/repo_map.json).

Inspired by Safe-Agentic-DataOps's CodeGraph AST indexer, this script gives AI
agents a fast, single-file index of tracked files, Python symbols, and key
entry points so they do not waste context scanning the whole tree.
"""

from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs" / "architecture" / "repo_map.json"


def _tracked_files() -> list[str]:
    """Return git-tracked files, falling back to a filtered walk if needed."""
    try:
        out = subprocess.check_output(
            ["git", "ls-files"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        )
        files = [line.strip() for line in out.splitlines() if line.strip()]
        if files:
            return sorted(files)
    except Exception:
        pass

    ignored = {
        ".git",
        ".fabric",
        "world",
        "logs",
        "crash-reports",
        "libraries",
        "versions",
        "__pycache__",
        ".venv",
        "node_modules",
    }
    collected: list[str] = []
    for path in ROOT.rglob("*"):
        if path.is_file() and not any(part in ignored for part in path.parts):
            collected.append(path.relative_to(ROOT).as_posix())
    return sorted(collected)


def _extract_python_symbols(rel_path: str) -> dict[str, list[str]]:
    """Extract top-level classes and functions from a Python file."""
    try:
        tree = ast.parse((ROOT / rel_path).read_text(encoding="utf-8"))
    except Exception:
        return {"classes": [], "functions": []}

    classes = [
        node.name for node in tree.body if isinstance(node, ast.ClassDef)
    ]
    functions = [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    return {"classes": classes, "functions": functions}


def build_repo_map() -> dict:
    """Build the structured repository map dictionary."""
    files = _tracked_files()
    python_symbols = {
        f: _extract_python_symbols(f) for f in files if f.endswith(".py")
    }
    return {
        "project": "AllayOps",
        "file_count": len(files),
        "files": files,
        "python_symbols": python_symbols,
    }


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    repo_map = build_repo_map()
    OUTPUT.write_text(json.dumps(repo_map, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)} ({repo_map['file_count']} files)")


if __name__ == "__main__":
    main()
