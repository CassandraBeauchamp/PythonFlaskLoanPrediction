# Main
from flask import Flask, request
from flask import Flask, render_template, url_for, redirect
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.proj3d import transform
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

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
        name = request.form["name"]
        email = request.form["email"]
        gender = request.form["gender"]
        married = request.form["married"]
        dependents = request.form["dependents"]
        education = request.form["education"]
        self_employed = request.form["self-employed"]
        income = request.form["ApplicantIncome"]
        coapplicantincome = request.form["CoapplicantIncome"]
        amount = request.form["LoanAmount"]
        loan_term = request.form["Loan_Amount_Term"]
        credit = request.form["Credit_History"]
        area = request.form["Property_Area"]
        if area == "urban":
            u = 1
            r = 0
            s = 0
        elif area == "rural":
            u = 0
            r = 1
            s = 0
        else:
            u = 0
            r = 0
            s = 1

        result = predict(np.array([[gender,married,dependents,education,self_employed,income,coapplicantincome,amount,loan_term,
                           credit,r,s,u]],dtype=float))
        print(result)
        if(result>.5):
            return render_template("ApprovedLoan.html")
        else:
            return render_template("DeniedLoan.html")
    return render_template("LoanForm.html")

@app.route("/DeniedLoan")  # this sets the route to this page
def deny():
    return render_template("DeniedLoan.html")

@app.route("/AppovedLoan")  # this sets the route to this page
def approve():
    return render_template("ApprovedLoan.html")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Import Data for Loans
    loan_applications = pd.read_csv("train_u6lujuX_CVtuZ9i (1).csv")
    # Get rid of loan ID, it's not needed
    loan_applications.drop('Loan_ID', axis=1, inplace=True)
    # Fill in all null values
    loan_applications["Gender"] = loan_applications['Gender'].fillna(loan_applications['Gender'].mode()[0])
    loan_applications["Married"] = loan_applications['Married'].fillna(loan_applications['Married'].mode()[0])
    loan_applications["Dependents"] = loan_applications['Dependents'].fillna(loan_applications['Dependents'].mode()[0])
    loan_applications["Self_Employed"] = loan_applications['Self_Employed'].fillna(loan_applications['Self_Employed'].mode()[0])
    loan_applications["LoanAmount"] = loan_applications['LoanAmount'].fillna(loan_applications['LoanAmount'].mean())
    loan_applications["Loan_Amount_Term"] = loan_applications['Loan_Amount_Term'].fillna(loan_applications['Loan_Amount_Term'].mean())
    loan_applications["Credit_History"] = loan_applications['Credit_History'].fillna(loan_applications['Credit_History'].mean())
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
    b, a = np.polyfit(loan_applications["ApplicantIncome"], y=loan_applications["LoanAmount"], deg=1)
    xseq = np.linspace(0, 80000, num=100)
    ax.plot(xseq, a + b * xseq, color="k", lw=2.5);
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

    # Turn the categories into numbers
    ordinal_encoder = OrdinalEncoder()
    loan_applications['Dependents'] = ordinal_encoder.fit_transform(loan_applications[['Dependents']])
    loan_applications['Education'] = ordinal_encoder.fit_transform(loan_applications[['Education']])
    loan_applications['Loan_Status'] = ordinal_encoder.fit_transform(loan_applications[['Loan_Status']])
    loan_applications['Married'] = ordinal_encoder.fit_transform(loan_applications[['Married']])
    loan_applications['Gender'] = ordinal_encoder.fit_transform(loan_applications[['Gender']])
    loan_applications['Self_Employed'] = ordinal_encoder.fit_transform(loan_applications[['Self_Employed']])

    ohe_encoder = OneHotEncoder(sparse=False)

    property_area_encoded = ohe_encoder.fit_transform(loan_applications[['Property_Area']])
    property_area_encoded_df = pd.DataFrame(property_area_encoded,
                                            columns=ohe_encoder.get_feature_names_out(['Property_Area']))

    # Add seperate columns for each property area type
    loan_applications = pd.concat([loan_applications, property_area_encoded_df], axis=1)
    # Get rid of old property area attribute

    loan_applications.drop("Loan_Status", axis=1)
    y = loan_applications['Loan_Status']

    new_loan_applications = loan_applications
    new_loan_applications.drop('Loan_Status', axis=1, inplace=True)
    new_loan_applications.drop('Property_Area', axis=1, inplace=True)

    # Creating our machine learning model using logistic regression
    np.random.seed(42)
    X_train, X_test, y_train, y_test = train_test_split(new_loan_applications,
                                                        y,
                                                        test_size=.5)

    model = LogisticRegression()

    parameters = {'C': np.logspace(-4, 4, 20),
                  'solver': ['liblinear']}

    model = GridSearchCV(model, param_grid=parameters, scoring='accuracy')
    model.fit(X_train, y_train)
    print("Score:" + str(model.score(X_test, y_test)))

    # Make predictions


    # Method for the loan form to get a decision
    def predict(array):
        return model.predict(array)

    app.run(debug=False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
