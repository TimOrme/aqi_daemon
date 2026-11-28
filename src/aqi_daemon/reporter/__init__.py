from dataclasses import dataclass
from enum import Enum
from typing import Protocol, Set


@dataclass(frozen=True)
class ReadReport:
    """A raw read from an AQI device."""

    pmtwofive: float | None = None
    pmten: float| None = None
    ground_level_ozone: float | None = None
    carbon_monoxide: float | None = None
    sulfur_dioxide: float | None = None
    nitrogen_dioxide: float | None = None

class ReaderStatus(Enum):
    IDLE = 0
    WARMING_UP = 1
    READING = 2
    ERRORING = 3

class Reporter(Protocol):
    def report_read(self, read: ReadReport):
        pass

    def report_status(self, status: ReaderStatus):
        pass

    def report_error(self, msg: str, error: Exception):
        pass
