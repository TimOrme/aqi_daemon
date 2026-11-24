import time

import schedule

from aqi_daemon.config import get_config_from_env, Config
from aqi_daemon.read import Reader, AqiRead
from aqi_daemon.read.mock import MockReader
from aqi_daemon.read.novapm import OpinionatedReader
from aqi_daemon.reporter import Reporter

class ReportingReader:
    def __init__(self, reader: Reader, reporter: Reporter) -> None:
        self.reader = reader
        self.reporter = reporter

    def read(self) -> AqiRead:
        try:
            # Set the approximate time of the next read
            result: AqiRead = self.reader.read()
        except Exception as e:
            self.reporter.report_error("Failed to retrieve data from reader", e)

def build_reader(conf: Config) -> Reader:
    """Retrieve the reader class.

    Uses LRU cache to simulate a singleton.
    """
    if conf.reader_type == "MOCK":
        return MockReader()
    elif conf.reader_type == "NOVAPM":
        return OpinionatedReader(
                ser_dev=conf.usb_path,
                warm_up_secs=conf.warm_up_sec,
                iterations=conf.sample_count_per_read,
                sleep_time=conf.sleep_sec_between_reads,
                command_wait_time=conf.command_wait_time,
        )
    else:
        raise Exception("Invalid reader type specified")

async def read_from_device(reader: Reader, reporter: Reporter) -> None:
    "Background cron task to read from the device."""

    try:
        # Set the approximate time of the next read
        result: AqiRead = reader.read()
    except Exception as e:
        reporter.report_error("Failed to retrieve data from reader", e)


if __name__ == '__main__':
    config = get_config_from_env()
    schedule.every(config.poll_frequency_sec).seconds.do(read_from_device)

    while True:
        schedule.run_pending()
        time.sleep(1)