from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# Login class with logic of login & logout & sessions
class Login():
    # Default constructor method
    def __init__(self, app):
        pass

    def index(self):
        if not session.get("name"):
            return redirect("/login")
        return render_template("index.html")

    def login(self):
        if request.method == "POST":
            session["name"] = request.form.get("name")
            return redirect("/")
        return render_template("login.html")


    def logout(self):
        session["name"] = None
        return redirect("/")
