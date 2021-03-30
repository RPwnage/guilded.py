import requests
import json
from guilded.endpoints import endpoints


class GuildedAccount:
    def __init__(self, email, password):
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.session_cookies = None
        self.headers = None
        if self.login() == False:
            raise Exception('Authentication with given email/password failed')

    def accountDetails(self):
        request = self.session.get(str(endpoints.mainApiURL + str(endpoints.userDetailEndpoint).format(userid=self.user_id)),
                                   headers=self.headers, cookies=self.session_cookies)
        return (request.json())

    def login(self):
        request = self.session.post(str(endpoints.mainApiURL + endpoints.loginEndpoint),
                                    data=json.dumps({
                                        "email": self.email,
                                        "password": self.password,
                                        "getMe": True
                                    }), headers={"Content-Type": "application/json"}, cookies=self.session_cookies)

        if request.status_code == 200:
            self.user_id = request.json()["user"]["id"]
            self.subdomain = request.json()["user"]["subdomain"]
            return True
        return False

    def createAccount(self, email, password, username):
        headers = self.headers
        headers["Content-Type"] = "application/json"
        request = self.session.post((str(endpoints.mainApiURL) + "/users?type=email"),
                                    data=json.dumps({
                                        "extraInfo": {
                                            "platform": "desktop"
                                        },
                                        "name": str(username),
                                        "email": str(email),
                                        "password": str(password),
                                        "fullName": str(username)
                                    }))

        try:
            if request.json()["user"]["name"] == username:
                self.session_cookies = request.cookies
                self.user_id = request.json()["user"]["id"]
                return True
            elif request.status_code != 200:
                return False
        except:
            pass
        return False
