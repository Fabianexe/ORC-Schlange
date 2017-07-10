import json
import ORCSchlange.sql


class Config:
    class __OnlyOne:
        def __init__(self, args):
            self.client_id = None
            self.client_secret = None
            self.api = None
            self.auth = None
            if args.config == 0:
                self.sandbox()
            elif args.config == 1:
                self.read_db(args.dbfile)
            elif isinstance(args.config, str):
                self.read_file(args.config)
            else:
                self.read_inline(*args.config)

        def sandbox(self):
            self.client_id = "APP-DZ4II2NELOUB89VC"
            self.client_secret = "c0a5796e-4ed3-494b-987e-827755174718"

            self.api = "https://pub.sandbox.orcid.org/v2.0"
            self.auth = "https://sandbox.orcid.org/oauth/token"

        def read_db(self, path):
            db = ORCSchlange.sql.DB(path)
            conf = db.read_config()
            db.close()
            self.api = conf[0]
            self.auth = conf[1]
            self.client_id = conf[2]
            self.client_secret = conf[3]

        def read_file(self, path):
            f = open(path)
            content = f.read()
            f.close()
            js = json.loads(content)
            self.client_id = js["client_id"]
            self.client_secret = js["client_secret"]
            self.auth = js["auth"] if "auth" in js else "https://orcid.org/oauth/token"
            self.api = js["api"] if "api" in js else "https://pub.orcid.org/v2.0/"

        def read_inline(self, clientid, secret):
            self.client_id = clientid
            self.client_secret = secret
            self.api = "https://orcid.org/oauth/token"
            self.auth = "https://pub.orcid.org/v2.0/"

        def __str__(self):
            return "{0} - {1}\n{2}\n{3}".format(self.client_id, self.client_secret, self.auth, self.api)

    instance = None

    def __init__(self, args=None):
        if not Config.instance:
            if args:
                Config.instance = Config.__OnlyOne(args)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self):
        return str(self.instance)
