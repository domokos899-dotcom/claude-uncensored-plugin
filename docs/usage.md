# Usage

```powershell
pip install -r requirements.txt
python -m claude_uncensored_plugin --profile default
```

Hotkey `Ctrl+Shift+U` opens the overlay. Profiles live in `config/profiles.json`;
each rule is `{id, field, pattern, replacement}` where `pattern` is a regex applied
case-insensitively to the named field (`system` or `content`).