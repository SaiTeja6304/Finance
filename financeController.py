from flask import render_template, redirect, request

class FinanceController:
    def __init__(self, app):
        pass

    def settings_page(self):
        return render_template("settings.html")

    def planner_data(self):
        return render_template("planner_data.html")

    def planner_page(self):
        return render_template("planner.html")

    def add_data(self):
        return render_template("add_data.html")

    def my_data(self):
        return render_template("data.html")

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