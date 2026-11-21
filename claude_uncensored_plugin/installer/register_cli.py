"""CLI wrapper so bootstrap.ps1 can shell into installer.register."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .register import install_plugin, uninstall_plugin


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install-dir", type=Path)
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args(argv)
    if args.uninstall:
        return 0 if uninstall_plugin() else 1
    if not args.install_dir:
        parser.error("--install-dir required for install")
    return 0 if install_plugin(args.install_dir) else 1


if __name__ == "__main__":
    sys.exit(main())