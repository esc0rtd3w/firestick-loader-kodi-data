import pyamf
from pyamf import remoting
from pyamf.flex import messaging
import requests
import json


class lntvConfig(object):
    def __init__(self):
        self.url = "https://api.backendless.com/762F7A10-3072-016F-FF64-33280EE6EC00/E9A27666-CD62-10CD-FF05-ED45B12ABE00/binary"
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTT Build/LVY48F)"})

    def get_data(self):
        data = {
            "clientId": None,
            "destination": "GenericDestination",
            "correlationId": None,
            "source": "com.backendless.services.persistence.PersistenceService",
            "operation": "first",
            "messageRefType": None,
            "headers": {"application-type": "ANDROID", "api-version": "1.0"},
            "timestamp": 0,
            "body": ["ConfigCharlie"],
            "timeToLive": 0,
            "messageId": None,
        }
        msg = messaging.RemotingMessage(**data)
        req = remoting.Request(target="null", body=[msg])
        ev = remoting.Envelope(pyamf.AMF3)
        ev["null"] = req
        resp = requests.post(self.url, data=remoting.encode(ev).getvalue(), headers={"Content-Type": "application/x-amf"})
        resp_msg = remoting.decode(resp.content)
        config = json.dumps(resp_msg.bodies[0][1].body.body, default=lambda obj: repr(obj))
        return json.loads(config)
