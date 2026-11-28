"""Config module."""

import os.path
from dataclasses import dataclass



@dataclass(frozen=True)
class Config:
    """Config data for the application."""
    poll_frequency_sec: int

    reader_type: str

    # Nova PM properties
    usb_path: str
    sleep_sec_between_reads: int
    sample_count_per_read: int
    warm_up_sec: int
    command_wait_time: int

    # EPA Properties
    epa_lookback_minutes: int

    # Reporter properties
    reporter_type: str

    aqimon_url: str | None



DEFAULT_CONFIG = Config(
    poll_frequency_sec=60 * 15,  # Every 15 minutes
    epa_lookback_minutes=60 * 8,  # 8 hours
    reader_type="NOVAPM",
    usb_path="/dev/ttyUSB0",
    sleep_sec_between_reads=5,
    warm_up_sec=15,
    command_wait_time=1,
    sample_count_per_read=5,
    reporter_type="aqimon",
    aqimon_url=None
)


def get_config_from_env() -> Config:
    """Get the config from environment variables."""
    return Config(
        poll_frequency_sec=int(os.environ.get("AQIMON_POLL_FREQUENCY_SEC", DEFAULT_CONFIG.poll_frequency_sec)),
        reader_type=os.environ.get("AQIMON_READER_TYPE", DEFAULT_CONFIG.reader_type),
        usb_path=os.environ.get("AQIMON_USB_PATH", DEFAULT_CONFIG.usb_path),
        sleep_sec_between_reads=int(
            os.environ.get("AQIMON_SLEEP_SEC_BETWEEN_READS", DEFAULT_CONFIG.sleep_sec_between_reads)
        ),
        warm_up_sec=int(os.environ.get("AQIMON_WARM_UP_SEC", DEFAULT_CONFIG.warm_up_sec)),
        command_wait_time=int(os.environ.get("AQIMON_COMMAND_WAIT_TIME", DEFAULT_CONFIG.command_wait_time)),
        sample_count_per_read=int(os.environ.get("AQIMON_SAMPLE_COUNT_PER_READ", DEFAULT_CONFIG.sample_count_per_read)),
        epa_lookback_minutes=int(os.environ.get("AQIMON_EPA_LOOKBACK_MIN", DEFAULT_CONFIG.epa_lookback_minutes)),
        reporter_type=os.environ.get("AQID_REPORTER_TYPE", DEFAULT_CONFIG.reporter_type),
        aqimon_url=os.environ.get("AQID_AQIMON_URL", DEFAULT_CONFIG.aqimon_url),
    )
