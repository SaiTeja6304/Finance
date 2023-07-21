from flask import Flask, redirect, render_template, request, session, app
from flask_session import Session
from finance_model import financeModel
import datetime

user = ""
# Login class with logic of login & logout & sessions
class Login():

    # Default constructor method
    def __init__(self, app):
        pass

    def get_user(self):
        global user
        return user

    def index(self):
        global user
        if not session.get("name"):
            return redirect("/login")
        dt = datetime.datetime.now()
        date = dt.strftime('%Y-%m-%d %H:%M:%S')
        user = session.get("name")
        return render_template("index.html", date=date)

    def login(self):
        global user
        errorpwd = ""
        incorrectpwd = ""
        if request.method == "POST":
            session["name"] = request.form.get("name")
            upwd = request.form.get("pwd")
            user = session["name"]
            fm = financeModel(app)
            pwdata = fm.loginDetails(session["name"])
            if not pwdata:
                errorpwd = "User does not exist. Please Register"
                return render_template("login.html", error=errorpwd)
            elif upwd == pwdata[0][0]:
                return redirect("/")
            else:
                incorrectpwd = "Wrong Password. Please Try Again"
                return render_template("login.html", error=incorrectpwd)
        return render_template("login.html")

    def logout(self):
        session["name"] = None
        return redirect("/")
