from flask import render_template, redirect, request

class AnalysisController:
    def __init__(self, app):
        pass

    def current_yrdata(self):
        return render_template("current_yrdata.html")

    def prev_yrdata(self):
        return render_template("prev_yrdata.html")

    def graphical_analysis(self):
        return render_template("graphical_analysis.html")