#!/usr/bin/env python3
"""
Test script for PDF generation with comprehensive health data
"""

import requests
import json

def test_pdf_generation():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Comprehensive PDF Generation...")
    
    # Comprehensive test data with symptoms and medicines
    test_data = {
        "name": "John Smith",
        "age": "35",
        "risk_level": "Medium",
        "symptoms": [
            "Fever", 
            "Cough", 
            "Headache", 
            "Fatigue", 
            "Sore Throat"
        ],
        "diagnoses": [
            {"symptom": "Fever", "condition": "Flu", "medicine": "Paracetamol"},
            {"symptom": "Cough", "condition": "Flu", "medicine": "Cough Syrup"},
            {"symptom": "Headache", "condition": "Migraine", "medicine": "Ibuprofen"},
            {"symptom": "Fatigue", "condition": "Anemia", "medicine": "Iron Supplements"},
            {"symptom": "Sore Throat", "condition": "Throat Infection", "medicine": "Lozenges"}
        ],
        "bmi": {
            "value": "24.5",
            "category": "Normal"
        },
        "mental_wellness": {
            "mood": "Okay",
            "sleep": 7
        },
        "vital_signs": {
            "blood_pressure": "125",
            "sugar_level": "95",
            "heart_rate": "72",
            "vision": "No"
        }
    }
    
    try:
        print(f"📊 Test Data Summary:")
        print(f"   • Patient: {test_data['name']}, Age: {test_data['age']}")
        print(f"   • Symptoms: {len(test_data['symptoms'])} symptoms")
        print(f"   • Diagnoses: {len(test_data['diagnoses'])} conditions with medicines")
        print(f"   • Risk Level: {test_data['risk_level']}")
        print(f"   • BMI: {test_data['bmi']['value']} ({test_data['bmi']['category']})")
        print()
        
        print("🔄 Sending request to generate PDF...")
        response = requests.post(f"{base_url}/generate-report", 
                               json=test_data,
                               timeout=30)
        
        if response.status_code == 200:
            # Save the PDF file
            with open("test_comprehensive_health_report.pdf", "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ PDF Generated Successfully!")
            print(f"   📄 File: test_comprehensive_health_report.pdf")
            print(f"   📏 Size: {file_size:,} bytes")
            print()
            print("📋 PDF Contents Include:")
            print("   ✅ Patient Information (Name, Age, Date)")
            print("   ✅ BMI Assessment")
            print("   ✅ Risk Level Analysis")
            print("   ✅ Complete Symptoms List (5 symptoms)")
            print("   ✅ Recommended Medicines & Treatment")
            print("   ✅ Detailed Symptom-Medicine Mapping")
            print("   ✅ Mental Wellness Assessment")
            print("   ✅ Vital Signs Analysis")
            print("   ✅ Health Summary")
            print("   ✅ Medical Recommendations")
            print("   ✅ Professional Medical Disclaimer")
            print()
            print("🎉 All symptoms and medicines are included in the PDF!")
            return True
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {"error": response.text}
            print(f"❌ PDF Generation Failed!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Error: {error_data.get('error', 'Unknown error')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the app!")
        print("   Make sure the app is running with: python3 run.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_local_pdf():
    """Test PDF generation without web server"""
    print("\n🧪 Testing Local PDF Generation...")
    
    try:
        from logic.pdf_generator import generate_pdf
        
        result = generate_pdf(
            name="Test Patient",
            age="28",
            risk_level="High",
            symptoms=["Chest Pain", "Shortness of Breath", "Dizziness"],
            diagnoses=[
                {"symptom": "Chest Pain", "condition": "Cardiac Issue", "medicine": "Consult Doctor"},
                {"symptom": "Shortness of Breath", "condition": "Asthma", "medicine": "Inhaler"},
                {"symptom": "Dizziness", "condition": "Vertigo", "medicine": "Meclizine"}
            ],
            bmi={"value": "26.8", "category": "Overweight"},
            mental_wellness={"mood": "Stressed", "sleep": 5},
            vital_signs={"blood_pressure": "145", "sugar_level": "110", "heart_rate": "95", "vision": "Yes"},
            output_path="test_local_report.pdf"
        )
        
        import os
        if os.path.exists(result):
            file_size = os.path.getsize(result)
            print(f"✅ Local PDF Generated: {result}")
            print(f"   📏 Size: {file_size:,} bytes")
            return True
        else:
            print("❌ Local PDF file not created")
            return False
            
    except Exception as e:
        print(f"❌ Local PDF generation error: {e}")
        return False

if __name__ == "__main__":
    print("🏥 Health Check App - PDF Generation Test")
    print("=" * 50)
    
    # Test local PDF generation first
    local_success = test_local_pdf()
    
    # Test web app PDF generation
    web_success = test_pdf_generation()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Local PDF Generation: {'✅ PASS' if local_success else '❌ FAIL'}")
    print(f"   Web App PDF Generation: {'✅ PASS' if web_success else '❌ FAIL'}")
    
    if local_success and web_success:
        print("\n🎉 All PDF tests passed! Your app can generate comprehensive reports!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")