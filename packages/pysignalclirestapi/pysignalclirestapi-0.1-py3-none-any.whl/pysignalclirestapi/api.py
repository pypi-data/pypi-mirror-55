"""SignalCliRestApi Python library."""

import base64
import requests

class SignalCliRestApiError(Exception):
    """SignalCliRestApiError base classi."""
    pass

class SignalCliRestApi(object):
    """SignalCliRestApi implementation."""
    def __init__(self, base_url, number, api_version=1):
        """Initialize the class."""
        super(SignalCliRestApi, object).__init__()
        self._api_version = api_version
        self._base_url = base_url
        self._number = number

        if self._api_version > 1:
            raise SignalCliRestApiError("api version not supported!")

    def send_message(self, message, recipients, filename=None):
        """Send a message to one (or more) recipients.
         
        Additionally a file can be attached.
        """
        url = self._base_url + "/" + str(self._api_version)
        data = {
            "message": message,
            "number": self._number,
            "recipients": recipients,
        }

        if filename is not None:
            with open(filename, "rb") as ofile:
                data["base64_attachment"] = base64.b64encode(ofile.read())
        resp = requests.post(url+"/send", json=data)
        if resp.status_code != 201:
            json_resp = resp.json()
            if "error" in json_resp:
                raise SignalCliRestApiError(json_resp["error"])
            raise SignalCliRestApiError("unknown error while sending signal message")
