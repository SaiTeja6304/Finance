from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import login
import financeController

# Initial command
app = Flask(__name__)

# Creating object for login class created in login file, passing this entire app as parameter
lp = login.Login(app)

# Creating object for FinanceController class created in financeController file
fc = financeController.FinanceController(app)

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
app.add_url_rule("/graph-analysis-pg", view_func=fc.graphical_analysis)
app.add_url_rule("/generate-mail-pg", view_func=fc.generation_mailing)
app.add_url_rule("/upload-export-pg", view_func=fc.upload_export)

# Settings for creating session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Command to run the application
if __name__ == "__main__":
    app.run()