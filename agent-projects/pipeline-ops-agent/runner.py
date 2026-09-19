"""A small plugin-driven, read-only pipeline investigation workbench."""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "sample_data"
PLUGINS = ROOT / "plugins"


def load_plugins(directory: Path = PLUGINS) -> dict[str, tuple[dict, object]]:
    """Load only packaged plugins with a simple, validated manifest."""
    loaded = {}
    for manifest_file in sorted(directory.glob("*/manifest.json")):
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        name = manifest.get("name")
        fields = manifest.get("inputs")
        if not isinstance(name, str) or not name.isidentifier() or name in loaded:
            raise ValueError(f"Invalid or repeated plugin name in {manifest_file}")
        if not isinstance(fields, list) or any(not isinstance(field, str) or not field.isidentifier() for field in fields):
            raise ValueError(f"Invalid inputs for {name}")
        module_path = manifest_file.with_name("tool.py")
        if not module_path.is_file():
            raise ValueError(f"Missing tool.py for {name}")
        spec = importlib.util.spec_from_file_location(f"lab_{name}", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not callable(getattr(module, "run", None)):
            raise ValueError(f"Plugin {name} must define run")
        loaded[name] = (manifest, module.run)
    return loaded


def run_tool(name: str, arguments: dict, directory: Path = PLUGINS) -> dict:
    plugins = load_plugins(directory)
    if name not in plugins:
        raise ValueError(f"Unknown tool: {name}")
    manifest, function = plugins[name]
    expected = set(manifest["inputs"])
    if set(arguments) != expected:
        raise ValueError(f"Expected arguments: {sorted(expected)}")
    result = function(**arguments)
    return {"tool": name, "arguments": arguments, "result": result}


def read_records(filename: str, required: set[str]) -> list[dict[str, str]]:
    # Only packaged fixture names can be selected: no user-supplied filesystem paths.
    if filename not in {"runs.csv", "checks.csv"}:
        raise ValueError("Unknown sample dataset")
    with (DATA / filename).open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("Sample dataset is missing required columns")
        return list(reader)
