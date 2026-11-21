"""Minimal overlay window to toggle profiles and inject request fixtures."""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk

from ..plugin_core import UncensoredPlugin


class OverlayWindow:
    def __init__(self, plugin: UncensoredPlugin) -> None:
        self.plugin = plugin
        self.root = tk.Tk()
        self.root.title("Claude Uncensored Plugin — Control")
        self.root.geometry("420x260")
        self._build()

    def _build(self) -> None:
        ttk.Label(self.root, text="Active profile:").pack(anchor="w", padx=10, pady=4)
        self.var = tk.StringVar(value=self.plugin.active_profile or "")
        combo = ttk.Combobox(self.root, textvariable=self.var, values=list(self.plugin.registry.names()))
        combo.pack(fill="x", padx=10)
        ttk.Button(self.root, text="Activate", command=self._activate).pack(pady=6)
        self.log = tk.Text(self.root, height=8)
        self.log.pack(fill="both", expand=True, padx=10, pady=6)

    def _activate(self) -> None:
        try:
            result = self.plugin.activate(self.var.get())
            self.log.insert("end", f"[ok] {result}\n")
        except KeyError as exc:
            self.log.insert("end", f"[err] {exc}\n")

    def run(self) -> None:
        self.root.mainloop()


def launch_overlay(plugin: UncensoredPlugin) -> threading.Thread:
    window = OverlayWindow(plugin)
    thread = threading.Thread(target=window.run, daemon=True)
    thread.start()
    return thread