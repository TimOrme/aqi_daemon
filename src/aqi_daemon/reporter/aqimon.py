import requests
from requests import HTTPError, RequestException

from aqi_daemon.reporter import ReadReport, ReaderStatus

import logging

LOG = logging.getLogger(__name__)

class AqiMonReporter:

    def __init__(self, url: str):
        self.url: str = url
        self.device_id: str | None = None

    def register_device(self, device_name: str):
        requests.post(self.url + "/register", json={
            "device_name": device_name
        })

    def report_read(self, read: ReadReport):
        try:
            response = requests.post(self.url + "/read", json={
                "pmten": read.pmten,
                "pmtwofive": read.pmtwofive,
                "carbon_monoxide": read.carbon_monoxide,
                "ground_level_ozone": read.ground_level_ozone,
                "nitrogen_dioxide": read.nitrogen_dioxide,
                "sulfur_dioxide": read.sulfur_dioxide
            })

            response.raise_for_status()
        except RequestException as e:
            LOG.error(e)


    def report_status(self, status: ReaderStatus):
        try:
            response = requests.post(self.url + "/status", json={
                "status": status.name
            })
            response.raise_for_status()
        except RequestException as e:
            LOG.error(e)

    def report_error(self, msg: str, error: Exception):
        try:
            response = requests.post(self.url + "/error", json={
                "msg": msg,
                "error": str(error)
            })
            response.raise_for_status()
        except RequestException as e:
            LOG.error(e)