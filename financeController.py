import base64
import csv
import json
import os
import smtplib
import datetime
from io import BytesIO
from flask import render_template, redirect, request, app, flash, send_file
from fpdf import FPDF

from login_encap import Register
from finance_encap import FinanceEncap
from finance_model import financeModel
from login import Login
import matplotlib.pyplot as pyplot
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename

class FinanceController:
    def __init__(self, app):

        pass

    def settings_page(self):
        loguser = Login(app)
        finaluser = loguser.get_user()
        fm = financeModel(app)
        settingsdata = fm.fetchSettingsData(finaluser)
        return render_template("settings.html", settingsdata=settingsdata)

    def change_password(self):
        if request.method == "POST":
            if request.form.get("chng-pwd"):
                newpwd = request.form.get("newpwd")
                repwd = request.form.get("repwd")

                loguser = Login(app)
                finaluser = loguser.get_user()
                if newpwd != repwd:
                    flash("Password not match. Re-enter", "info")
                    return redirect("/settingpg")
                else:
                    fm = financeModel(app)
                    fm.changePwd(finaluser, newpwd)
                    flash("Password Changed Successfully", "info")
                    return redirect("/settingpg")

    def show_settings_update(self):
        loguser = Login(app)
        finaluser = loguser.get_user()
        fm = financeModel(app)
        settingsdata = fm.fetchSettingsData(finaluser)
        return render_template("settings_update.html", settingsdata=settingsdata)

    def update_details(self):
        if request.method == "POST":
            if request.form.get("upddet"):
                username = request.form.get("username")
                usemail = request.form.get("usemail")
                dob = request.form.get("dob")
                pnum = request.form.get("pnum")
                pwd = request.form.get("pwd")
                userupd = request.form.get("userupd")

                reg = Register(username, usemail, dob, pnum, pwd)
                reg.set_usname(username)
                reg.set_usemail(usemail)
                reg.set_usdob(dob)
                reg.set_usnum(pnum)
                reg.set_uspwd(pwd)

                fm = financeModel(app)
                fm.updateUserDetails(reg, userupd)

                flash("Update Details Successfully", "info")
                return redirect("/")

    def register(self):
        if request.method == "POST":
            if request.form.get("usreg"):
                name = request.form.get("fname")
                usemail = request.form.get("usemail")
                usdob = request.form.get("usdob")
                usnum = request.form.get("usphnum")
                pwd = request.form.get("uspwd")

                reg = Register(name, usemail, usdob, usnum, pwd)
                reg.set_usname(name)
                reg.set_usemail(usemail)
                reg.set_usdob(usdob)
                reg.set_usnum(usnum)
                reg.set_uspwd(pwd)

                fm = financeModel(app)
                fuid = fm.addUser(reg)

                self.send_email(usemail, fuid, name)

                return redirect("/")

    def send_email(self, usemail, fuid, name):
        EMAIL_ADDRESS = os.environ.get('MAIL_DEFAULT_SENDER')
        EMAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            subject = 'Registeration Success'
            body = f"""Dear Customer \n {name}, Thanks For Registering with Finance Manager. 
                Please use the following UserID to log-in to the application:{fuid} \n 
                Thank you for using our application - Finance Manager. \n 
                For any further queries please contact +919885983806"""

            msg = f'Subject: {subject}\n\n {body}'

            smtp.sendmail(EMAIL_ADDRESS, usemail, msg)

    def planner_data(self):
        loguser = Login(app)
        finaluser = loguser.get_user()
        fm = financeModel(app)
        plandata = fm.fetchPlan(finaluser)
        return render_template("planner_data.html", plandata=plandata)

    def planner_page(self):
        return render_template("planner.html")

    def fetch_plan_update(self):
        if request.method == "GET":
            puid = request.args.get("puid")
            pdoe = request.args.get("pdoe")
            fm = financeModel(app)
            updata = fm.fetchPlanUpdate(puid, pdoe)
            return json.dumps(updata)

    def update_plan(self):
        if request.method == "POST":
            if request.form.get("upd-plan"):
                upincome = request.form.get("upincome")
                upamounts = request.form.get("upamounts")
                uptax = request.form.get("uptax")
                upothexp = request.form.get("upothexp")
                updoe = request.form.get("up-date-of-entry")
                upcomments = request.form.get("upcomments")
                upuserid = request.form.get("upuserid")

                fin = FinanceEncap(upincome, upamounts, uptax, upothexp, updoe, upcomments)
                fin.set_income(upincome)
                fin.set_otheramt(upamounts)
                fin.set_tax(uptax)
                fin.set_otherexp(upothexp)
                fin.set_dtofent(updoe)
                fin.set_comment(upcomments)

                fm = financeModel(app)
                fm.updatePlan(fin, upuserid, updoe)

                flash("Updated Plan Successfully", "info")
                return redirect("/")

    def planner(self):
        if request.method == "POST":
            if request.form.get("add-plan"):
                pincome = request.form.get("pincome")
                pamounts = request.form.get("pamounts")
                ptax = request.form.get("ptax")
                pothexp = request.form.get("pothexp")
                pdtofent = request.form.get("p-date-of-entry")
                pcomments = request.form.get("pcomments")
                loguser = Login(app)
                finaluser = loguser.get_user()

                fin = FinanceEncap(pincome, pamounts, ptax, pothexp, pdtofent, pcomments)
                fin.set_income(pincome)
                fin.set_otheramt(pamounts)
                fin.set_tax(ptax)
                fin.set_otherexp(pothexp)
                fin.set_dtofent(pdtofent)
                fin.set_comment(pcomments)

                fm = financeModel(app)
                fm.addPlan(fin, finaluser)

                flash("Plan Record Successfully", "info")
                return redirect("/")

    def del_plan(self):
        if request.method == "GET":
            delplan = request.args.get("delplan")
            delpuid = request.args.get("delpuid")

            fm = financeModel(app)
            fm.delPlan(delplan, delpuid)
        return delplan

    def add_data(self):
        return render_template("add_data.html")

    def saveData(self):
        if request.method == "POST":
            if request.form.get("addt"):
                loguser = Login(app)
                finaluser = loguser.get_user()

                income = request.form.get("income")
                otheramt = request.form.get("tamounts")
                tax = request.form.get("tax")
                otherexp = request.form.get("oexpenditures")
                dtofent = request.form.get("date-of-entry")
                comment = request.form.get("comments")

                fin = FinanceEncap(income, otheramt, tax, otherexp, dtofent, comment)
                fin.set_income(income)
                fin.set_otheramt(otheramt)
                fin.set_tax(tax)
                fin.set_otherexp(otherexp)
                fin.set_dtofent(dtofent)
                fin.set_comment(comment)

                fm = financeModel(app)
                fm.addData(fin, finaluser)

                flash("Data Added Successfully", "info")
                return redirect("/")

    def my_data(self):
        loguser = Login(app)
        finaluser = loguser.get_user()
        fm = financeModel(app)
        data = fm.fetchData(finaluser)
        return render_template("data.html", data=data)

    def fetch_update(self):
        if request.method == "GET":
            userID = request.args.get("userId")
            doe = request.args.get("doe")
            fm = financeModel(app)
            updata = fm.fetchUpdate(userID, doe)
            return json.dumps(updata)

    def update_data(self):
        if request.method == "POST":
            if request.form.get("upddt"):
                uincome = request.form.get("uincome")
                uamounts = request.form.get("uamounts")
                utax = request.form.get("utax")
                uexp = request.form.get("uexp")
                udoe = request.form.get("u-date-of-entry")
                ucomments = request.form.get("ucomments")
                uuserid = request.form.get("uuserid")

                fin = FinanceEncap(uincome, uamounts, utax, uexp, udoe, ucomments)
                fin.set_income(uincome)
                fin.set_otheramt(uamounts)
                fin.set_tax(utax)
                fin.set_otherexp(uexp)
                fin.set_dtofent(udoe)
                fin.set_comment(ucomments)

                fm = financeModel(app)
                fm.updateData(fin, uuserid, udoe)

                flash("Updated Data Successfully", "info")
                return redirect("/")

    def del_data(self):
        if request.method == "GET":
            deldoe = request.args.get("deldoe")
            deluid = request.args.get("deluid")

            fm = financeModel(app)
            fm.delData(deldoe, deluid)
        return deldoe

    def current_yr(self):
        dt = datetime.datetime.now()
        date = dt.strftime('%Y')
        loguser = Login(app)
        finaluser = loguser.get_user()
        fm = financeModel(app)
        currentdata = fm.fetchCurrentDate(finaluser)
        finaldata = []
        for i in currentdata:
            split = i[0]
            if date == split[0:4]:
                finaldata.append(i)
        showdata = []
        for j in finaldata:
            showdata.append(fm.fetchCurrentData(j))
        return render_template("current_yr.html", date=date, showdata=showdata)

    def generation_mailing(self):
        return render_template("pdf_mail.html")

    def graph_email(self):
        if request.method == "POST":
            if request.form.get("grphemail"):
                sndemail = request.form.get("sndemail")
                emldoe = request.form.get("emldoe")
                fm = financeModel(app)
                grphdt = fm.graphEmail(emldoe)
                if len(grphdt) == 0:
                    flash("Data Not Available For This Date", "info")
                    return redirect("/generate-mail-pg")
                loguser = Login(app)
                finaluser = loguser.get_user()
                piegr = BytesIO()
                data = np.array([grphdt[0][1], grphdt[0][2], grphdt[0][3], grphdt[0][4]])
                labels = ['Income', 'Earnings', 'Tax', 'Expenditure']
                total = sum(data)
                fig = pyplot.figure(figsize=(2, 2))
                pyplot.pie(data, labels=labels, autopct=lambda p: '{:.0f}%'.format(p * total / 100), shadow=True)
                pyplot.title('Amounts', fontsize=14)
                pyplot.grid(True)
                pyplot.savefig(piegr, format='png')
                pyplot.close()
                piegr.seek(0)
                plot_url = base64.b64encode(piegr.getvalue()).decode('utf8')


                EMAIL_ADDRESS = os.environ.get('MAIL_DEFAULT_SENDER')
                EMAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()

                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

                    subject = 'Finance Manager - Graph'
                    body = f"""Dear Customer \n {finaluser}, Thanks For using Graphing Services with Finance Manager. 
                                Here is the graph for the requested date: {emldoe} --> \n {plot_url} \n 
                                For any further queries please contact +919885983806"""

                    msg = f'Subject: {subject}\n\n {body}'

                    smtp.sendmail(EMAIL_ADDRESS, sndemail, msg)

                return redirect("/")

    def generate_pdf(self):
        # create pdf object
        pdf = FPDF('P', 'mm', 'Letter')
        # add a page
        pdf.add_page()
        # set font and size
        pdf.set_font('times', '', 16)
        loguser = Login(app)
        finaluser = loguser.get_user()
        fm = financeModel(app)
        userdata = fm.fetchData(finaluser)
        pdf.cell(150, 20, "UserID, Income, Earnings, Tax, Expenditure, Comments", ln=True, border=True)
        for data in userdata:
            # insert data into pdf
            pdf.cell(150, 20, str(data), ln=True, border=True)

        # create pdf and name it
        pdf.output('finance_data.pdf')
        flash("PDF Generated Successfully", "info")
        return redirect("/")

    def generate_plan_pdf(self):
        # create pdf object
        pdf = FPDF('P', 'mm', 'Letter')
        # add a page
        pdf.add_page()
        # set font and size
        pdf.set_font('times', '', 16)
        loguser = Login(app)
        finaluser = loguser.get_user()
        fm = financeModel(app)
        plandata = fm.fetchPlan(finaluser)
        pdf.cell(150, 20, "UserID, Income, Earnings, Tax, Expenditure, Comments", ln=True, border=True)
        for plan in plandata:
            # insert data into pdf
            pdf.cell(150, 20, str(plan), ln=True, border=True)

        # create pdf and name it
        pdf.output('finance_plan.pdf')
        flash("PDF Generated Successfully", "info")
        return redirect("/")

    def upload_export(self):
        return render_template("upload_export.html")

    def export_csv(self):
        fm = financeModel(app)
        loguser = Login(app)
        finaluser = loguser.get_user()
        filename = "data"
        myfilename = filename + ".csv"
        with open(myfilename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['UserID', 'Income', 'Earnings', 'Tax', 'Expenditure', 'Date', 'Comments'])
            writer.writerows(fm.fetchData(finaluser))
        flash("CSV Generated Successfully", "info")
        return redirect("/")

    def export_plan_csv(self):
        fm = financeModel(app)
        loguser = Login(app)
        finaluser = loguser.get_user()
        filename = "plan"
        myfilename = filename + ".csv"
        with open(myfilename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['UserID', 'Income', 'Earnings', 'Tax', 'Expenditure', 'Date', 'Comments'])
            writer.writerows(fm.fetchPlan(finaluser))
        flash("CSV Generated Successfully", "info")
        return redirect("/")

    def uplod_doc(self):
        loguser = Login(app)
        finaluser = loguser.get_user()
        fm = financeModel(app)
        filedt = fm.fetchFiles(finaluser)
        return render_template("upload_doc.html", filedt=filedt)

    def upload_file(self):
        loguser = Login(app)
        finaluser = loguser.get_user()
        if request.method == 'POST':
            file = request.files['file']
            fm = financeModel(app)
            fm.insertFile(finaluser, file.filename, file.stream.read())
            flash("Uploaded Successfully", "info")
            return redirect("/")


    def download(self, fileuser, filename):
        fm = financeModel(app)
        return send_file(BytesIO(fm.downloadFile(fileuser, filename)[0][0]), attachment_filename=filename, as_attachment=True)


    def analysis_show(self):
        return render_template("analysis.html")
