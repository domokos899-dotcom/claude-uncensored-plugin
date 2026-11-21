# Architecture

The plugin is a modular toolkit. Entry point `python -m claude_uncensored_plugin`
loads `config/profiles.json`, activates a profile, and exposes a Tkinter overlay
for toggling profiles at runtime.

- `plugin_core` — orchestrates profile selection + injection
- `injector` — applies regex rules to request payloads
- `profiles` — profile/rule dataclasses + JSON registry
- `context_hooks` — composer and system-prompt rewrite hooks
- `windows_bridge` — named-pipe transport to the browser extension shim
- `installer` — HKCU registry registration for the desktop runtime