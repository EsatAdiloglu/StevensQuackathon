from typing import NamedTuple

class Flag(NamedTuple):
    id: int | None
    report_id: int | None
    source: str
    fr: int
    to: int
    reason: str

class _RawRecord(NamedTuple):
    id: int
    sender: str
    recipient: str
    body: str
    flags: list[Flag]

class Record(NamedTuple):
    id: int
    sender: str
    recipient: str
    body: str
    flags: list[Flag]