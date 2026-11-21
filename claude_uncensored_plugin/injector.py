"""Prompt injector — rewrites request payloads with active profile rules."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .profiles import Profile, Rule


@dataclass
class InjectorResult:
    modified: bool
    applied: list[str]


class PromptInjector:
    """Applies regex-based rules to system/messages fields without mutating input."""

    def apply(self, payload: dict[str, Any], profile: Profile) -> dict[str, Any]:
        out = {k: (v if not isinstance(v, str) else v) for k, v in payload.items()}
        hits: list[str] = []

        for rule in profile.rules:
            target = rule.field
            if target not in out:
                continue
            value = out[target]
            if isinstance(value, str):
                new_value = self._apply_rule(value, rule)
                if new_value != value:
                    hits.append(rule.id)
                    out[target] = new_value
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, dict) and "content" in item:
                        item = {**item, "content": self._apply_rule(str(item["content"]), rule)}
                    new_list.append(item)
                out[target] = new_list

        if hits and profile.prepend_system:
            out.setdefault("system", "")
            out["system"] = f"{profile.prepend_system}\n\n{out['system']}".strip()

        return out

    def _apply_rule(self, text: str, rule: Rule) -> str:
        try:
            pattern = re.compile(rule.pattern, re.IGNORECASE | re.MULTILINE)
        except re.error:
            return text
        return pattern.sub(rule.replacement, text)