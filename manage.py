#!/usr/bin/env python
"""Django command-line management entry point for the pandora project."""

from __future__ import annotations

import os
import sys


def main() -> None:
    """Run the Django management command passed on the command line."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise SystemExit("Django is not installed in this environment; run 'uv sync' first.") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
