import yaml
from os.path import expanduser
import datetime, time
import os


# TODO replace with something that is not dependent on the cli
class WeaviateAuth:

    def __init__(self, weaviateCLI):

        self.weaviateCliPath = weaviateCLI

        # Load data from weaviate.conf
        self.weaviateData = yaml.load(open(expanduser("~") + "/.weaviate.conf"), Loader=yaml.FullLoader)
        self.weaviateAuth = 1
        if 'auth' in self.weaviateData:
            self.weaviateAuth = self.weaviateData['auth']
            if self.weaviateData['auth'] != 1:
                self.weaviateExp = self.weaviateData['auth_expires']
                self.weaviateBearrer = self.weaviateData['auth_bearer']
        self.WEAVIATE_URL = self.weaviateData['url']

    # Get Epoch time for Bearer
    def _getEpochTime(self):
        dts = datetime.datetime.utcnow()
        return round(time.mktime(dts.timetuple()) + dts.microsecond/1e6)

    def getWeaviateURL(self):
        return self.WEAVIATE_URL

    def defineAuthHeader(self):
        # set headers
        if self.weaviateAuth == 2:
            header={'Content-type': 'application/json', 'Authorization': 'Bearer ' + self.weaviateBearrer}
            # Set Bearer
            if (self.weaviateExp - 2) < self._getEpochTime():
                print("BEARER EXPIRED, RESET")
                os.system(self.weaviateCliPath + "/weaviate-cli.py" + " ping")
                time.sleep(2)
                self.weaviateData = yaml.load(open(expanduser("~") + "/.weaviate.conf"))
                self.weaviateBearrer = self.weaviateData['auth_bearer']
                self.weaviateExp = self.weaviateData['auth_expires']
                header={'Content-type': 'application/json', 'Authorization': 'Bearer ' + self.weaviateBearrer}
        else:
            header={'Content-type': 'application/json'}

        return header
