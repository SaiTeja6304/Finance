from flask import render_template, redirect, request, app
from analysis_model import analysisModel
from login import Login
import matplotlib.pyplot as pyplot
import numpy as np

class AnalysisController:
    def __init__(self, app):
        pass

    def current_yrdata(self):
        return render_template("current_yrdata.html")

    def prev_yrdata(self):
        loguser = Login(app)
        finaluser = loguser.get_user()
        am = analysisModel(app)
        data = am.fetchData(finaluser)
        return render_template("prev_yrdata.html", data=data)

    def graphData(self, income, earn, tax, exp):
        data = np.array([income, earn, tax, exp])
        labels = ['Income', 'Earnings', 'Tax', 'Expenditure']
        total = sum(data)
        fig = pyplot.figure(figsize=(2, 2))
        pyplot.pie(data, labels=labels, autopct=lambda p: '{:.0f}%'.format(p * total / 100), shadow=True)
        pyplot.show()

        return redirect("/prevgrph")

    def graphical_analysis(self):
        return render_template("graphical_analysis.html")