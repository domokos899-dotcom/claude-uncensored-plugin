"""Quick smoke test used by CI to verify profile loading and injection."""
from __future__ import annotations

import json
from pathlib import Path

from claude_uncensored_plugin.injector import PromptInjector
from claude_uncensored_plugin.profiles import Profile, Rule


def main() -> int:
    profile = Profile(
        name="smoke",
        rules=[Rule(id="r1", field="content", pattern="hello", replacement="hi")],
    )
    result = PromptInjector().apply({"content": "hello world"}, profile)
    assert result["content"] == "hi world", result
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())