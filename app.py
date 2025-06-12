from flask import Flask, render_template, request
import numpy as np
import joblib
import os

app = Flask(__name__)

# ------------------ Load Models Safely -------------------

base_path = os.path.join(os.path.dirname(__file__), 'models')

try:
    crop_model = joblib.load(os.path.join(base_path, 'crop_recommendation_model.pkl'))
    label_encoder = joblib.load(os.path.join(base_path, 'crop_label_encoder.pkl'))
    yield_model = joblib.load(os.path.join(base_path, 'farmhub_yield_model.pkl'))
except Exception as e:
    print(f"⛔️ Error loading models: {e}")

# ------------------ ROUTES -------------------

@app.route('/')
def home():
    return render_template('homepage.html')

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

@app.route('/signup')
def signup():
    return render_template('signup.html')

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/farmers-dashboard')
def farmer_dashboard():
    return render_template("farmers-dashboard.html")

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

@app.route('/contactus')
def contact_us():
    return render_template('contactus.html')

@app.route('/about-us')
def about_us():
    return render_template('About-us.html')


# ------------------ VALIDATION FUNCTION -------------------

def check_input_limits(data):
    warnings = []

    if data['nitrogen'] < 10:
        warnings.append("⚠️ Nitrogen is too low.")
    elif data['nitrogen'] > 140:
        warnings.append("⚠️ Nitrogen is too high.")

    if data['phosphorus'] < 5:
        warnings.append("⚠️ Phosphorus is too low.")
    elif data['phosphorus'] > 145:
        warnings.append("⚠️ Phosphorus is too high.")

    if data['potassium'] < 5:
        warnings.append("⚠️ Potassium is too low.")
    elif data['potassium'] > 205:
        warnings.append("⚠️ Potassium is too high.")

    if data['temperature'] < 8 or data['temperature'] > 43:
        warnings.append("⚠️ Temperature out of optimal range.")

    if data['humidity'] < 14 or data['humidity'] > 100:
        warnings.append("⚠️ Humidity level is not ideal.")

    if data['ph'] < 3.5 or data['ph'] > 9.5:
        warnings.append("⚠️ pH level is too acidic or too basic.")

    if data['rainfall'] < 20 or data['rainfall'] > 300:
        warnings.append("⚠️ Rainfall amount is not suitable.")

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

        print(f"[DEBUG] Input Data: {input_data}")

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
        print(f"[DEBUG] Raw Prediction Output: {prediction}")

        try:
            crop_name = label_encoder.inverse_transform([prediction])[0]
        except Exception as e:
            print(f"[DEBUG] Label decode error: {e}")
            crop_name = str(prediction)

        return render_template(
            'crop-recommendation.html',
            prediction_text=f"🌱 Recommended Crop: {crop_name}",
            warnings=warnings
        )

    except Exception as e:
        print(f"[ERROR] Prediction error: {e}")
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