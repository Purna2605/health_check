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
    pdf.set_font("Arial", "B", size=18)
    pdf.cell(200, 15, txt="HEALTH ASSESSMENT REPORT", ln=True, align='C')
    pdf.ln(5)
    
    # Patient information
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(200, 10, txt="PATIENT INFORMATION", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 8, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 8, txt=f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    
    # BMI Information
    if bmi:
        pdf.set_font("Arial", "B", size=14)
        pdf.cell(200, 10, txt="BMI ASSESSMENT", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, txt=f"BMI Value: {bmi.get('value', 'N/A')}", ln=True)
        pdf.cell(200, 8, txt=f"Category: {bmi.get('category', 'N/A')}", ln=True)
        pdf.ln(5)
    
    # Risk Level
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(200, 10, txt="RISK ASSESSMENT", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", size=12)
    risk_color = (255, 0, 0) if risk_level == "High" else (255, 165, 0) if risk_level == "Medium" else (0, 128, 0)
    pdf.set_text_color(*risk_color)
    pdf.cell(200, 8, txt=f"Risk Level: {risk_level}", ln=True)
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.ln(5)
    
    # Symptoms and Diagnosis
    if symptoms or diagnoses:
        pdf.set_font("Arial", "B", size=14)
        pdf.cell(200, 10, txt="SYMPTOMS & DIAGNOSIS", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        if symptoms:
            pdf.set_font("Arial", "B", size=12)
            pdf.cell(200, 8, txt="Selected Symptoms:", ln=True)
            pdf.set_font("Arial", size=11)
            
            # Display symptoms in a formatted way
            for i, symptom in enumerate(symptoms, 1):
                pdf.cell(200, 6, txt=f"  {i}. {symptom}", ln=True)
            pdf.ln(3)
        
        if diagnoses:
            pdf.set_font("Arial", "B", size=12)
            pdf.cell(200, 8, txt="Recommended Treatment:", ln=True)
            pdf.set_font("Arial", size=11)
            
            # Group diagnoses by condition
            condition_medicines = {}
            for diagnosis in diagnoses:
                condition = diagnosis.get('condition', 'Unknown')
                medicine = diagnosis.get('medicine', 'Consult Doctor')
                if condition not in condition_medicines:
                    condition_medicines[condition] = set()
                condition_medicines[condition].add(medicine)
            
            for i, (condition, medicines) in enumerate(condition_medicines.items(), 1):
                pdf.cell(200, 6, txt=f"  {i}. {condition}:", ln=True)
                for medicine in medicines:
                    pdf.cell(200, 5, txt=f"     • {medicine}", ln=True)
                pdf.ln(2)
    
    # Mental Wellness
    if mental_wellness:
        pdf.set_font("Arial", "B", size=14)
        pdf.cell(200, 10, txt="MENTAL WELLNESS", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        pdf.set_font("Arial", size=12)
        mood = mental_wellness.get('mood', 'N/A')
        sleep = mental_wellness.get('sleep', 'N/A')
        pdf.cell(200, 8, txt=f"Mood: {mood}", ln=True)
        pdf.cell(200, 8, txt=f"Sleep Duration: {sleep} hours", ln=True)
        pdf.ln(5)
    
    # Vital Signs
    if vital_signs:
        pdf.set_font("Arial", "B", size=14)
        pdf.cell(200, 10, txt="VITAL SIGNS", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        pdf.set_font("Arial", size=12)
        bp = vital_signs.get('blood_pressure', 'N/A')
        sugar = vital_signs.get('sugar_level', 'N/A')
        hr = vital_signs.get('heart_rate', 'N/A')
        vision = vital_signs.get('vision', 'N/A')
        
        pdf.cell(200, 8, txt=f"Blood Pressure: {bp} mmHg", ln=True)
        pdf.cell(200, 8, txt=f"Sugar Level: {sugar} mg/dL", ln=True)
        pdf.cell(200, 8, txt=f"Heart Rate: {hr} bpm", ln=True)
        pdf.cell(200, 8, txt=f"Vision Issues: {vision}", ln=True)
        pdf.ln(5)
    
    # Recommendations
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(200, 10, txt="RECOMMENDATIONS", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", size=11)
    recommendations = []
    
    if risk_level == "High":
        recommendations.extend([
            "• Seek immediate medical attention",
            "• Contact your healthcare provider today",
            "• Monitor symptoms closely"
        ])
    elif risk_level == "Medium":
        recommendations.extend([
            "• Schedule an appointment with your doctor",
            "• Monitor symptoms for changes",
            "• Follow prescribed medications"
        ])
    else:
        recommendations.extend([
            "• Maintain regular health check-ups",
            "• Continue healthy lifestyle habits",
            "• Stay hydrated and get adequate rest"
        ])
    
    recommendations.extend([
        "• Take medications as prescribed",
        "• Follow up with healthcare provider as needed",
        "• Keep track of any symptom changes"
    ])
    
    for rec in recommendations:
        pdf.cell(200, 6, txt=rec, ln=True)
    
    pdf.ln(10)
    
    # Disclaimer
    pdf.set_font("Arial", "I", size=10)
    pdf.cell(200, 6, txt="DISCLAIMER:", ln=True)
    pdf.cell(200, 5, txt="This report is generated based on the symptoms and information provided.", ln=True)
    pdf.cell(200, 5, txt="It is for informational purposes only and not a substitute for professional", ln=True)
    pdf.cell(200, 5, txt="medical advice, diagnosis, or treatment. Always consult with a qualified", ln=True)
    pdf.cell(200, 5, txt="healthcare professional for proper medical evaluation and treatment.", ln=True)
    
    # Save the PDF
    pdf.output(output_path)
    return output_path