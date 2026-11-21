"""Windows named-pipe bridge — talks to the browser extension shim."""
from __future__ import annotations

import json
import sys
from typing import Any


class NamedPipeBridge:
    PIPE_NAME = r"\\.\pipe\claude_uncensored_plugin"

    def __init__(self, pipe_name: str = PIPE_NAME) -> None:
        self.pipe_name = pipe_name
        self._handle: Any = None

    def connect(self, timeout_ms: int = 2000) -> bool:
        if sys.platform != "win32":
            raise OSError("named pipe bridge is Windows-only")
        import win32file  # type: ignore
        import pywintypes  # type: ignore

        try:
            self._handle = win32file.CreateFile(
                self.pipe_name,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None,
            )
            return True
        except pywintypes.error:
            return False

    def send(self, message: dict[str, Any]) -> None:
        if self._handle is None:
            raise RuntimeError("bridge not connected")
        import win32file  # type: ignore

        payload = (json.dumps(message) + "\n").encode("utf-8")
        win32file.WriteFile(self._handle, payload)