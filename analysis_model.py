import sqlite3

class analysisModel():
    def __init__(self, app):
        self.con = sqlite3.connect("finance.db")
        self.cur = self.con.cursor()

    def fetchData(self, finaluser):
        self.cur.execute("SELECT * FROM data WHERE userid=?",(finaluser,))
        data = self.cur.fetchall()
        return data

    def fetchCurrentDate(self, finaluser):
        self.cur.execute("SELECT doe FROM data WHERE userid=?",(finaluser,))
        return self.cur.fetchall()

    def fetchCurrentData(self, doe):
        self.cur.execute("SELECT * FROM data WHERE doe=?",(doe))
        return self.cur.fetchall()

    def __del__(self):
        self.cur.close()
        self.con.close()