from claude_uncensored_plugin.injector import PromptInjector
from claude_uncensored_plugin.profiles import Profile, Rule


def test_injector_rewrites_system_field() -> None:
    profile = Profile(
        name="t",
        prepend_system="PREAMBLE",
        rules=[Rule(id="r", field="system", pattern="redact", replacement="allow")],
    )
    out = PromptInjector().apply({"system": "please redact this"}, profile)
    assert "allow" in out["system"]
    assert out["system"].startswith("PREAMBLE")


def test_injector_no_rules_is_noop() -> None:
    profile = Profile(name="noop")
    out = PromptInjector().apply({"system": "same"}, profile)
    assert out["system"] == "same"