"""Pure counting logic for wc-cli.

This module owns the counting semantics (lines, words, characters) and the
table rendering.  It performs no I/O beyond reading the files it is given,
so it can be unit-tested without the CLI layer.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FileStats:
    """Statistics of a single text file."""

    file: str
    lines: int
    words: int
    chars: int


class FileReadError(OSError):
    """A file could not be read: missing path, directory, or non-UTF-8 content."""

    def __init__(self, *, path: Path, reason: str) -> None:
        """Create the error.

        :param path: path that could not be read.
        :param reason: short human-readable description of the cause.
        """
        super().__init__(f"{path}: {reason}")
        self.path = path
        self.reason = reason


def count_file(path: Path) -> FileStats:
    """Count lines, words and characters of one text file.

    Lines: every ``\\n`` plus one final unterminated line.
    Words: split on any whitespace.
    Characters: Unicode code points.
    Decoding: strict ``utf-8-sig`` (a leading BOM is stripped).

    :param path: path of the file to count.
    :return: statistics with the file name in the ``file`` field.
    :raises FileReadError: if the path is a directory, missing, or not UTF-8.
    """
    try:
        if path.is_dir():
            raise FileReadError(path=path, reason="is a directory")
        raw = path.read_bytes()
    except FileReadError:
        raise
    except FileNotFoundError as error:
        raise FileReadError(path=path, reason="no such file") from error
    except OSError as error:
        raise FileReadError(path=path, reason=f"read error: {error}") from error
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise FileReadError(path=path, reason="not valid UTF-8") from error
    return _stats_for(path, content)


def _stats_for(path: Path, content: str) -> FileStats:
    """Build statistics from already decoded file content.

    :param path: source path, used only for the file name.
    :param content: decoded file text.
    :return: the per-file statistics.
    """
    newlines = content.count("\n")
    lines = newlines + (1 if content and not content.endswith("\n") else 0)
    return FileStats(
        file=path.name,
        lines=lines,
        words=len(content.split()),
        chars=len(content),
    )


def summarize(stats: Sequence[FileStats]) -> FileStats:
    """Aggregate per-file statistics into a single total row.

    :param stats: per-file statistics, in output order (may be empty).
    :return: a :class:`FileStats` with ``file`` set to ``"total"`` and summed counts.
    """
    return FileStats(
        file="total",
        lines=sum(item.lines for item in stats),
        words=sum(item.words for item in stats),
        chars=sum(item.chars for item in stats),
    )


def render_table(stats: Sequence[FileStats]) -> str:
    """Render the per-file rows and the total as an aligned text table.

    The header is ``lines words chars file``; numeric columns are
    right-aligned, the file column left-aligned; an empty input renders
    only the header and a zero total row.  The result has no trailing
    newline.

    :param stats: per-file statistics, in output order.
    :return: the table as a single string.
    """
    rows = [*stats, summarize(stats)]
    widths = (
        max(len("lines"), *(len(str(row.lines)) for row in rows)),
        max(len("words"), *(len(str(row.words)) for row in rows)),
        max(len("chars"), *(len(str(row.chars)) for row in rows)),
    )
    lines = [f"{'lines':>{widths[0]}} {'words':>{widths[1]}} {'chars':>{widths[2]}} file"]
    for row in rows:
        lines.append(f"{row.lines:>{widths[0]}} {row.words:>{widths[1]}} {row.chars:>{widths[2]}} {row.file}")
    return "\n".join(lines)
