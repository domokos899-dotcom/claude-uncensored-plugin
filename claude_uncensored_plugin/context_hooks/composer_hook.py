"""Hook that rewrites the composer textarea before submit."""
from __future__ import annotations

from typing import Any

from ..injector import PromptInjector
from ..profiles import Profile


class ComposerHook:
    def __init__(self, injector: PromptInjector) -> None:
        self.injector = injector

    def on_submit(self, text: str, profile: Profile | None) -> str:
        if profile is None:
            return text
        payload = {"content": text}
        result = self.injector.apply(payload, profile)
        return result.get("content", text)

    def before_send(self, message: dict[str, Any], profile: Profile | None) -> dict[str, Any]:
        if profile is None:
            return message
        return self.injector.apply(message, profile)