from flask import Flask, render_template, request, session, redirect
import joblib
import requests
import pandas as pd
import sqlite3

# ML IMPORTS
from ml.forecast_demand import forecast_crop
from ml.explain_model import explain_crop

app = Flask(__name__)
app.secret_key = "secret123"

# =========================
# DATABASE
# =========================
def get_db():
    return sqlite3.connect("data/app.db")


def init_db():
    db = get_db()
    cursor = db.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # LISTINGS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        farmer TEXT,
        crop TEXT,
        quantity TEXT,
        price TEXT,
        contact TEXT,
        quantity_unit TEXT,
        price_unit TEXT
    )
    """)

    db.commit()
    db.close()


# =========================
# AUTH FUNCTIONS
# =========================
def register_user(username, password, role):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, role))
    db.commit()
    db.close()


def login_user(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    db.close()
    return user


# =========================
# MARKETPLACE FUNCTIONS
# =========================
def add_listing(farmer, crop, quantity, price, contact, quantity_unit, price_unit):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO listings VALUES (?, ?, ?, ?, ?, ?, ?)",
        (farmer, crop, quantity, price, contact, quantity_unit, price_unit)
    )
    db.commit()
    db.close()


def get_listings():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT rowid, * FROM listings")
    rows = cursor.fetchall()
    db.close()

    listings = []
    for row in rows:
        listings.append({
            "id": row[0],  # 🔥 important for edit/delete
            "farmer": row[1],
            "crop": row[2],
            "quantity": row[3],
            "price": row[4],
            "contact": row[5],
        })
    return listings


def delete_listing(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM listings WHERE rowid=?", (id,))
    db.commit()
    db.close()


def update_listing(id, crop, quantity, price):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE listings
        SET crop=?, quantity=?, price=?
        WHERE rowid=?
    """, (crop, quantity, price, id))
    db.commit()
    db.close()


# =========================
# LOAD MODEL
# =========================
model = joblib.load("models/crop_model.pkl")
crop_labels = joblib.load("models/crop_labels.pkl")

rainfall_data = pd.read_csv("data/india_major_district_rainfall.csv")

soil_encode = {
    "clay": 0,
    "loamy": 1,
    "sandy": 2,
    "black": 3,
    "alluvial": 4
}

season_encode = {
    "kharif": 0,
    "rabi": 1,
    "zaid": 2
}


# =========================
# WEATHER
# =========================
def get_weather(city):
    api_key = "98a1aefce6dc031fb9f01c5712ef2e05"

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url).json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

    except:
        temp, humidity = 28, 60

    district = rainfall_data[
        rainfall_data["district"].str.lower() == city.lower()
    ]

    rain = district["avg_monthly_rainfall_mm"].values[0] if not district.empty else 100

    return temp, humidity, rain


# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return redirect("/login")


# -------- AUTH --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        register_user(
            request.form["username"],
            request.form["password"],
            request.form["role"]
        )
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = login_user(
            request.form["username"],
            request.form["password"]
        )

        if user:
            session["user"] = user[0]
            session["role"] = user[2]
            return redirect("/dashboard")

        return "Invalid login"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/login")
    return render_template("dashboard.html")


# -------- PREDICTION --------
@app.route("/predict_page")
def predict_page():
    return render_template("predict.html")


@app.route("/predict", methods=["POST"])
def predict():
    soil = request.form["soil_type"]
    season = request.form["season"]
    city = request.form["city"]

    temp, hum, rain = get_weather(city)

    input_data = [[
        soil_encode[soil],
        season_encode[season],
        temp,
        hum,
        rain
    ]]

    pred = model.predict(input_data)[0]
    crop = crop_labels[pred]

    demand_forecast, demand_trend, price_forecast, price_trend = forecast_crop(crop)

    explanation = explain_crop(soil, season, rain, temp, hum, crop)

    return render_template("result.html",
        temperature=temp,
        humidity=hum,
        rainfall=rain,
        season=season,
        crop=crop,
        demand_forecast=demand_forecast,
        demand_trend=demand_trend,
        price_forecast=price_forecast,
        price_trend=price_trend,
        explanation_points=explanation
    )


# -------- FORECAST --------
@app.route("/forecast_page", methods=["GET", "POST"])
def forecast_page():

    if request.method == "POST":
        crop = request.form["crop"]

        demand, dtrend, price, ptrend = forecast_crop(crop)
        # =========================
        # 📊 FORECAST GRAPHS (POPUP)
        # =========================
        import matplotlib.pyplot as plt
        months = [1, 2, 3, 4, 5, 6]

        # Demand graph
        demand_values = [d[1] for d in demand]

        plt.figure()
        plt.plot(months, demand_values, marker='o')
        plt.title("Demand Forecast (Next 6 Months)")
        plt.xlabel("Months")
        plt.ylabel("Demand")
        plt.grid()

        plt.savefig("static/demand_graph.png")  # ✅ ADD
        plt.close()                             # ✅ ADD
        # Price graph
        price_values = [p[1] for p in price]

        plt.figure()
        plt.plot(months, price_values, marker='o')
        plt.title("Price Forecast (Next 6 Months)")
        plt.xlabel("Months")
        plt.ylabel("Price")
        plt.grid()

        import time

        filename = f"static/forecast_{int(time.time())}.png"
        plt.savefig(filename)   # ✅ ADD
        plt.close()                             # ✅ ADD

        # =========================
        
        return render_template(
            "forecast.html",
            demand_forecast=demand,
            demand_trend=dtrend,
            price_forecast=price,
            price_trend=ptrend
        )

    return render_template("forecast.html")


# -------- MARKETPLACE --------
@app.route("/market")
def market():
    listings = get_listings()
    return render_template("market.html", listings=listings)


@app.route("/add_listing", methods=["GET", "POST"])
def add_listing_route():

    if session.get("role") != "farmer":
        return "Access Denied"

    if request.method == "POST":
        add_listing(
            session["user"],
            request.form["crop"],
            request.form["quantity"],
            request.form["price"],
            request.form["contact"],
            request.form["quantity_unit"],
            request.form["price_unit"]
        )
        return redirect("/market")

    return render_template("add_listing.html")


@app.route("/delete_listing/<int:id>")
def delete_listing_route(id):
    listings = get_listings()

    item = next((x for x in listings if x["id"] == id), None)

    if not item or item["farmer"] != session.get("user"):
        return "Unauthorized"

    delete_listing(id)
    return redirect("/market")


@app.route("/edit_listing/<int:id>", methods=["GET", "POST"])
def edit_listing_route(id):
    listings = get_listings()

    item = next((x for x in listings if x["id"] == id), None)

    if not item or item["farmer"] != session.get("user"):
        return "Unauthorized"

    if request.method == "POST":
        update_listing(
            id,
            request.form["crop"],
            request.form["quantity"],
            request.form["price"]
        )
        return redirect("/market")

    return render_template("edit_listing.html", item=item)


# =========================
# RUN
# =========================
db = get_db()
cursor = db.cursor()

cursor.execute("UPDATE listings SET farmer='Praveen Kumar' WHERE farmer='Ragu'")
cursor.execute("UPDATE listings SET contact='919342219547'")

db.commit()
db.close()
if __name__ == "__main__":
    init_db()   # 🔥 IMPORTANT FIX
    app.run(debug=True)