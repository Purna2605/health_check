from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from logic.risk_classifier import classify_risk
from logic.pdf_generator import generate_pdf
from logic.hospital_finder import get_hospital_map_url
import os
import threading

app = Flask(__name__)
CORS(app)

# -------------------- REMINDER SYSTEM --------------------
reminders = []
reminder_lock = threading.Lock()

def validate_time_format(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# -------------------- BMI CALCULATOR --------------------
def calculate_bmi(height_cm, weight_kg):
    try:
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"
        return round(bmi, 2), category
    except Exception as e:
        return None, f"Error: {e}"

@app.route('/bmi', methods=['POST'])
def bmi():
    data = request.json
    height = data.get('height')
    weight = data.get('weight')
    if height is None or weight is None:
        return jsonify({"error": "Height and weight are required."}), 400
    bmi_value, category = calculate_bmi(height, weight)
    return jsonify({"bmi": bmi_value, "category": category})

# -------------------- SYMPTOM DIAGNOSIS --------------------
@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    symptoms = data.get('symptoms', [])
    symptom_map = {
        "Fever": ("Flu", "Paracetamol"),
        "Cough": ("Flu", "Cough Syrup"),
        "Headache": ("Migraine", "Ibuprofen"),
        "Sore Throat": ("Throat Infection", "Lozenges"),
        "Fatigue": ("Anemia", "Iron Supplements"),
        "Nausea": ("Food Poisoning", "Ondansetron"),
        "Vomiting": ("Food Poisoning", "Domperidone"),
        "Diarrhea": ("Infection", "ORS"),
        "Chest Pain": ("Cardiac Issue", "Consult Doctor"),
        "Shortness of Breath": ("Asthma", "Inhaler"),
        "Skin Rash": ("Allergy", "Antihistamine"),
        "Back Pain": ("Muscle Strain", "Pain Reliever"),
        "Dizziness": ("Vertigo", "Meclizine"),
        "Loss of Appetite": ("Gastric Issue", "Antacids"),
        "Joint Pain": ("Arthritis", "NSAIDs"),
        "Abdominal Pain": ("Ulcer", "Omeprazole"),
        "Constipation": ("Digestive Issue", "Laxative"),
        "Runny Nose": ("Cold", "Decongestant"),
        "Sneezing": ("Allergy", "Antihistamine"),
        "Itchy Eyes": ("Conjunctivitis", "Eye Drops"),
        "Swollen Glands": ("Infection", "Antibiotics"),
        "Muscle Aches": ("Viral Fever", "Paracetamol"),
        "Ear Pain": ("Ear Infection", "Antibiotics"),
        "Blurred Vision": ("Vision Issue", "Eye Exam"),
        "Palpitations": ("Heart Issue", "ECG Check"),
        "Fainting": ("Low BP", "Consult Doctor")
    }

    diagnoses = []
    for symptom in symptoms:
        diagnosis = symptom_map.get(symptom)
        if diagnosis:
            diagnoses.append({"symptom": symptom, "condition": diagnosis[0], "medicine": diagnosis[1]})
        else:
            diagnoses.append({"symptom": symptom, "condition": "Unknown", "medicine": "Consult Doctor"})

    return jsonify({"results": diagnoses})

# -------------------- MAIN ROUTES --------------------
@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')

@app.route("/test-pdf", methods=["GET"])
def test_pdf():
    with open('test_pdf_manual.html', 'r') as f:
        return f.read()

@app.route("/api", methods=["GET"])
def api_home():
    return "Welcome to the Health Check App Backend API!"

@app.route("/classify-risk", methods=["POST"])
def classify_risk_route():
    data = request.json
    symptoms = data.get("symptoms", [])
    if not isinstance(symptoms, list):
        return jsonify({"error": "Symptoms must be a list."}), 400
    try:
        risk = classify_risk(symptoms)
        return jsonify({"risk": risk})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate-report", methods=["POST"])
def generate_report_route():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        name = data.get("name", "N/A")
        age = data.get("age", "N/A")
        risk_level = data.get("risk_level", "Low")
        symptoms = data.get("symptoms", [])
        diagnoses = data.get("diagnoses", [])
        bmi = data.get("bmi")
        mental_wellness = data.get("mental_wellness")
        vital_signs = data.get("vital_signs")
        
        # Ensure symptoms and diagnoses are lists
        if not isinstance(symptoms, list):
            symptoms = []
        if not isinstance(diagnoses, list):
            diagnoses = []
        
        print(f"Generating PDF for {name} with {len(symptoms)} symptoms and {len(diagnoses)} diagnoses")
        
        file_path = generate_pdf(
            name=name,
            age=age,
            risk_level=risk_level,
            symptoms=symptoms,
            diagnoses=diagnoses,
            bmi=bmi,
            mental_wellness=mental_wellness,
            vital_signs=vital_signs
        )
        
        if not os.path.exists(file_path):
            return jsonify({"error": "PDF file was not created"}), 500
            
        return send_file(file_path, as_attachment=True, download_name="comprehensive_health_report.pdf")
    except ImportError as e:
        return jsonify({"error": "PDF library not available. Please install fpdf2: pip install fpdf2"}), 500
    except Exception as e:
        print(f"PDF generation error: {str(e)}")
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

@app.route("/find-hospitals", methods=["POST"])
def find_hospitals_route():
    data = request.json
    location = data.get("location", "India")
    try:
        url = get_hospital_map_url(location)
        return jsonify({"map_url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chatbot_route():
    user_message = request.json.get("message", "").lower()
    location = request.json.get("location", "India")
    response = ""
    try:
        if any(symptom in user_message for symptom in ["fever", "cough", "headache", "pain"]):
            symptoms = user_message.split()
            risk = classify_risk(symptoms)
            response = f"Based on your symptoms, your risk is: {risk.upper()}."
        elif "report" in user_message:
            response = "Your report is ready. You can download it from the main page."
        elif "hospital" in user_message or "nearby" in user_message:
            url = get_hospital_map_url(location)
            response = f"You can find nearby hospitals here: {url}"
        elif "water" in user_message:
            response = "Please drink a glass of water. Hydration is important!"
        elif "medicine" in user_message:
            response = "Make sure to take your prescribed medicine on time."
        else:
            response = "I'm your health assistant. Describe your symptoms or ask for a report/hospital/reminder."
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/set_reminder", methods=["POST"])
def set_reminder():
    data = request.json
    medicines = data.get("medicines", [])

    if not isinstance(medicines, list) or not medicines:
        return jsonify({"error": "Provide a list of medicines with name and time."}), 400

    added = []
    with reminder_lock:
        for med in medicines:
            name = med.get("name")
            time_str = med.get("time")
            if not name or not time_str:
                continue
            if not validate_time_format(time_str):
                continue
            reminders.append({
                "message": f"It's time to take your medicine: {name}",
                "time": time_str,
                "notified": False
            })
            added.append(f"{name} at {time_str}")

    if not added:
        return jsonify({"error": "No valid reminders added."}), 400

    return jsonify({"status": f"Reminders set for: {', '.join(added)}"})

@app.route("/get_reminders", methods=["GET"])
def get_reminders():
    now = datetime.now().strftime("%H:%M")
    due = []
    with reminder_lock:
        for r in reminders:
            if r["time"] == now and not r["notified"]:
                due.append(r["message"])
                r["notified"] = True
    return jsonify({"reminders": due})

# -------------------- SCHEDULER --------------------
def send_reminder():
    now = datetime.now().strftime("%H:%M")
    with reminder_lock:
        for r in reminders:
            if r["time"] == now and not r["notified"]:
                print(f"\U0001F514 Reminder: {r['message']} (Time: {now})")
                r["notified"] = True

scheduler = BackgroundScheduler()
scheduler.add_job(func=send_reminder, trigger="interval", seconds=60)
scheduler.start()

# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)