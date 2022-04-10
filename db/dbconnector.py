import sqlite3

class DBConn:  # This class creates, opens, and closes the DB connection

    def __init__(self):
        self.con = sqlite3.connect('./db/embyupdate.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.cur.close()
        self.con.close()

    def open(self):
        self.con = sqlite3.connect('./db/embyupdate.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()
        self.con.close()
