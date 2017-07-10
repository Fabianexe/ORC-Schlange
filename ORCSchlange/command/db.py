import sys
from ORCSchlange.command import BaseReporter


def check_date(d):
    return len(d) != 10 or len(d.split("-")) != 3 or not d.split("-")[0].isdecimal() \
           or not d.split("-")[1].isdecimal() or not d.split("-")[2].isdecimal()


class DBReporeter(BaseReporter):
    def add(self):
        self.open()
        self.debug("Validate orchid")
        self.args.orchid = self.args.orchid.replace("-", "")
        if len(self.args.orchid) != 16:
            self.error("Invalide orchid")
            self.close()
            sys.exit(1)
        self.debug("Validate start")
        if check_date(self.args.start):
            self.error("Invalide start")
            self.close()
            sys.exit(1)
        if self.args.stop:
            self.debug("Stop found")
            self.debug("Validate stop")
            if check_date(self.args.stop):
                self.error("Invalide stop")
                sys.exit(1)
            self.debug("Add orcid")
            if not self.db.add_user(self.args.orchid, self.args.start, self.args.stop):
                self.error("Doubled orchid entry. Nothing have been added.")
        else:
            self.debug("Add orcid")
            if not self.db.add_user(self.args.orchid, self.args.start, None):
                self.error("Doubled orchid entry. Nothing have been added.")
        self.close()

    def prints(self):
        self.open()
        for orc in self.db.get_orcids():
            print(orc)
        self.close()

    def clean(self):
        self.open()
        self.debug("Drop old DB")
        self.db.drop_db()
        self.debug("Create new DB")
        self.db.create_db()
        self.close()

    def create(self):
        self.open()
        self.debug("Create new DB")
        if not self.db.create_db():
            self.error("DB already exists")
        self.close()

    def create_test(self):
        self.open()
        self.debug("Create test DB")
        self.db.create_test_db()
        self.close()

    def add_conf(self):
        self.open()
        self.debug("Insert config in DB")
        self.db.add_config(self.args.cliend_id, self.args.clien_secret, self.args.auth, self.args.api)
        self.close()
