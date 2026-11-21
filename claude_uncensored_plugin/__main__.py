"""Entry point: `python -m claude_uncensored_plugin`."""
from __future__ import annotations

import argparse
import sys

from .plugin_core import UncensoredPlugin


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="claude-uncensored-plugin")
    parser.add_argument("--profile", help="profile name to activate at startup")
    parser.add_argument("--config", default="config/profiles.json")
    parser.add_argument("--headless", action="store_true", help="skip overlay UI")
    args = parser.parse_args(argv)

    plugin = UncensoredPlugin(args.config)
    if args.profile:
        plugin.activate(args.profile)

    if not args.headless:
        from .overlay_ui import launch_overlay
        launch_overlay(plugin)

    print(plugin.status())
    return 0


if __name__ == "__main__":
    sys.exit(main())