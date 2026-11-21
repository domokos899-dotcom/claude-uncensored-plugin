from pathlib import Path

from claude_uncensored_plugin.profiles import ProfileRegistry


def test_load_from_fixture(tmp_path: Path) -> None:
    fixture = tmp_path / "profiles.json"
    fixture.write_text(
        '{"profiles":[{"name":"x","rules":[{"id":"a","field":"system","pattern":"foo","replacement":"bar"}]}]}',
        encoding="utf-8",
    )
    registry = ProfileRegistry.from_file(fixture)
    profile = registry.get("x")
    assert profile is not None
    assert profile.rules[0].id == "a"


def test_missing_file_returns_empty(tmp_path: Path) -> None:
    registry = ProfileRegistry.from_file(tmp_path / "nope.json")
    assert list(registry.names()) == []