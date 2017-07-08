import sqlite3

conn = sqlite3.connect('example/people.db')
c = conn.cursor()

c.execute("DROP TABLE people")
c.execute("CREATE TABLE people (orcid CHARACTER(16), start DATE, end DATE)")
c.execute("INSERT INTO people VALUES ('0000000219094153','1900-01-01','2016-12-31')")
c.execute("INSERT INTO people VALUES ('000000020183570X','1900-01-01','2016-12-31')")
c.execute("INSERT INTO people VALUES ('0000000303977442','1900-01-01','2016-12-31')")

conn.commit()

conn.close()
