__author__ = 'Matthew'
try:
    import pymysql
except ImportError:
    import pip
    pip.main(['install','pymysql'])
    import pymysql
from math import floor


import timestamp


class MYSQL_CONSTANTS:
    VARCHAR = 'VARCHAR'
    INT = 'INT'

class FormConstants:
    YES = 'YES'
    NO = 'NO'
    MAYBE = 'PROBABLY'
    YES_LATE = 'YES+-+LATE'

    @staticmethod
    def dict():
        return {
            'YES':1,
            'NO':0,
            'PROBABLY':.5,
            'YES+-+LATE':1
        }

class db(object):
    class MySQL_DB_EXCEPTION(Exception):
        pass

    def __init__(self, dbName, tbName):
        self.dbName = dbName.lower()
        self.tbName = tbName.lower()
        self.columns = [('ip', MYSQL_CONSTANTS.VARCHAR + '(20)'), ('vote', MYSQL_CONSTANTS.VARCHAR + '(15)')]
        self.conn = pymysql.connect(
        db='bballcounter',
        user='root',
        passwd='07041776',
        host='localhost')

        self._set_up_db()

    def update_player(self, ip, vote):
        c = self.conn.cursor()

        c.execute("USE {0}".format(self.dbName))
        self.conn.commit()

        #already in??
        c.execute("SELECT * FROM {0} WHERE ip='{1}'".format(self.tbName, ip))
        already_inserted = len([r for r in c.fetchall()]) > 0

        if not already_inserted:
            # insert
            command = "INSERT INTO {0} VALUES (0, '{1}', '{2}')".format(self.tbName, ip, vote)
        else:
            #update

            command = "UPDATE {0} SET vote='{1}' WHERE ip='{2}'".format(self.tbName, vote, ip)
        print "{0}: Executing MySQL command: {1}".format(timestamp.timeStamp(), command)
        c.execute(command)
        self.conn.commit()

    def get_count(self):
        c = self.conn.cursor()

        c.execute("USE {0}".format(self.dbName))
        self.conn.commit()

        #already in??
        c.execute("SELECT * FROM {0}".format(self.tbName))
        votes = [r[2] for r in c.fetchall()]

        count = 0
        value = FormConstants.dict()
        for vote in votes:
            count += FormConstants.dict()[vote]

        return int(floor(count))



    def _set_up_db(self):
        c = self.conn.cursor()

        c.execute("SHOW DATABASES")
        dbs = [r[0] for r in c.fetchall()]
        if self.dbName not in dbs:
            c.execute("CREATE DATABASE {0}".format(self.dbName)) #for some reason, CREATE DATABASE IF NOT EXISTS ___ doesn't work
            self.conn.commit()

        c.execute("USE {0}".format(self.dbName))
        self.conn.commit()

        c.execute("SHOW TABLES")
        tables = [r[0] for r in c.fetchall()]

        if self.tbName not in tables:
            c.execute("CREATE TABLE {0} (id MEDIUMINT NOT NULL AUTO_INCREMENT, {1}, PRIMARY KEY (id))".format(self.tbName, ','.join('{0} {1}'.format(item[0], item[1]) for item in self.columns)))
            self.conn.commit()

#
# if __name__ == '__main__':
#     import unittest
#
#     class test_MySQL(unittest.TestCase):
#         def test_setup(self):
#