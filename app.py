from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import numpy as np
import joblib
import os
import sqlite3
import hashlib

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-very-secure-secret-key'

# ------------------ DATABASE INITIALIZATION -------------------
def init_db():
    conn = sqlite3.connect('farmhub.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create contacts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Call this at startup
init_db()

# ------------------ Load Models Safely -------------------
base_path = os.path.join(os.path.dirname(__file__), 'models')

try:
    crop_model = joblib.load(os.path.join(base_path, 'crop_recommendation_model.pkl'))
    label_encoder = joblib.load(os.path.join(base_path, 'crop_label_encoder.pkl'))
    yield_model = joblib.load(os.path.join(base_path, 'farmhub_yield_model.pkl'))
except Exception as e:
    print(f"⛔️ Error loading models: {e}")

# ------------------ Helper Functions -------------------
def get_db_connection():
    conn = sqlite3.connect('farmhub.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------ ROUTES -------------------
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get("identifier")
        password = hash_password(data.get("password"))

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return jsonify({"message": "Login successful", "redirect": "/farmers-dashboard"})
        else:
            return jsonify({"message": "Invalid email or password"}), 401
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        dob = data.get("DOB")
        gender = data.get("gender")
        password = hash_password(data.get("password"))

        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO users (name, email, dob, gender, password) VALUES (?, ?, ?, ?, ?)",
                         (name, email, dob, gender, password))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Signup successful', 'redirect': '/farmers-dashboard'})
        except sqlite3.IntegrityError:
            return jsonify({'message': 'Email already registered'}), 400
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------ Admin Credentials -------------------
ADMIN_EMAIL = "sanketdhawade2002@gmail.com"
ADMIN_PASSWORD = hash_password("Sjd@1234")

# ------------------ Admin Login -------------------
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = hash_password(data.get('password'))

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = True
            return jsonify({"message": "Admin login successful", "redirect": "/admin_dashboard"})
        else:
            return jsonify({"message": "Invalid admin credentials"}), 401
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()

    return render_template('admin_dashboard.html', users=users, contacts=contacts)

@app.route('/contactus', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        conn = get_db_connection()
        conn.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()

        return jsonify({"message": "Thank you! We have received your message."})
    return render_template('contactus.html')

@app.route('/farmers-dashboard')
def farmer_dashboard():
    if 'user_id' in session:
        return render_template("homepage.html", name=session['user_name'])
    return redirect(url_for('login'))

# ------------------ Page Routes -------------------
@app.route('/crops')
def crop_form():
    return render_template('crops.html')

@app.route('/yield')
def yield_form():
    return render_template('yield.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/yield-prediction')
def yield_prediction():
    return render_template('yield-prediction.html')

@app.route('/storageguidelines')
def storage_guidelines():
    return render_template('storageguidelines.html')

@app.route('/analyzer')
def analyzer():
    return render_template('soil-analyzer.html')

@app.route('/smart-crop-management')
def smart_crop():
    return render_template('SMART-CROP-MANAGEMENT.html')

@app.route('/analyse-tool')
def analyse_tool():
    return render_template('soil-analyse-tool.html')

@app.route('/schemes')
def schemes():
    return render_template('schemes.html')

@app.route('/profit-calculator')
def profit_calculator():
    return render_template('profit-calculator.html')

@app.route('/produce')
def produce():
    return render_template('PRODUCE PROCESSING.html')

@app.route('/pest-alerts')
def pest_alerts():
    return render_template('pest-alerts.html')

@app.route('/market-dashboard')
def market_dashboard():
    return render_template('market-dashboard.html')

@app.route('/logistics')
def logistics_transport():
    return render_template('logistics-and-transport.html')

@app.route('/faq')
def faq():
    return render_template('FAQ.html')

@app.route('/expense-tracker')
def expense_tracker():
    return render_template('expense-tracker.html')

@app.route('/crop-recommendation')
def crop_recommendation():
    return render_template('crop-recommendation.html')

@app.route('/crop-calendar')
def crop_calendar():
    return render_template('crop-calendar.html')

@app.route('/about-us')
def about_us():
    return render_template('About-us.html')

# ------------------ VALIDATION FUNCTION -------------------
def check_input_limits(data):
    warnings = []

    if data['nitrogen'] < 10:
        warnings.append("⚠️ Nitrogen is too low. This may lead to stunted growth and yellowing of leaves.")
    elif data['nitrogen'] > 140:
        warnings.append("⚠️ Nitrogen is too high. It can cause excessive leaf growth and poor flowering/fruiting.")

    if data['phosphorus'] < 5:
        warnings.append("⚠️ Phosphorus is too low. Root development and flowering may be severely affected.")
    elif data['phosphorus'] > 145:
        warnings.append("⚠️ Phosphorus is too high. Can cause nutrient imbalance and zinc deficiency.")

    if data['potassium'] < 5:
        warnings.append("⚠️ Potassium is too low. Increases risk of diseases and weak stem development.")
    elif data['potassium'] > 205:
        warnings.append("⚠️ Potassium is too high. May inhibit uptake of magnesium and calcium.")

    if data['temperature'] < 8:
        warnings.append("⚠️ Temperature is too low. Crops may experience frost damage or delayed growth.")
    elif data['temperature'] > 43:
        warnings.append("⚠️ Temperature is too high. May cause heat stress, wilting, and flower drop.")

    if data['humidity'] < 14:
        warnings.append("⚠️ Humidity is too low. Risk of drought stress and reduced transpiration.")
    elif data['humidity'] > 100:
        warnings.append("⚠️ Humidity is too high. Increases risk of fungal diseases and mold.")

    if data['ph'] < 3.5:
        warnings.append("⚠️ Soil is too acidic. Nutrient absorption will be limited, harming crop health.")
    elif data['ph'] > 9.5:
        warnings.append("⚠️ Soil is too alkaline. Essential nutrients like iron and phosphorus become unavailable.")

    if data['rainfall'] < 20:
        warnings.append("⚠️ Rainfall is too low. Soil dryness may lead to seed failure and low yield.")
    elif data['rainfall'] > 300:
        warnings.append("⚠️ Rainfall is too high. Waterlogging can damage roots and cause crop rot.")

    return warnings

# ------------------ ML PREDICTION ROUTES -------------------
@app.route('/predict_crop', methods=['POST'])
def predict_crop():
    try:
        input_data = {
            'nitrogen': float(request.form['nitrogen']),
            'phosphorus': float(request.form['phosphorus']),
            'potassium': float(request.form['potassium']),
            'temperature': float(request.form['temperature']),
            'humidity': float(request.form['humidity']),
            'ph': float(request.form['ph']),
            'rainfall': float(request.form['rainfall'])
        }

        warnings = check_input_limits(input_data)

        features = np.array([[
            input_data['nitrogen'],
            input_data['phosphorus'],
            input_data['potassium'],
            input_data['temperature'],
            input_data['humidity'],
            input_data['ph'],
            input_data['rainfall']
        ]])

        prediction = crop_model.predict(features)[0]

        try:
            crop_name = label_encoder.inverse_transform([prediction])[0]
        except Exception:
            crop_name = str(prediction)

        return render_template(
            'crop-recommendation.html',
            prediction_text=f"🌱 Recommended Crop: {crop_name}",
            warnings=warnings
        )

    except Exception as e:
        return render_template('crop-recommendation.html', prediction_text=f"❌ Error: {str(e)}")

@app.route('/predict_yield', methods=['POST'])
def predict_yield():
    try:
        area = float(request.form['area'])
        rainfall = float(request.form['rainfall'])
        temperature = float(request.form['temperature'])

        features = np.array([[area, rainfall, temperature]])
        predicted_yield = yield_model.predict(features)[0]

        return render_template('yield.html', prediction_text=f"🌾 Expected Yield: {predicted_yield:.2f} tonnes")

    except Exception as e:
        return render_template('yield.html', prediction_text=f"❌ Error: {str(e)}")

# ------------------ Start the Server -------------------
if __name__ == '__main__':
    app.run(debug=True)
