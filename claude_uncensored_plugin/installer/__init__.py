"""Installer helpers for wiring the plugin into the desktop runtime."""
from .register import install_plugin, uninstall_plugin

__all__ = ["install_plugin", "uninstall_plugin"]