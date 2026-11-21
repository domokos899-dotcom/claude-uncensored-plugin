"""Core runtime for the uncensored plugin: profile loading and patch application."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .injector import PromptInjector
from .profiles import ProfileRegistry


class UncensoredPlugin:
    """Orchestrates profile selection, injection, and context rewriting."""

    def __init__(self, config_path: Path | str = "config/profiles.json") -> None:
        self.config_path = Path(config_path)
        self.registry = ProfileRegistry.from_file(self.config_path)
        self.injector = PromptInjector()
        self.active_profile: str | None = None

    def activate(self, name: str) -> dict[str, Any]:
        profile = self.registry.get(name)
        if profile is None:
            raise KeyError(f"unknown profile: {name}")
        self.active_profile = name
        return {"active": name, "rules": len(profile.rules)}

    def rewrite_context(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self.active_profile is None:
            return payload
        profile = self.registry.get(self.active_profile)
        assert profile is not None
        return self.injector.apply(payload, profile)

    def status(self) -> dict[str, Any]:
        return {
            "version": __import__("claude_uncensored_plugin").__version__,
            "active_profile": self.active_profile,
            "loaded_profiles": list(self.registry.names()),
        }