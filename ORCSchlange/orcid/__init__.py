from requests import Session
from ORCSchlange.config import Config
import pybtex.database
from ORCSchlange.bib import Date, WorkSummary


class OrcID:
    def __init__(self, orcid, start, stop):
        self.id = orcid
        self.start = Date(*start.split("-"))
        self.stop = Date(*stop.split("-"))

    def get_id(self):
        return "-".join([self.id[4 * i: 4 * (i + 1)] for i in range(4)])

    def __str__(self):
        return self.get_id() + ": " + str(self.start) + " - " + str(self.stop)


def get_date(d):
    return Date(d["year"]["value"], d["month"]["value"] if d["month"] else None,
                d["day"]["value"] if d["day"] else None)


class API:
    def __init__(self):
        self.authurl = Config().auth
        self.baseurl = Config().api
        self.s = Session()
        self.s.headers = {'Accept': 'application/json'}
        data = {"grant_type": "client_credentials", "scope": "/read-public", "client_id": Config().client_id,
                "client_secret": Config().client_secret}
        r = self.s.request(method="post", url=self.authurl, data=data)
        self.s.headers = {'Accept': 'application/json', "Access token": r.json()["access_token"]}

    def get_worksums(self, orcid):
        r = self.s.request(method="get", url="{0}/{1}/works".format(self.baseurl, orcid.get_id()))
        for work in (w["work-summary"][0] for w in r.json()["group"]):
            if work["publication-date"] is not None:
                d = get_date(work["publication-date"])
                if orcid.start <= d <= orcid.stop:
                    yield WorkSummary(work["path"], work["title"]["title"]["value"], d)

    def get_work(self, summary):
        r = self.s.request(method="get", url=self.baseurl + summary.path)
        json = r.json()
        if json['citation'] is not None:
            if json['citation']['citation-type'] == "BIBTEX":
                return pybtex.database.parse_string(json['citation']['citation-value'], "bibtex")
        return None
