import md5
import datetime
import csv
import requests
import zipfile
from StringIO import StringIO

from Malcom.model.datatypes import Url
from Malcom.feeds.core import Feed


class Alexa(Feed):
    """
    This is a feed that will fetch data from a Alexa's top 1M
    """
    def __init__(self):
        super(Alexa, self).__init__(run_every="12h")

        self.source = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
        self.description = "This feed contains Alexa's top 1M domains"

    def update(self):
        r = requests.get(self.source)
        z = zipfile.ZipFile(StringIO(r.content))
        lines = z.read('top-1m.csv').split('\n')

        for line in lines:
            num, domain = line.split(',')
            if int(num) > 10000:
                break
            self.analyze(domain)

    def analyze(self, domain):

        d = self.model.get(value=domain)
        if d:
            d['tags'].append("alexa_1m")
            self.model.save(d)
