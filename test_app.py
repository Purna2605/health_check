#!/usr/bin/env python3
"""
Simple test script to verify the Health Check App functionality
"""

import requests
import json
import time

def test_app():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Health Check App...")
    
    # Test 1: Check if app is running
    try:
        response = requests.get(f"{base_url}/api")
        print(f"✅ App is running: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ App is not running. Please start with 'python3 app.py'")
        return False
    
    # Test 2: BMI calculation
    try:
        bmi_data = {"height": 170, "weight": 70}
        response = requests.post(f"{base_url}/bmi", json=bmi_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ BMI Test: BMI = {result['bmi']}, Category = {result['category']}")
        else:
            print("❌ BMI Test failed")
    except Exception as e:
        print(f"❌ BMI Test error: {e}")
    
    # Test 3: Symptom diagnosis
    try:
        symptoms_data = {"symptoms": ["Fever", "Cough", "Headache"]}
        response = requests.post(f"{base_url}/diagnose", json=symptoms_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Symptom Diagnosis Test: Found {len(result['results'])} diagnoses")
        else:
            print("❌ Symptom Diagnosis Test failed")
    except Exception as e:
        print(f"❌ Symptom Diagnosis Test error: {e}")
    
    # Test 4: Risk classification
    try:
        risk_data = {"symptoms": ["Chest Pain", "Shortness of Breath"]}
        response = requests.post(f"{base_url}/classify-risk", json=risk_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Risk Classification Test: Risk Level = {result['risk']}")
        else:
            print("❌ Risk Classification Test failed")
    except Exception as e:
        print(f"❌ Risk Classification Test error: {e}")
    
    # Test 5: Hospital finder
    try:
        hospital_data = {"location": "New York"}
        response = requests.post(f"{base_url}/find-hospitals", json=hospital_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Hospital Finder Test: Generated URL for New York")
        else:
            print("❌ Hospital Finder Test failed")
    except Exception as e:
        print(f"❌ Hospital Finder Test error: {e}")
    
    # Test 6: Medicine reminder
    try:
        reminder_data = {"medicines": [{"name": "Aspirin", "time": "08:00"}]}
        response = requests.post(f"{base_url}/set_reminder", json=reminder_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Medicine Reminder Test: {result['status']}")
        else:
            print("❌ Medicine Reminder Test failed")
    except Exception as e:
        print(f"❌ Medicine Reminder Test error: {e}")
    
    # Test 7: Comprehensive PDF Report
    try:
        report_data = {
            "name": "John Doe",
            "age": "30",
            "risk_level": "Medium",
            "symptoms": ["Fever", "Cough", "Headache"],
            "diagnoses": [
                {"symptom": "Fever", "condition": "Flu", "medicine": "Paracetamol"},
                {"symptom": "Cough", "condition": "Flu", "medicine": "Cough Syrup"},
                {"symptom": "Headache", "condition": "Migraine", "medicine": "Ibuprofen"}
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
        response = requests.post(f"{base_url}/generate-report", json=report_data)
        if response.status_code == 200:
            print("✅ Comprehensive PDF Report Test: Report generated successfully")
            # Save test report
            with open("test_health_report.pdf", "wb") as f:
                f.write(response.content)
            print("   📄 Test report saved as 'test_health_report.pdf'")
        else:
            print("❌ PDF Report Test failed")
    except Exception as e:
        print(f"❌ PDF Report Test error: {e}")

    print("\n🎉 All tests completed!")
    print(f"📱 Visit {base_url} in your browser to use the app")
    print("📄 The PDF report now includes:")
    print("   • Selected symptoms")
    print("   • Recommended medicines for each condition")
    print("   • BMI assessment")
    print("   • Mental wellness data")
    print("   • Vital signs")
    print("   • Risk-based recommendations")
    return True

if __name__ == "__main__":
    test_app()