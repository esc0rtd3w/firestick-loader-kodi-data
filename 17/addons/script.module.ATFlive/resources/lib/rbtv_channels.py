import requests
import json
import string
import random
from base64 import b64decode


class rbtvChannels(object):
    def __init__(self, config, user=""):
        self.config = config
        self.user = user
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTT Build/LVY48F)"})

    @staticmethod
    def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))

    def register_user(self):
        user_url = b64decode(self.config[0]["YmFzZXVybG5ld3gw"][1:]).decode("utf-8") + "adduserinfo.nettv/"
        data = {"api_level": "19", "android_id": self.id_generator(16), "device_id": "unknown", "device_name": "AFTT", "version": "1.2 (30)"}
        headers = {
            "Referer": b64decode(self.config[0]["SXNpc2VrZWxvX3Nlc2lzdGltdV95ZXppbm9tYm9sbzAw"][1:]).decode("utf-8"),
            "Authorization": b64decode(self.config[0]["amFnX3Ryb3JfYXR0X2Vu"][1:]).decode("utf-8"),
        }
        r = self.s.post(user_url, headers=headers, data=data)
        self.user = str(r.json().get("user_id"))

    def get_channel_list(self):
        check = "1"
        if not self.user:
            self.register_user()
            check = "8"
        list_url = b64decode(self.config[0]["YmFzZXVybG5ld3gw"][1:]).decode("utf-8") + "redbox.tv/"
        data = {"check": check, "user_id": self.user, "version": "30"}
        headers = {
            "Referer": b64decode(self.config[0]["SXNpc2VrZWxvX3Nlc2lzdGltdV95ZXppbm9tYm9sbzAw"][1:]).decode("utf-8"),
            "Authorization": b64decode(self.config[0]["amFnX3Ryb3JfYXR0X2Vu"][1:]).decode("utf-8"),
        }
        r = self.s.post(list_url, headers=headers, data=data)
        return r.json()
