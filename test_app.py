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
    
    print("\n🎉 All tests completed!")
    print(f"📱 Visit {base_url} in your browser to use the app")
    return True

if __name__ == "__main__":
    test_app()