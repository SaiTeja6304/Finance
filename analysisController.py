import base64
from io import BytesIO
import pandas as pd
from flask import render_template, redirect, request, app, flash
from analysis_model import analysisModel
from login import Login
import matplotlib.pyplot as pyplot
import numpy as np
import datetime

class AnalysisController:
    def __init__(self, app):
        pass

    def current_yrdata(self):
        dt = datetime.datetime.now()
        year = dt.strftime('%Y')
        loguser = Login(app)
        finaluser = loguser.get_user()
        am = analysisModel(app)
        currentyear = am.fetchCurrentDate(finaluser)
        finaldata = []
        showdata = []
        finalyear = []
        for i in currentyear:
            split = i[0]
            if year == split[0:4]:
                finaldata.append(i)
                finalyear.append(i)
        for j in finaldata:
            showdata.append(am.fetchCurrentData(j))
        sumincome = 0
        sumamt = 0
        sumtax = 0
        sumexp = 0
        for k in showdata:
            sumincome = sumincome + k[0][1]
            sumamt = sumamt + k[0][2]
            sumtax = sumtax + k[0][3]
            sumexp = sumexp + k[0][4]
        data = {'Finance': 'Amount', 'Income': sumincome, 'Earnings': sumamt, 'Tax': sumtax, 'Expenditure': sumexp}
        savings = []
        for dt in showdata:
            sumearn = dt[0][1] + dt[0][2]
            sumexp = dt[0][3] + dt[0][4]
            save = sumearn - sumexp
            savings.append(save)
        finalyearconverted = []
        img = BytesIO()
        for yr in finalyear:
            finalyearconverted.append(str(yr))
        line = {'date': finalyearconverted, 'savings': savings}
        df = pd.DataFrame(line)
        pyplot.plot(df['date'], df['savings'], color='red', marker='o')
        pyplot.title('date vs savings', fontsize=14)
        pyplot.xlabel('date', fontsize=14)
        pyplot.ylabel('savings', fontsize=14)
        pyplot.grid(True)
        pyplot.savefig(img, format='png')
        pyplot.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        return render_template("current_yrdata.html", data=data, year=year, plot_url=plot_url)

    def prev_yrdata(self):
        loguser = Login(app)
        finaluser = loguser.get_user()
        am = analysisModel(app)
        data = am.fetchData(finaluser)
        savings = []
        for dt in data:
            sumearn  = dt[1] + dt[2]
            sumexp = dt[3] + dt[4]
            save = sumearn - sumexp
            savings.append(save)
        return render_template("prev_yrdata.html", data=data, savings=savings)

    def graphData(self, income, earn, tax, exp):
        data = np.array([income, earn, tax, exp])
        labels = ['Income', 'Earnings', 'Tax', 'Expenditure']
        total = sum(data)
        fig = pyplot.figure(figsize=(2, 2))
        pyplot.pie(data, labels=labels, autopct=lambda p: '{:.0f}%'.format(p * total / 100), shadow=True)
        pyplot.show()

        return redirect("/prevgrph")

    def graphical_analysis(self):
        loguser = Login(app)
        finaluser = loguser.get_user()
        am = analysisModel(app)
        yeardata = am.fetchData(finaluser)
        savearr = []
        for yd in yeardata:
            sumearn = yd[1] + yd[2]
            sumexp = yd[3] + yd[4]
            savings = sumearn - sumexp
            savearr.append(savings)
        dates = am.fetchCurrentDate(finaluser)
        finaldates = []
        for date in dates:
            finaldates.append(str(date))
        bargr = BytesIO()
        pyplot.plot(finaldates, savearr, color='red', marker='o')
        pyplot.title('date vs savings', fontsize=14)
        pyplot.xlabel('date', fontsize=14)
        pyplot.ylabel('savings', fontsize=14)
        pyplot.grid(True)
        pyplot.savefig(bargr, format='png')
        pyplot.close()
        bargr.seek(0)
        plot_url = base64.b64encode(bargr.getvalue()).decode('utf8')
        #bar graph
        piegr = BytesIO()
        pyplot.bar(finaldates, savearr, color='maroon', width = 0.4)
        pyplot.title('date vs savings', fontsize=14)
        pyplot.xlabel('date', fontsize=14)
        pyplot.ylabel('savings', fontsize=14)
        pyplot.savefig(piegr, format='png')
        pyplot.close()
        piegr.seek(0)
        plot_url1 = base64.b64encode(piegr.getvalue()).decode('utf8')
        yearlist = [yrs for yrs in range(0, 9999)]
        return render_template("graphical_analysis.html", plot_url=plot_url, yearlist=yearlist, plot_url1=plot_url1)

    def graph_all_years(self):
        if request.method == "GET":
            grdt = request.args.get("grdt")
            loguser = Login(app)
            finaluser = loguser.get_user()
            am = analysisModel(app)
            currentyear = am.fetchCurrentDate(finaluser)
            finaldata = []
            for i in currentyear:
                split = i[0]
                if grdt == split[0:4]:
                    finaldata.append(i)
            if len(finaldata) == 0:
                print("hi")
                flash("Data Not Available For This Date", "info")
                return redirect("/graph-analysis-pg")
            showdata = []
            for j in finaldata:
                showdata.append(am.fetchCurrentData(j))
            savearr = []
            for k in showdata:
                sumearn = k[0][1] + k[0][2]
                sumexp = k[0][3] + k[0][4]
                save = sumearn - sumexp
                savearr.append(save)
            income = 0
            earn = 0
            tax = 0
            exp = 0
            saveindex = 0
            savings = 0
            bararr = []
            barheadings = ["Income", "Earnings", "Tax", "Expenditure", "Savings"]
            for dt in showdata:
                income = dt[0][1] + income
                earn = dt[0][2] + earn
                tax = dt[0][3] + tax
                exp = dt[0][4] + exp
                savings = savearr[saveindex] + savings
            bararr.append(income)
            bararr.append(earn)
            bararr.append(tax)
            bararr.append(exp)
            bararr.append(savings)
            pyplot.bar(barheadings, bararr, color='maroon', width = 0.4)
            pyplot.title(f'Total Year Finance for {grdt}', fontsize=14)
            pyplot.xlabel('Date', fontsize=14)
            pyplot.ylabel('Amount', fontsize=14)
            pyplot.show()
            return redirect("/graph-analysis-pg")
