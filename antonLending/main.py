# Main
from flask import Flask, request
from flask import Flask, render_template, url_for, redirect
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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


@app.route("/LoanForm", methods=["GET", "POST"])  # this sets the route to this page
def loanForm():
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["email"])
        return render_template("home.html")
    return render_template("LoanForm.html")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Import Data for Loans
    loan_applications = pd.read_csv("train_u6lujuX_CVtuZ9i (1).csv")
    # Plotting from pandas DataFrames
    colors = {'Y': 'green', 'N': 'red'}
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(x=loan_applications["ApplicantIncome"],
                         y=loan_applications["LoanAmount"],
                         c=loan_applications["Loan_Status"].map(colors))
    ax.set(title="Applicant Income and Loan Amount Scatter Plot",
           xlabel="Applicant Income",
           ylabel="Loan Amount")
    ax.legend(*scatter.legend_elements(), title="Loan Acceptance")
    fig.savefig("Scatter-LoanAmount-LoanStatus.png")

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(x=loan_applications["Loan_Amount_Term"],
                         y=loan_applications["LoanAmount"],
                         c=loan_applications["Loan_Status"].map(colors))
    ax.set(title="Loan Amount Term and Loan Amount",
           xlabel="Loan Amount Term",
           ylabel="Loan Amount")
    ax.legend(*scatter.legend_elements(), title="Loan Acceptance")
    fig.savefig("Scatter-Loan-Amount-Loan-Term.png")

    fig, ax = plt.subplots()
    ax.bar(loan_applications["Loan_Amount_Term"],
           height=loan_applications["ApplicantIncome"],
           width = 1)
    ax.set(title="Loan Amount Term and Applicant Income",
           xlabel="Loan Amount Term",
           ylabel="Applicant Income")
    fig.savefig("Bar-Graph-Loan-Amount-Term.png")

    # loan_applications["Dependents"] = loan_applications["Dependents"].str.replace('[\$\]','')
    # loan_applications["ApplicantIncome"] = loan_applications["ApplicantIncome"].str.replace('[\$\]')
    # loan_applications["CoapplicantIncome"] = loan_applications["CoapplicantIncome"].str.replace('[\$\]')
    # loan_applications["LoanAmount"] = loan_applications["LoanAmount"].str.replace('[\$\]')
    # loan_applications["Loan_Amount_Term"] = loan_applications["Loan_Amount_Term"].str.replace('[\$\]')
    # loan_applications["Credit_History"] = loan_applications["Credit_History"].str.replace('[\$\]')

    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
