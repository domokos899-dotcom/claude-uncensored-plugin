"""Profile registry and rule models for the uncensored plugin."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True)
class Rule:
    id: str
    field: str
    pattern: str
    replacement: str


@dataclass(frozen=True)
class Profile:
    name: str
    description: str = ""
    prepend_system: str = ""
    rules: list[Rule] = field(default_factory=list)


class ProfileRegistry:
    def __init__(self, profiles: dict[str, Profile]) -> None:
        self._profiles = profiles

    @classmethod
    def from_file(cls, path: Path) -> "ProfileRegistry":
        if not path.exists():
            return cls({})
        raw = json.loads(path.read_text(encoding="utf-8"))
        profiles: dict[str, Profile] = {}
        for entry in raw.get("profiles", []):
            rules = [Rule(**r) for r in entry.get("rules", [])]
            profile = Profile(
                name=entry["name"],
                description=entry.get("description", ""),
                prepend_system=entry.get("prepend_system", ""),
                rules=rules,
            )
            profiles[profile.name] = profile
        return cls(profiles)

    def get(self, name: str) -> Profile | None:
        return self._profiles.get(name)

    def names(self) -> Iterator[str]:
        return iter(self._profiles.keys())