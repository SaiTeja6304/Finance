import sqlite3

class financeModel():
    def __init__(self, app):
        self.con = sqlite3.connect("finance.db")
        self.cur =self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (userid TEXT PRIMARY KEY, 
        username TEXT NOT NULL, useremail TEXT NOT NULL, userdob DATE, usernumber TEXT NOT NULL, 
        password TEXT NOT NULL)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS data (userid TEXT NOT NULL, 
        income INTEGER, otheramt INTEGER, tax INTEGER, otherexp INTEGER, doe INTEGER, 
        comments TEXT NOT NULL, FOREIGN KEY(userid) REFERENCES users(userid))""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS plan (userid TEXT NOT NULL, 
        income INTEGER, otheramt INTEGER, tax INTEGER, otherexp INTEGER, doe INTEGER, 
        comments TEXT NOT NULL, FOREIGN KEY(userid) REFERENCES users(userid))""")
        self.con.commit()

    def loginDetails(self, userid):
        self.cur.execute("SELECT password FROM users WHERE userid=?", (userid,))
        pwdata = self.cur.fetchall()
        return pwdata

    def addUser(self, user):
        name = user.get_usname()
        email = user.get_usemail()
        dob = user.get_usdob()
        num = user.get_usnum()
        pwd = user.get_uspwd()

        self.cur.execute('SELECT MAX(rowid) as "mid [integer]" FROM users')
        rows = self.cur.fetchone()[0]
        uid = rows

        if uid == None:
            uid = 1
        else:
            uid = uid + 1

        fuid = 'USER' + str(uid)
        self.cur.execute("INSERT INTO users (userid, username, useremail, userdob, usernumber, password) VALUES (?,?,?,?,?,?)",(fuid, name, email, dob, num, pwd))
        self.con.commit()
        return fuid

    def addData(self, data, fuser):
        income = data.get_income()
        otheramt = data.get_otheramt()
        tax = data.get_tax()
        otherexp = data.get_otherexp()
        dtofent = data.get_dtofent()
        comment = data.get_comment()

        self.cur.execute("INSERT INTO data (userid, income, otheramt, tax, otherexp, doe, comments) VALUES (?,?,?,?,?,?,?)", (fuser, income, otheramt, tax, otherexp, dtofent, comment))
        self.con.commit()

    def fetchData(self, finaluser):
        self.cur.execute("SELECT * FROM data WHERE userid=?",(finaluser,))
        data = self.cur.fetchall()
        return data

    def addPlan(self, plan, finuser):
        income = plan.get_income()
        otheramt = plan.get_otheramt()
        tax = plan.get_tax()
        otherexp = plan.get_otherexp()
        dtofent = plan.get_dtofent()
        comment = plan.get_comment()
        self.cur.execute("INSERT INTO plan (userid, income, otheramt, tax, otherexp, doe, comments) VALUES (?,?,?,?,?,?,?)", (finuser, income, otheramt, tax, otherexp, dtofent, comment))
        self.con.commit()

    def fetchPlan(self, userplan):
        self.cur.execute("SELECT * FROM plan WHERE userid=?",(userplan,))
        plandata = self.cur.fetchall()
        return plandata

    def fetchUpdate(self, userID, doe):
        self.cur.execute("SELECT * FROM data WHERE userid=? AND doe=?",(userID, doe))
        return self.cur.fetchall()

    def updateData(self, updata, uuserid, udoe):
        income = updata.get_income()
        otheramt = updata.get_otheramt()
        tax = updata.get_tax()
        otherexp = updata.get_otherexp()
        dtofent = updata.get_dtofent()
        comment = updata.get_comment()
        self.cur.execute("UPDATE data SET income=?, otheramt=?, tax=?, otherexp=?, comments=? WHERE userid=? AND doe=?",(income, otheramt, tax, otherexp, comment, uuserid, udoe))
        self.con.commit()

    def fetchPlanUpdate(self, puid, pdoe):
        self.cur.execute("SELECT * FROM plan WHERE userid=? AND doe=?", (puid, pdoe))
        return self.cur.fetchall()

    def updatePlan(self, uplan, upuserid, updoe):
        income = uplan.get_income()
        otheramt = uplan.get_otheramt()
        tax = uplan.get_tax()
        otherexp = uplan.get_otherexp()
        dtofent = uplan.get_dtofent()
        comment = uplan.get_comment()
        self.cur.execute("UPDATE plan SET income=?, otheramt=?, tax=?, otherexp=?, comments=? WHERE userid=? AND doe=?",(income, otheramt, tax, otherexp, comment, upuserid, updoe))
        self.con.commit()

    def delData(self, deldoe, deluid):
        self.cur.execute("DELETE FROM data WHERE userid=? AND doe=?",(deluid,deldoe))
        self.con.commit()

    def delPlan(self, delplan, delpuid):
        self.cur.execute("DELETE FROM plan WHERE userid=? AND doe=?",(delpuid, delplan))
        self.con.commit()

    def fetchSettingsData(self, finaluserid):
        self.cur.execute("SELECT * FROM users WHERE userid=?",(finaluserid,))
        return self.cur.fetchall()

    def changePwd(self, pwduser, pwd):
        self.cur.execute("UPDATE users SET password=? WHERE userid=?",(pwd, pwduser))
        self.con.commit()

    def updateUserDetails(self, userdt, userid):
        name = userdt.get_usname()
        email = userdt.get_usemail()
        dob = userdt.get_usdob()
        num = userdt.get_usnum()
        pwd = userdt.get_uspwd()
        self.cur.execute("UPDATE users SET username=?, useremail=?, userdob=?, usernumber=?, password=? WHERE userid=?",(name, email, dob, num, pwd, userid))
        self.con.commit()

    def fetchCurrentDate(self, finaluser):
        self.cur.execute("SELECT doe FROM data WHERE userid=?",(finaluser,))
        return self.cur.fetchall()

    def fetchCurrentData(self, doe):
        self.cur.execute("SELECT * FROM data WHERE doe=?",(doe))
        return self.cur.fetchall()

    def graphEmail(self, doe):
        self.cur.execute("SELECT * FROM data WHERE doe=?",(doe,))
        return self.cur.fetchall()


    def __del__(self):
        self.cur.close()
        self.con.close()