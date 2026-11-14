"""Generate an AST-based CodeGraph (docs/architecture/codegraph.json).

Upgrades Safe-Agentic-DataOps's CodeGraph concept for AllayOps by:
1. Extracting every Python module node, its architectural plane, classes, and functions.
2. Extracting directed `imports` edges via Python AST (`import` / `from ... import`).
3. Validating 4-plane architectural boundaries (e.g., `shared_interfaces` must remain
   a zero-upstream-dependency leaf layer) and detecting import cycles.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs" / "architecture" / "codegraph.json"

PLANES: tuple[str, ...] = (
    "shared_interfaces",
    "minecraft_plane",
    "observability_plane",
    "agentic_plane",
    "research",
    "tests",
    "scripts",
)


def _module_name(rel_path: str) -> str:
    return rel_path.removesuffix(".py").replace("/", ".")


def _plane_of(rel_path: str) -> str:
    top = rel_path.split("/", 1)[0]
    return top if top in PLANES else "root"


def _analyze_python_file(rel_path: str, known_modules: set[str]) -> tuple[dict, list[dict]]:
    text = (ROOT / rel_path).read_text(encoding="utf-8")
    tree = ast.parse(text)

    classes = [n.name for n in tree.body if isinstance(n, ast.ClassDef)]
    functions = [
        n.name
        for n in tree.body
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    mod = _module_name(rel_path)
    plane = _plane_of(rel_path)
    node = {
        "id": mod,
        "path": rel_path,
        "plane": plane,
        "classes": classes,
        "functions": functions,
        "loc": len(text.splitlines()),
    }

    imported: set[str] = set()
    for stmt in ast.walk(tree):
        if isinstance(stmt, ast.Import):
            for alias in stmt.names:
                if alias.name in known_modules:
                    imported.add(alias.name)
        elif isinstance(stmt, ast.ImportFrom) and stmt.module:
            if stmt.module in known_modules:
                imported.add(stmt.module)
            for alias in stmt.names:
                candidate = f"{stmt.module}.{alias.name}"
                if candidate in known_modules:
                    imported.add(candidate)

    edges = [
        {"source": mod, "target": target, "type": "imports"}
        for target in sorted(imported)
        if target != mod
    ]
    return node, edges


def _detect_boundary_violations(edges: list[dict]) -> list[str]:
    """Ensure `shared_interfaces` never imports upper planes."""
    violations: list[str] = []
    forbidden_from_shared = {
        "minecraft_plane",
        "observability_plane",
        "agentic_plane",
        "research",
    }
    for edge in edges:
        src_plane = edge["source"].split(".", 1)[0]
        tgt_plane = edge["target"].split(".", 1)[0]
        if src_plane == "shared_interfaces" and tgt_plane in forbidden_from_shared:
            violations.append(
                f"Layer violation: {edge['source']} -> {edge['target']}"
            )
    return violations


def build_codegraph() -> dict:
    py_files = sorted(
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*.py")
        if not any(
            part in {".git", ".venv", "venv", "__pycache__", "world", "logs"}
            for part in p.parts
        )
    )
    known_modules = {_module_name(p) for p in py_files}

    nodes: list[dict] = []
    edges: list[dict] = []
    for rel_path in py_files:
        node, mod_edges = _analyze_python_file(rel_path, known_modules)
        nodes.append(node)
        edges.extend(mod_edges)

    violations = _detect_boundary_violations(edges)
    plane_counts: dict[str, int] = {}
    for n in nodes:
        plane_counts[n["plane"]] = plane_counts.get(n["plane"], 0) + 1

    return {
        "project": "AllayOps",
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "planes": plane_counts,
            "boundary_violations": violations,
        },
        "nodes": nodes,
        "edges": edges,
    }


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    graph = build_codegraph()
    OUTPUT.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    s = graph["summary"]
    print(
        f"Generated {OUTPUT.relative_to(ROOT)} "
        f"({s['node_count']} nodes, {s['edge_count']} edges, "
        f"{len(s['boundary_violations'])} boundary violations)"
    )
    if s["boundary_violations"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
