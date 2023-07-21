import sqlite3

class analysisModel():
    def __init__(self, app):
        self.con = sqlite3.connect("finance.db")
        self.cur = self.con.cursor()

    def fetchData(self, finaluser):
        self.cur.execute("SELECT * FROM data WHERE userid=?",(finaluser,))
        data = self.cur.fetchall()
        return data

    def __del__(self):
        self.cur.close()
        self.con.close()