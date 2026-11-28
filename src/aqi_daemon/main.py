import sys
import time

import schedule

from aqi_daemon.config import get_config_from_env, Config
from aqi_daemon.read import Reader, AqiRead
from aqi_daemon.read.mock import MockReader
from aqi_daemon.read.novapm import OpinionatedReader
from aqi_daemon.reporter import Reporter, ReadReport
from aqi_daemon.reporter.aqimon import AqiMonReporter

import logging

LOG = logging.getLogger(__name__)


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

def build_reader(conf: Config, reporter: Reporter) -> Reader:
    """Retrieve the reader class.

    Uses LRU cache to simulate a singleton.
    """
    if conf.reader_type == "MOCK":
        return MockReader()
    elif conf.reader_type == "NOVAPM":
        return OpinionatedReader(
                ser_dev=conf.usb_path,
                on_status_change=lambda x: reporter.report_status(x),
                warm_up_secs=conf.warm_up_sec,
                iterations=conf.sample_count_per_read,
                sleep_time=conf.sleep_sec_between_reads,
                command_wait_time=conf.command_wait_time,
        )
    else:
        raise Exception("Invalid reader type specified")

def read_from_device(reader: Reader, reporter: Reporter) -> None:
    "Background cron task to read from the device."""

    try:
        # Set the approximate time of the next read
        LOG.info("Reading...")
        result = reader.read()
        reporter.report_read(ReadReport(pmten=result.pmten, pmtwofive=result.pmtwofive))
    except Exception as e:
        reporter.report_error("Failed to retrieve data from reader", e)


def start():
    config = get_config_from_env()

    logging.basicConfig(level=logging.INFO)

    if config.aqimon_url is None:
        sys.exit("You must set an aqimon URL.")

    reporter = AqiMonReporter(url=config.aqimon_url)
    LOG.info("Configured reporter at %s", config.aqimon_url)

    reader = build_reader(config, reporter)
    LOG.info("Configured reader.")

    schedule.every(config.poll_frequency_sec).seconds.do(lambda: read_from_device(reader, reporter))
    LOG.info("Beginning polling every %s seconds", config.poll_frequency_sec)


    while True:
        schedule.run_pending()
        time.sleep(1)