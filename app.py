from flask import Flask, render_template, request
import pickle
import numpy as np
import joblib

crop_model = joblib.load('crop_recommendation_model.pkl')
label_encoder = joblib.load('crop_label_encoder.pkl')
yield_model = joblib.load('farmhub_yeild_model.pkl')


app = Flask(__name__)

# Load ML models and label encoder
crop_model = pickle.load(open('crop_recommendation_model.pkl', 'rb'))
label_encoder = pickle.load(open('crop_label_encoder.pkl', 'rb'))
yield_model = pickle.load(open('farmhub_yeild_model.pkl', 'rb'))  # double-check spelling

@app.route('/')
def crop_form():
    return render_template('crop.html')

@app.route('/yield')
def yield_form():
    return render_template('yield.html')

@app.route('/predict_crop', methods=['POST'])
def predict_crop():
    nitrogen = float(request.form['nitrogen'])
    phosphorus = float(request.form['phosphorus'])
    potassium = float(request.form['potassium'])
    ph = float(request.form['ph'])

    features = np.array([[nitrogen, phosphorus, potassium, ph]])
    prediction = crop_model.predict(features)[0]
    crop_name = label_encoder.inverse_transform([prediction])[0]

    return render_template('crop.html', prediction_text=f"🌱 Recommended Crop: {crop_name}")

@app.route('/predict_yield', methods=['POST'])
def predict_yield():
    area = float(request.form['area'])
    rainfall = float(request.form['rainfall'])
    temperature = float(request.form['temperature'])

    features = np.array([[area, rainfall, temperature]])
    predicted_yield = yield_model.predict(features)[0]

    return render_template('yield.html', prediction_text=f"🌾 Expected Yield: {predicted_yield:.2f} tonnes")

if __name__ == '__main__':
    app.run(debug=True)
