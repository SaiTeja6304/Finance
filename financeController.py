import json

from flask import render_template, redirect, request, app, flash
from login_encap import Register
from finance_encap import FinanceEncap
from finance_model import financeModel
from login import Login


class FinanceController:
    def __init__(self, app):

        pass

    def settings_page(self):
        return render_template("settings.html")

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
                fm.addUser(reg)

                return redirect("/")

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
        return render_template("current_yr.html")

    def generation_mailing(self):
        return render_template("pdf_mail.html")

    def upload_export(self):
        return render_template("upload_export.html")

    def uplod_doc(self):
        return render_template("upload_doc.html")

    def analysis_show(self):
        return render_template("analysis.html")