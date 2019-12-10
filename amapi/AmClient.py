import requests
import json
import sys
import datetime as dt

class AmClient:
    URL_BASE = 'https://marketplace.atlassian.com'
    HTTP_CONTENT_HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def __init__(self, username=None, password=None, verbosity=0):
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.verbosity = verbosity

    def get(self, path, parms=None):
        url = AmClient.URL_BASE + path
        if self.verbosity>1:
            for k, v in parms.items():
                log_url = log_url + '&' + str(k) + '=' + str(v)
            print(log_url)
        if ((self.username is not None) and (self.password is not None)):
            result = self.session.get(url, params=parms, auth=(self.username, self.password))
        else:
            result = self.session.get(url, params=parms)
        if result.status_code != 200:
            print(result.status_code)
            print(result.text)
            sys.exit()
        return result