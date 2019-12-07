import requests
import json


class rbtvConfig(object):
    def __init__(self, app_id="kid_r1n7bbVzW", app_secret="8713e20822c043adb3a6c23783e1e33b", user=""):
        self.app_id = app_id
        self.app_secret = app_secret
        self.user = user
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "android-kinvey-http/2.10.11"})

    def app_login(self, username="", password=""):
        if not self.user:
            login_data = json.dumps({"username": username, "password": password})
            login_url = "https://baas.kinvey.com/user/{0}".format(self.app_id)
            r = self.s.post(login_url, data=login_data, headers={"Content-Type": "application/json"}, auth=(self.app_id, self.app_secret))
            self.user = r.json()
        else:
            user_url = "https://baas.kinvey.com/user/{0}/{1}".format(self.app_id, self.user["_id"])
            r = self.s.get(user_url, headers={"Authorization": "Kinvey {0}".format(self.user["_kmd"]["authtoken"]), "Content-Type": "application/json"})
        return self.user

    def get_data(self, data="AppConfigBeta"):
        if not self.user:
            self.app_login()
        data_url = "https://baas.kinvey.com/appdata/{0}/{1}".format(self.app_id, data)
        r = self.s.get(data_url, headers={"Authorization": "Kinvey {0}".format(self.user["_kmd"]["authtoken"]), "Content-Type": "application/json"})
        return r.json()
