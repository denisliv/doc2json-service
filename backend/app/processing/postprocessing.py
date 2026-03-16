"""Plugin registry: load and apply postprocessors from plugins/ directory."""

import importlib.util
import logging
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)


def _plugins_dir() -> Path:
    return Path(settings.PLUGINS_DIR)


def load_plugin(name: str):
    """Load a plugin module by filename (without .py)."""
    path = _plugins_dir() / f"{name}.py"
    if not path.exists():
        raise FileNotFoundError(f"Plugin not found: {name}")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "process") or not callable(module.process):
        raise ValueError(f"Plugin {name} is missing a callable 'process' function")
    return module


def apply_postprocessors(names: list[str], data, context: dict):
    """Apply a chain of postprocessors sequentially."""
    for name in names:
        try:
            plugin = load_plugin(name)
            data = plugin.process(data, **context)
        except Exception:
            logger.exception("Postprocessor '%s' failed", name)
    return data


def list_available_plugins() -> list[dict]:
    """Return list of available plugins for UI."""
    plugins = []
    plugins_dir = _plugins_dir()
    if not plugins_dir.exists():
        return plugins
    for path in sorted(plugins_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        try:
            module = load_plugin(path.stem)
            plugins.append({
                "name": path.stem,
                "type": getattr(module, "PLUGIN_TYPE", "unknown"),
                "description": (module.__doc__ or "").strip(),
            })
        except Exception:
            logger.warning("Could not load plugin %s", path.stem)
    return plugins
