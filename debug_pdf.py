#!/usr/bin/env python3
"""
Debug PDF generation issues
"""

import sys
import traceback
from logic.pdf_generator import generate_pdf

def test_step_by_step():
    print("🔍 Debug PDF Generation Step by Step")
    print("=" * 50)
    
    # Test 1: Basic PDF
    print("\n1️⃣ Testing Basic PDF Generation...")
    try:
        result = generate_pdf("Test User", "25", "Low")
        print(f"✅ Basic PDF: {result}")
    except Exception as e:
        print(f"❌ Basic PDF failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 2: PDF with symptoms only
    print("\n2️⃣ Testing PDF with Symptoms...")
    try:
        result = generate_pdf(
            "Test User", "25", "Medium",
            symptoms=["Fever", "Cough", "Headache"]
        )
        print(f"✅ Symptoms PDF: {result}")
    except Exception as e:
        print(f"❌ Symptoms PDF failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 3: PDF with diagnoses
    print("\n3️⃣ Testing PDF with Diagnoses...")
    try:
        result = generate_pdf(
            "Test User", "25", "Medium",
            symptoms=["Fever", "Cough"],
            diagnoses=[
                {"symptom": "Fever", "condition": "Flu", "medicine": "Paracetamol"},
                {"symptom": "Cough", "condition": "Flu", "medicine": "Cough Syrup"}
            ]
        )
        print(f"✅ Diagnoses PDF: {result}")
    except Exception as e:
        print(f"❌ Diagnoses PDF failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 4: Full comprehensive PDF
    print("\n4️⃣ Testing Full Comprehensive PDF...")
    try:
        result = generate_pdf(
            name="John Doe",
            age="30",
            risk_level="Medium",
            symptoms=["Fever", "Cough", "Headache"],
            diagnoses=[
                {"symptom": "Fever", "condition": "Flu", "medicine": "Paracetamol"},
                {"symptom": "Cough", "condition": "Flu", "medicine": "Cough Syrup"},
                {"symptom": "Headache", "condition": "Migraine", "medicine": "Ibuprofen"}
            ],
            bmi={"value": "24.2", "category": "Normal"},
            mental_wellness={"mood": "Okay", "sleep": 7},
            vital_signs={
                "blood_pressure": "120",
                "sugar_level": "90", 
                "heart_rate": "75",
                "vision": "No"
            }
        )
        print(f"✅ Full PDF: {result}")
        
        # Check file size
        import os
        if os.path.exists(result):
            size = os.path.getsize(result)
            print(f"📄 File size: {size:,} bytes")
        
    except Exception as e:
        print(f"❌ Full PDF failed: {e}")
        traceback.print_exc()
        return False
    
    print("\n🎉 All PDF generation tests passed!")
    return True

def test_flask_route():
    print("\n🌐 Testing Flask Route...")
    try:
        # Import Flask app components
        from app import app
        
        # Create test client
        with app.test_client() as client:
            test_data = {
                "name": "Test User",
                "age": "25",
                "risk_level": "Medium",
                "symptoms": ["Fever", "Cough"],
                "diagnoses": [
                    {"symptom": "Fever", "condition": "Flu", "medicine": "Paracetamol"},
                    {"symptom": "Cough", "condition": "Flu", "medicine": "Cough Syrup"}
                ],
                "bmi": {"value": "24.2", "category": "Normal"},
                "mental_wellness": {"mood": "Okay", "sleep": 7},
                "vital_signs": {
                    "blood_pressure": "120",
                    "sugar_level": "90",
                    "heart_rate": "75", 
                    "vision": "No"
                }
            }
            
            print("📤 Sending POST request to /generate-report...")
            response = client.post('/generate-report', 
                                 json=test_data,
                                 content_type='application/json')
            
            print(f"📥 Response status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Flask route works!")
                print(f"📄 Response size: {len(response.data):,} bytes")
                
                # Save the PDF
                with open("flask_test_report.pdf", "wb") as f:
                    f.write(response.data)
                print("💾 PDF saved as flask_test_report.pdf")
                
            else:
                print(f"❌ Flask route failed!")
                try:
                    error_data = response.get_json()
                    print(f"Error: {error_data}")
                except:
                    print(f"Response text: {response.data.decode()}")
                    
    except Exception as e:
        print(f"❌ Flask test failed: {e}")
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("🏥 Health Check App - PDF Debug")
    print("Testing PDF generation functionality...")
    
    # Test PDF generation functions
    pdf_success = test_step_by_step()
    
    # Test Flask route
    flask_success = test_flask_route()
    
    print("\n" + "=" * 50)
    print("📊 Debug Results:")
    print(f"   PDF Generation: {'✅ WORKING' if pdf_success else '❌ BROKEN'}")
    print(f"   Flask Route: {'✅ WORKING' if flask_success else '❌ BROKEN'}")
    
    if pdf_success and flask_success:
        print("\n✅ PDF generation is working correctly!")
        print("If you're still having issues, please describe the specific error.")
    else:
        print("\n❌ Found issues with PDF generation.")
        print("Check the error messages above for details.")