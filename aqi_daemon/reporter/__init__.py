from dataclasses import dataclass
from enum import Enum
from typing import Protocol


@dataclass(frozen=True)
class ReadReport:
    """A raw read from an AQI device."""

    pmtwofive: float | None
    pmten: float| None
    ground_level_ozone: float | None
    carbon_monoxide: float | None
    sulfur_dioxide: float | None
    nitrogen_dioxide: float | None

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