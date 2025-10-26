# disease_prediction.py

# Mapping of symptoms to diseases and recommendations
disease_data = {
    "fever": {
        "disease": "Common Cold",
        "description": "A viral infection causing sneezing, runny nose, and fever.",
        "prevention": "Wash hands regularly, avoid close contact with infected people.",
        "diet": "Drink warm fluids, eat fruits rich in Vitamin C.",
        "exercise": "Light stretching or walking if possible."
    },
    "cough": {
        "disease": "Bronchitis",
        "description": "Inflammation of the bronchial tubes causing coughing and mucus production.",
        "prevention": "Avoid smoking, stay hydrated.",
        "diet": "Warm soups, herbal teas.",
        "exercise": "Deep breathing exercises."
    },
    "headache": {
        "disease": "Migraine",
        "description": "Severe headache often accompanied by nausea, light sensitivity, and vomiting.",
        "prevention": "Avoid triggers like stress, loud noises, and certain foods.",
        "diet": "Eat regular meals, stay hydrated.",
        "exercise": "Gentle yoga or meditation."
    },
    "skin_rash": {
        "disease": "Eczema",
        "description": "A condition causing inflamed, itchy, and cracked skin.",
        "prevention": "Use gentle soaps, moisturize regularly, avoid allergens.",
        "diet": "Omega-3 rich foods like fish and flaxseeds.",
        "exercise": "Low-impact activities to avoid sweating."
    },
    "fatigue": {
        "disease": "Anemia",
        "description": "A condition characterized by low red blood cell count leading to fatigue.",
        "prevention": "Eat iron-rich foods, treat underlying causes.",
        "diet": "Leafy greens, lean meats, beans.",
        "exercise": "Light aerobic activities like walking."
    },
    "shortness_of_breath": {
        "disease": "Asthma",
        "description": "Chronic inflammation of the airways causing difficulty breathing.",
        "prevention": "Avoid allergens, manage stress.",
        "diet": "Anti-inflammatory foods like ginger and turmeric.",
        "exercise": "Breathing exercises or swimming."
    },
    "chest_pain": {
        "disease": "Angina",
        "description": "Chest pain caused by reduced blood flow to the heart.",
        "prevention": "Maintain a healthy weight, avoid high-fat diets.",
        "diet": "Low-fat, heart-healthy foods.",
        "exercise": "Light walking or guided cardiac rehabilitation exercises."
    },
    "itching": {
        "disease": "Fungal Infection",
        "description": "A skin infection caused by fungi, leading to itching and redness.",
        "prevention": "Keep skin clean and dry, avoid sharing personal items.",
        "diet": "Probiotic-rich foods like yogurt.",
        "exercise": "Avoid activities causing excessive sweating."
    },
    "sore_throat": {
        "disease": "Pharyngitis",
        "description": "Inflammation of the throat causing pain and discomfort.",
        "prevention": "Avoid cold drinks, stay hydrated.",
        "diet": "Warm teas with honey, soups.",
        "exercise": "Rest and avoid strenuous activities."
    },
    "joint_pain": {
        "disease": "Arthritis",
        "description": "Inflammation of joints causing pain and stiffness.",
        "prevention": "Maintain a healthy weight, stay active.",
        "diet": "Foods rich in omega-3 fatty acids.",
        "exercise": "Low-impact exercises like swimming or cycling."
    },
    "vomiting": {
        "disease": "Gastroenteritis",
        "description": "Inflammation of the stomach and intestines causing vomiting and diarrhea.",
        "prevention": "Avoid contaminated food and water.",
        "diet": "Eat bananas, rice, applesauce, and toast (BRAT diet).",
        "exercise": "Rest and avoid physical activities."
    },
    "runny_nose": {
        "disease": "Allergic Rhinitis",
        "description": "An allergic reaction causing sneezing, runny nose, and congestion.",
        "prevention": "Avoid allergens like dust and pollen.",
        "diet": "Foods rich in Vitamin C to boost immunity.",
        "exercise": "Indoor activities during high pollen seasons."
    },
    "dizziness": {
        "disease": "Vertigo",
        "description": "A sensation of spinning or loss of balance caused by inner ear issues.",
        "prevention": "Avoid sudden movements, stay hydrated.",
        "diet": "Reduce salt intake to prevent fluid retention.",
        "exercise": "Balance exercises and physical therapy."
    },
    "nausea": {
        "disease": "Motion Sickness",
        "description": "A condition causing nausea due to movement during travel.",
        "prevention": "Avoid heavy meals before traveling, focus on a fixed point.",
        "diet": "Ginger tea or peppermint.",
        "exercise": "Focus on deep breathing exercises."
    },
    "blurred_vision": {
        "disease": "Glaucoma",
        "description": "A condition leading to increased pressure in the eyes, affecting vision.",
        "prevention": "Regular eye check-ups, avoid eye strain.",
        "diet": "Foods rich in antioxidants like carrots and spinach.",
        "exercise": "Walking or yoga to reduce stress."
    }
}

def predict_disease(symptom):
    if symptom in disease_data:
        return disease_data[symptom]
    return {"error": "No matching disease found for the given symptom."}

if __name__ == "__main__":
    symptom = input("Enter your symptom: ").lower()
    result = predict_disease(symptom)
    for key, value in result.items():
        print(f"{key.capitalize()}: {value}")