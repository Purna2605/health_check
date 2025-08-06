try:
    from fpdf import FPDF
except ImportError:
    # Fallback if fpdf is not available
    print("Warning: fpdf not available. Install with: pip install fpdf2")
    FPDF = None

import os
from datetime import datetime

def generate_pdf(name, age, risk_level, symptoms=None, diagnoses=None, bmi=None, 
                mental_wellness=None, vital_signs=None, output_path=None):
    """
    Generates a comprehensive PDF health report.
    Args:
        name: Patient name
        age: Patient age
        risk_level: Risk level (Low/Medium/High)
        symptoms: List of selected symptoms
        diagnoses: List of diagnosis results with conditions and medicines
        bmi: BMI information (value and category)
        mental_wellness: Mental wellness data (mood, sleep)
        vital_signs: Vital signs data (BP, sugar, heart rate)
        output_path: Optional custom output path
    Returns:
        Path to the generated PDF file
    """
    if FPDF is None:
        raise ImportError("fpdf2 library is required. Install with: pip install fpdf2")
    
    if output_path is None:
        output_path = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", size=18)
    pdf.cell(200, 15, txt="HEALTH ASSESSMENT REPORT", ln=True, align='C')
    pdf.ln(5)
    
    # Patient information
    pdf.set_font("Helvetica", "B", size=14)
    pdf.cell(200, 10, txt="PATIENT INFORMATION", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 8, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 8, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 8, txt=f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    
    # BMI Information
    if bmi:
        pdf.set_font("Helvetica", "B", size=14)
        pdf.cell(200, 10, txt="BMI ASSESSMENT", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        pdf.set_font("Helvetica", size=12)
        pdf.cell(200, 8, txt=f"BMI Value: {bmi.get('value', 'N/A')}", ln=True)
        pdf.cell(200, 8, txt=f"Category: {bmi.get('category', 'N/A')}", ln=True)
        pdf.ln(5)
    
    # Risk Level
    pdf.set_font("Helvetica", "B", size=14)
    pdf.cell(200, 10, txt="RISK ASSESSMENT", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", size=12)
    pdf.cell(200, 8, txt=f"Risk Level: {risk_level}", ln=True)
    pdf.ln(5)
    
    # Symptoms and Diagnosis - This is the main section you wanted!
    if symptoms or diagnoses:
        pdf.set_font("Helvetica", "B", size=14)
        pdf.cell(200, 10, txt="SYMPTOMS & TREATMENT PLAN", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        if symptoms:
            pdf.set_font("Helvetica", "B", size=12)
            pdf.cell(200, 8, txt="Selected Symptoms:", ln=True)
            pdf.set_font("Helvetica", size=11)
            
            # Display symptoms clearly numbered
            for i, symptom in enumerate(symptoms, 1):
                pdf.cell(200, 6, txt=f"  {i}. {symptom}", ln=True)
            pdf.ln(3)
        
        if diagnoses:
            pdf.set_font("Helvetica", "B", size=12)
            pdf.cell(200, 8, txt="Recommended Medicines & Treatment:", ln=True)
            pdf.set_font("Helvetica", size=11)
            
            # Group diagnoses by condition and show all medicines
            condition_medicines = {}
            for diagnosis in diagnoses:
                condition = diagnosis.get('condition', 'Unknown')
                medicine = diagnosis.get('medicine', 'Consult Doctor')
                if condition not in condition_medicines:
                    condition_medicines[condition] = set()
                condition_medicines[condition].add(medicine)
            
            for i, (condition, medicines) in enumerate(condition_medicines.items(), 1):
                pdf.cell(200, 6, txt=f"  {i}. Condition: {condition}", ln=True)
                for medicine in medicines:
                    pdf.cell(200, 5, txt=f"     - Medicine: {medicine}", ln=True)
                pdf.ln(2)
        
        # Add detailed symptom-medicine mapping
        if diagnoses:
            pdf.set_font("Helvetica", "B", size=12)
            pdf.cell(200, 8, txt="Detailed Symptom-Medicine Mapping:", ln=True)
            pdf.set_font("Helvetica", size=10)
            
            for i, diagnosis in enumerate(diagnoses, 1):
                symptom = diagnosis.get('symptom', 'Unknown')
                condition = diagnosis.get('condition', 'Unknown')
                medicine = diagnosis.get('medicine', 'Consult Doctor')
                pdf.cell(200, 5, txt=f"  {i}. {symptom} -> {condition} -> {medicine}", ln=True)
            pdf.ln(5)
    
    # Mental Wellness
    if mental_wellness:
        pdf.set_font("Helvetica", "B", size=14)
        pdf.cell(200, 10, txt="MENTAL WELLNESS", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        pdf.set_font("Helvetica", size=12)
        mood = mental_wellness.get('mood', 'N/A')
        sleep = mental_wellness.get('sleep', 'N/A')
        pdf.cell(200, 8, txt=f"Current Mood: {mood}", ln=True)
        pdf.cell(200, 8, txt=f"Sleep Duration: {sleep} hours per night", ln=True)
        
        # Add mental health recommendations
        pdf.set_font("Helvetica", "B", size=11)
        pdf.cell(200, 6, txt="Mental Health Recommendations:", ln=True)
        pdf.set_font("Helvetica", size=10)
        if mood == "Stressed":
            pdf.cell(200, 5, txt="  - Practice relaxation techniques", ln=True)
            pdf.cell(200, 5, txt="  - Consider stress management counseling", ln=True)
        if isinstance(sleep, (int, float)) and sleep < 7:
            pdf.cell(200, 5, txt="  - Aim for 7-9 hours of sleep per night", ln=True)
            pdf.cell(200, 5, txt="  - Establish a regular sleep schedule", ln=True)
        pdf.ln(5)
    
    # Vital Signs
    if vital_signs:
        pdf.set_font("Helvetica", "B", size=14)
        pdf.cell(200, 10, txt="VITAL SIGNS", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        pdf.set_font("Helvetica", size=12)
        bp = vital_signs.get('blood_pressure', 'N/A')
        sugar = vital_signs.get('sugar_level', 'N/A')
        hr = vital_signs.get('heart_rate', 'N/A')
        vision = vital_signs.get('vision', 'N/A')
        
        pdf.cell(200, 8, txt=f"Blood Pressure: {bp} mmHg", ln=True)
        pdf.cell(200, 8, txt=f"Blood Sugar Level: {sugar} mg/dL", ln=True)
        pdf.cell(200, 8, txt=f"Heart Rate: {hr} bpm", ln=True)
        pdf.cell(200, 8, txt=f"Vision Issues: {vision}", ln=True)
        
        # Add vital signs analysis
        pdf.set_font("Helvetica", "B", size=11)
        pdf.cell(200, 6, txt="Vital Signs Analysis:", ln=True)
        pdf.set_font("Helvetica", size=10)
        
        try:
            if bp != 'N/A' and bp.isdigit():
                bp_val = int(bp)
                if bp_val > 140:
                    pdf.cell(200, 5, txt="  - Blood pressure is HIGH - consult doctor immediately", ln=True)
                elif bp_val < 90:
                    pdf.cell(200, 5, txt="  - Blood pressure is LOW - monitor closely", ln=True)
                else:
                    pdf.cell(200, 5, txt="  - Blood pressure is within normal range", ln=True)
            
            if sugar != 'N/A' and sugar.isdigit():
                sugar_val = int(sugar)
                if sugar_val > 180:
                    pdf.cell(200, 5, txt="  - Blood sugar is HIGH - consult doctor", ln=True)
                elif sugar_val < 70:
                    pdf.cell(200, 5, txt="  - Blood sugar is LOW - monitor closely", ln=True)
                else:
                    pdf.cell(200, 5, txt="  - Blood sugar is within normal range", ln=True)
        except:
            pass
        
        pdf.ln(5)
    
    # Comprehensive Health Summary
    pdf.set_font("Helvetica", "B", size=14)
    pdf.cell(200, 10, txt="HEALTH SUMMARY", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Helvetica", size=11)
    if symptoms:
        pdf.cell(200, 6, txt=f"Total Symptoms Reported: {len(symptoms)}", ln=True)
    if diagnoses:
        conditions = set(d.get('condition', 'Unknown') for d in diagnoses)
        medicines = set(d.get('medicine', 'Unknown') for d in diagnoses)
        pdf.cell(200, 6, txt=f"Medical Conditions Identified: {len(conditions)}", ln=True)
        pdf.cell(200, 6, txt=f"Medicines Recommended: {len(medicines)}", ln=True)
    
    pdf.ln(5)
    
    # Recommendations based on risk level
    pdf.set_font("Helvetica", "B", size=14)
    pdf.cell(200, 10, txt="MEDICAL RECOMMENDATIONS", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Helvetica", size=11)
    recommendations = []
    
    if risk_level == "High":
        recommendations.extend([
            "- Seek immediate medical attention from a healthcare provider",
            "- Contact your doctor or visit emergency room if symptoms worsen",
            "- Monitor symptoms closely and keep a symptom diary",
            "- Take prescribed medications as directed"
        ])
    elif risk_level == "Medium":
        recommendations.extend([
            "- Schedule an appointment with your doctor within 1-2 days",
            "- Monitor symptoms for any changes or worsening",
            "- Follow prescribed medication regimen carefully",
            "- Rest and stay hydrated"
        ])
    else:
        recommendations.extend([
            "- Maintain regular health check-ups with your doctor",
            "- Continue healthy lifestyle habits",
            "- Stay hydrated and get adequate rest",
            "- Monitor for any new or worsening symptoms"
        ])
    
    recommendations.extend([
        "- Take all medications as prescribed by your healthcare provider",
        "- Follow up with your doctor as recommended",
        "- Keep track of any symptom changes or new symptoms",
        "- Maintain a healthy diet and regular exercise routine"
    ])
    
    for rec in recommendations:
        pdf.cell(200, 6, txt=rec, ln=True)
    
    pdf.ln(10)
    
    # Disclaimer
    pdf.set_font("Helvetica", "B", size=12)
    pdf.cell(200, 8, txt="IMPORTANT MEDICAL DISCLAIMER", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(200, 5, txt="This report is generated based on the symptoms and information provided.", ln=True)
    pdf.cell(200, 5, txt="It is for informational purposes only and is NOT a substitute for professional", ln=True)
    pdf.cell(200, 5, txt="medical advice, diagnosis, or treatment. Always seek the advice of your physician", ln=True)
    pdf.cell(200, 5, txt="or other qualified healthcare provider with any questions you may have regarding", ln=True)
    pdf.cell(200, 5, txt="a medical condition. Never disregard professional medical advice or delay seeking", ln=True)
    pdf.cell(200, 5, txt="it because of something you have read in this report.", ln=True)
    
    # Save the PDF
    try:
        pdf.output(output_path)
        return output_path
    except Exception as e:
        raise Exception(f"Failed to save PDF: {str(e)}")