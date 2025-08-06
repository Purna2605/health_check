try:
    from fpdf import FPDF
except ImportError:
    # Fallback if fpdf is not available
    print("Warning: fpdf not available. Install with: pip install fpdf2")
    FPDF = None

import os
from datetime import datetime

def generate_pdf(name, age, risk_level, output_path=None):
    """
    Generates a PDF health report.
    Args:
        name: Patient name
        age: Patient age
        risk_level: Risk level (Low/Medium/High)
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
    pdf.set_font("Arial", size=16)
    
    # Title
    pdf.cell(200, 10, txt="Health Risk Report", ln=True, align='C')
    pdf.ln(10)
    
    # Patient information
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    
    # Risk level
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(200, 10, txt=f"Risk Level: {risk_level}", ln=True)
    pdf.ln(10)
    
    # Additional information
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="This report is generated based on the symptoms provided.", ln=True)
    pdf.cell(200, 10, txt="Please consult with a healthcare professional for proper diagnosis.", ln=True)
    pdf.cell(200, 10, txt="This is not a substitute for professional medical advice.", ln=True)
    
    # Save the PDF
    pdf.output(output_path)
    return output_path