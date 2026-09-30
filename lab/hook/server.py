#!/usr/bin/env python3
"""Loopback webhook catcher. Writes POST bodies and always returns 200."""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DATA = Path(os.environ.get("CATCHER_DATA", "/data"))
LAST = DATA / "last.json"
ALL = DATA / "all.jsonl"
DATA.mkdir(parents=True, exist_ok=True)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, content_type: str = "application/json") -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path in ("/health", "/", "/ready"):
            self._send(200, b'{"ok":true}')
            return
        if path in ("/last", "/hook"):
            if LAST.is_file():
                self._send(200, LAST.read_bytes())
            else:
                self._send(200, b"{}")
            return
        self._send(404, b'{"error":"not found"}')

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length > 0 else b""
        LAST.write_bytes(raw or b"{}")
        with ALL.open("ab") as fh:
            fh.write(raw.replace(b"\n", b" ") + b"\n")
        self._send(200, b'{"ok":true}')

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("hook " + (fmt % args) + "\n")


if __name__ == "__main__":
    host = os.environ.get("CATCHER_HOST", "0.0.0.0")
    port = int(os.environ.get("CATCHER_PORT", "8080"))
    print(f"hook listening {host}:{port}", flush=True)
    ThreadingHTTPServer((host, port), Handler).serve_forever()
