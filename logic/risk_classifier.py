def classify_risk(symptoms):
    """
    Classifies health risk based on symptoms.
    Returns: 'Low', 'Medium', or 'High'
    """
    if not symptoms:
        return "Low"
    
    # Convert to lowercase for case-insensitive matching
    symptoms = [symptom.lower() for symptom in symptoms]
    
    # High-risk symptoms
    high_risk_symptoms = [
        'chest pain', 'shortness of breath', 'fainting', 'palpitations', 
        'blurred vision', 'severe headache', 'high fever'
    ]
    
    # Medium-risk symptoms
    medium_risk_symptoms = [
        'fever', 'persistent cough', 'severe fatigue', 'vomiting', 
        'diarrhea', 'severe pain'
    ]
    
    # Check for high-risk symptoms
    for symptom in symptoms:
        if any(high_risk in symptom for high_risk in high_risk_symptoms):
            return "High"
    
    # Check for medium-risk symptoms or multiple symptoms
    medium_risk_count = 0
    for symptom in symptoms:
        if any(medium_risk in symptom for medium_risk in medium_risk_symptoms):
            medium_risk_count += 1
    
    if medium_risk_count >= 2 or len(symptoms) >= 4:
        return "High"
    elif medium_risk_count >= 1 or len(symptoms) >= 2:
        return "Medium"
    else:
        return "Low"