from sqlite3 import connect, OperationalError, IntegrityError
from ORCSchlange.orcid import OrcID


class DB:
    def __init__(self, path="output/people.db"):
        self.conn = connect(path)
        self.c = self.conn.cursor()

    def get_list(self):
        self.c.execute('SELECT * FROM people')
        return self.c.fetchall()

    def get_orcids(self):
        return (OrcID(*t) for t in self.get_list())

    def close(self):
        self.conn.close()

    def create_db(self):
        try:
            self.c.execute("CREATE TABLE people (orcid CHARACTER(16) PRIMARY KEY, start DATE, end DATE)")
            self.conn.commit()
            return True
        except OperationalError:
            return False

    def drop_db(self):
        try:
            self.c.execute("DROP TABLE people")
            self.conn.commit()
        except OperationalError:
            pass

    def add_user(self, orchid, start, stop):
        try:
            self.c.execute("INSERT INTO people VALUES (?,?,?)", (orchid, start, stop))
            self.conn.commit()
            return True
        except IntegrityError:
            return False

    def create_test_db(self):
        self.drop_db()
        self.create_db()
        self.add_user("0000000219094153", "1900-01-01", "2016-12-31")
        self.add_user("000000020183570X", "1900-01-01", "2016-12-31")
        self.add_user("0000000303977442", "1900-01-01", "2016-12-31")

    def add_config(self, client_id, secret, auth, api):
        try:
            self.c.execute("DROP TABLE config")
            self.conn.commit()
        except OperationalError:
            pass
        self.c.execute("CREATE TABLE config (api TEXT, auth TEXT, id TEXT, secret TEXT)")
        self.conn.commit()
        self.c.execute("INSERT INTO config VALUES (?,?,?,?)", (api, auth, client_id, secret))
        self.conn.commit()

    def read_config(self):
        self.c.execute('SELECT * FROM config')
        return self.c.fetchone()
