# Main

from flask import Flask
from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)
@app.route("/")  # this sets the route to this page
def home():
	return render_template("home.html")

@app.route("/AboutUs")  # this sets the route to this page
def about():
	return render_template("AboutUs.html")

@app.route("/Statistics")  # this sets the route to this page
def stat():
	return render_template("Statistics.html")

@app.route("/Staff")  # this sets the route to this page
def staff():
	return render_template("Staff.html")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
