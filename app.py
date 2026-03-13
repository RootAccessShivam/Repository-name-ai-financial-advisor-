from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "finance_secret"


def financial_advice(income, expenses):

    savings = income - expenses

    if savings <= 0:
        return "You are spending more than you earn."
    elif savings < income * 0.2:
        return "Try to save at least 20% of your income."
    elif savings < income * 0.4:
        return "Good saving! Keep it up."
    else:
        return "Excellent savings! Consider investing."


def chatbot_response(message):

    message = message.lower()

    if "save" in message:
        return "It is recommended to save at least 20% of your income."
    elif "invest" in message:
        return "You can invest in SIP, mutual funds, or index funds."
    elif "emergency fund" in message:
        return "An emergency fund should cover 3–6 months of expenses."
    elif "hello" in message or "hi" in message:
        return "Hello! I am your AI Financial Advisor."
    else:
        return "Sorry, I don't understand. Try asking about savings or investments."


# LOGIN ROUTE
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect(url_for("home"))

    return render_template("login.html")


# DASHBOARD ROUTE
@app.route("/", methods=["GET", "POST"])
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    advice = ""
    savings = 0
    rent = 0
    food = 0
    transport = 0
    entertainment = 0

    if request.method == "POST":

        income = float(request.form["income"])
        rent = float(request.form["rent"])
        food = float(request.form["food"])
        transport = float(request.form["transport"])
        entertainment = float(request.form["entertainment"])

        expenses = rent + food + transport + entertainment

        savings = income - expenses
        advice = financial_advice(income, expenses)

    return render_template(
        "index.html",
        advice=advice,
        savings=savings,
        rent=rent,
        food=food,
        transport=transport,
        entertainment=entertainment
    )


# CHATBOT API
@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.form["message"]
    response = chatbot_response(user_message)

    return {"reply": response}


if __name__ == "__main__":
    app.run(debug=True)