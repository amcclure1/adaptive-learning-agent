"""Injectable UTC timestamps and opaque identifiers."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta


class TimeAndIds:
    def __init__(self) -> None:
        self._last_time: datetime | None = None

    def timestamp(self, *, after: str | None = None) -> str:
        current = datetime.now(UTC)
        floor = self._last_time
        if after is not None:
            parsed = datetime.fromisoformat(after.replace("Z", "+00:00"))
            floor = max(floor, parsed) if floor is not None else parsed
        if floor is not None and current <= floor:
            current = floor + timedelta(microseconds=1)
        self._last_time = current
        return current.isoformat(timespec="microseconds").replace("+00:00", "Z")

    def identifier(self, prefix: str) -> str:
        return f"{prefix}-{uuid.uuid4().hex}"
