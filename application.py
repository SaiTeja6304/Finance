from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import login
import financeController
import analysisController
from finance_model import financeModel

# Initial command
app = Flask(__name__)

# For database connection
db = financeModel("finance.db")

# Creating object for login class created in login file, passing this entire app as parameter
lp = login.Login(app)

# Creating object for FinanceController class created in financeController file
fc = financeController.FinanceController(app)

ac = analysisController.AnalysisController(app)

# Configuring the routes for login
app.add_url_rule("/", view_func=lp.index)
app.add_url_rule("/login", methods=['GET', 'POST'], view_func=lp.login)
app.add_url_rule("/logout", view_func=lp.logout)

# Configuring the routes for finance controller
app.add_url_rule("/settingpg", view_func=fc.settings_page)
app.add_url_rule("/planner-datapg", view_func=fc.planner_data)
app.add_url_rule("/plannerpg", view_func=fc.planner_page)
app.add_url_rule("/add-datapg", view_func=fc.add_data)
app.add_url_rule("/datapg", view_func=fc.my_data)
app.add_url_rule("/current-yrpg", view_func=fc.current_yr)
app.add_url_rule("/generate-mail-pg", view_func=fc.generation_mailing)
app.add_url_rule("/upload-export-pg", view_func=fc.upload_export)
app.add_url_rule("/upload-docpg", view_func=fc.uplod_doc)
app.add_url_rule("/analysis", view_func=fc.analysis_show)
app.add_url_rule("/register", methods=['GET', 'POST'], view_func=fc.register)
app.add_url_rule("/add-data", methods=['GET', 'POST'], view_func=fc.saveData)
app.add_url_rule("/planning", methods=['GET', 'POST'], view_func=fc.planner)
app.add_url_rule("/update-datapg", methods=['GET', 'POST'], view_func=fc.fetch_update)
app.add_url_rule("/update-data", methods=['GET', 'POST'], view_func=fc.update_data)
app.add_url_rule("/update-planpg", methods=['GET', 'POST'], view_func=fc.fetch_plan_update)
app.add_url_rule("/planning-update", methods=['GET', 'POST'], view_func=fc.update_plan)
app.add_url_rule("/delete-data", methods=['GET', 'POST'], view_func=fc.del_data)
app.add_url_rule("/delete-plan", methods=['GET', 'POST'], view_func=fc.del_plan)
app.add_url_rule("/pass-change", methods=['GET', 'POST'], view_func=fc.change_password)
app.add_url_rule("/show-upddet", view_func=fc.show_settings_update)
app.add_url_rule("/update-details", methods=['GET', 'POST'], view_func=fc.update_details)
app.add_url_rule("/graph-email", methods=['GET', 'POST'], view_func=fc.graph_email)
app.add_url_rule("/generatepdf", view_func=fc.generate_pdf)
app.add_url_rule("/genpdfplan", view_func=fc.generate_plan_pdf)
app.add_url_rule("/exportcsv", view_func=fc.export_csv)
app.add_url_rule("/exptplancsv", view_func=fc.export_plan_csv)
app.add_url_rule("/uploader", methods=['GET', 'POST'], view_func=fc.upload_file)

#Configuring routes for analysis controller
app.add_url_rule("/curyr-data", view_func=ac.current_yrdata)
app.add_url_rule("/prevgrph", view_func=ac.prev_yrdata)
app.add_url_rule("/graph/<int:income>,<int:earn>,<int:tax>,<int:exp>",methods=['GET', 'POST'], view_func=ac.graphData)
app.add_url_rule("/graph-analysis-pg", view_func=ac.graphical_analysis)
app.add_url_rule("/grapanalysis", methods=['GET', 'POST'], view_func=ac.graph_all_years)


# Settings for creating session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Command to run the application
if __name__ == "__main__":
    app.run()