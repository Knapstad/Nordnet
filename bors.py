import requests
import json
from bs4 import BeautifulSoup as BS
from io import StringIO


class NordnetUser:

    def __init__(self, user: str= None, password: str = None):
        self.user = user
        self.password = password
        self.session = requests.Session()
        self.api_url = "https://next.nordnet.no/api/2/"
        self.proxies = proxies = json.load(open("config_.json","r"))["proxies"]
        self.data ={"batch":""}



    def login(self) :
        """Takes self.user and self.password and creates a logged inn session at next.nordnet.no
        finds nessecary session auth tags and cookies"""
        url = "https://www.nordnet.no/api/2/login/anonymous"
        url2 = "https://www.nordnet.no/api/2/authentication/basic/login"
        payload = dict(username = self.user, password = self.password)
        ntag1= self.session.post(url, proxies=self.proxies, verify=False).headers["ntag"]
        log = self.session.post(url2, data= payload, headers= {"Referer": "https://www.nordnet.no/mux/login/start.html?state=signi"},
                                proxies=self.proxies, verify=False)
        self.session.get("https://next.nordnet.no", proxies=self.proxies, verify=False)
        self.next = self.session.cookies.get("NEXT", domain="next.nordnet.no")
        self.ntag = log.headers["ntag"]
        self.ntag1 = ntag1
        self.header = {"Cookie": "NEXT="+self.next, "client-id": "NEXT"}
        return log
    def set_header(self, head: dict):
        """Setts self.header to given argument"""
        self.header = head

    def accounts(self) -> list:
        """Finds and returnes a list of account dictionaries"""
        req = self.session.get(self.api_url + "accounts/", proxies=self.proxies, verify=False, headers=self.header,
                               data=self.data )
        req = json.load(StringIO(req.text))
        self.number_of_accounts = len(req)
        return req


#class instruments(nnuser):
   # def __init__(self):
        #nnuser.__innit__(self, user: str= None, password: str = None)
