"""Register/unregister the plugin via Windows registry (HKCU)."""
from __future__ import annotations

import sys
from pathlib import Path

REG_PATH = r"Software\ClaudeUncensoredPlugin"


def install_plugin(install_dir: Path) -> bool:
    if sys.platform != "win32":
        raise OSError("registry install is Windows-only")
    import winreg

    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE) as handle:
        winreg.SetValueEx(handle, "InstallDir", 0, winreg.REG_SZ, str(install_dir))
        winreg.SetValueEx(handle, "Version", 0, winreg.REG_SZ, "2.4.1")
    return key is not None


def uninstall_plugin() -> bool:
    if sys.platform != "win32":
        return False
    import winreg

    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        return True
    except FileNotFoundError:
        return False