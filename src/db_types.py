from typing import NamedTuple

class Flag(NamedTuple):
    id: int
    report_id: int
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