import requests
import os


class DeviceNotFoundError(Exception):
    pass


class ServerError(Exception):
    pass


class SessionNotFoundError(Exception):
    pass


class InvalidAuthCredentialsError(Exception):
    pass


class Config:
    def __init__(self, config=None):
        self.baseUrl = ""
        self.username = ""
        self.password = ""
        self.token = ""

        if config is not None:
            if "baseUrl" in config:
                self.baseUrl = config["baseUrl"]

            if "username" in config:
                self.username = config["username"]

            if "password" in config:
                self.password = config["password"]

            if "token" in config:
                self.token = config["token"]


class Client:
    def __init__(self, config):
        self.config = config

    def list_device_apps(self, deviceId):
        r = requests.get(
            "{baseUrl}/devices/{deviceId}/apps".format(
                baseUrl=self.config.baseUrl, deviceId=deviceId
            )
        )
        if r.status_code == 404:
            raise DeviceNotFoundError()
        apps = r.json()
        return apps

    def get_device(self, deviceId):
        r = requests.get(
            "{baseUrl}/devices/{deviceId}".format(
                baseUrl=self.config.baseUrl, deviceId=deviceId
            )
        )
        if r.status_code == 404:
            raise DeviceNotFoundError()
        device = r.json()
        return device

    def list_devices(self):
        r = requests.get("{baseUrl}/devices".format(baseUrl=self.config.baseUrl))
        devices = r.json()
        return devices

    def start_session(self, deviceId, appId, autoSync=False):
        passOrToken = self.config.password
        useToken = False

        if self.config.token:
            passOrToken = self.config.token
            useToken = True

        requestBody = {
            "deviceId": deviceId,
            "appId": appId,
            "username": self.config.username,
            "passOrToken": passOrToken,
            "useToken": useToken,
            "autoSync": autoSync,
        }
        r = requests.post(
            "{baseUrl}/sessions".format(baseUrl=self.config.baseUrl), json=requestBody
        )
        if r.status_code == 500:
            raise ServerError()

        if r.status_code == 401:
            raise InvalidAuthCredentialsError()

        session = r.json()
        return session

    def stop_session(self, sessionId):
        r = requests.get(
            "{baseUrl}/sessions/{sessionId}/stop".format(
                baseUrl=self.config.baseUrl, sessionId=sessionId
            )
        )
        if r.status_code == 404:
            raise SessionNotFoundError()
        return

    def sync(self):
        r = requests.post("{baseUrl}/sessions/sync".format(baseUrl=self.config.baseUrl))
        return


class ClientFactory:
    def create(self, config=None):
        if config == None:
            config = Config()

        if os.environ.get("GBA_BASE_URL"):
            config.baseUrl = os.environ.get("GBA_BASE_URL")

        if os.environ.get("GBA_USERNAME"):
            config.username = os.environ.get("GBA_USERNAME")

        if os.environ.get("GBA_PASSWORD"):
            config.password = os.environ.get("GBA_PASSWORD")

        if os.environ.get("GBA_TOKEN"):
            config.token = os.environ.get("GBA_TOKEN")

        return Client(config)
