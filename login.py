from flask import Flask, redirect, render_template, request, session, app
from flask_session import Session
from finance_model import financeModel
import datetime
import cv2

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
            if request.form.get("login"):
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

            if request.form.get("faceid"):
                # start video capture
                video_capture = cv2.VideoCapture(0)

                # loop the caputre till keypress
                while True:
                    # Capture frame-by-frame  and covert to gray scale
                    ret, frame = video_capture.read()
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Display the resulting frame
                    cv2.imshow('Video', frame)

                    # press q for 1 sec to stop the application
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                # When everything is done, release the capture
                video_capture.release()
                cv2.destroyAllWindows()
        return render_template("login.html")

    def logout(self):
        session["name"] = None
        return redirect("/")
