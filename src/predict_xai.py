import joblib
import shap
import pandas as pd
import numpy as np
from src.features_v2 import extract_features


MODEL_PATH = "outputs/model_v2.joblib"

print("Loading model...")
model = joblib.load(MODEL_PATH)

explainer = shap.TreeExplainer(model)


def explain_email(text):

    feats = extract_features(text)
    feature_vector = pd.DataFrame([feats])

    prediction = model.predict(feature_vector)[0]
    prob = model.predict_proba(feature_vector)[0][1]

    shap_vals = explainer.shap_values(feature_vector)

    if isinstance(shap_vals, list):
        values = shap_vals[1][0]
    else:
        values = shap_vals[0]

    explanation = []

    for i, col in enumerate(feature_vector.columns):
        impact = values[i]

        if isinstance(impact, (list, np.ndarray)):
            impact = float(np.array(impact).flatten()[0])
        else:
            impact = float(impact)

        explanation.append((col, feature_vector.iloc[0][col], impact))

    explanation = sorted(explanation, key=lambda x: abs(x[2]), reverse=True)

    print("\n=== RESULT ===")
    result = "PHISHING" if prediction == 1 else "SAFE"
    print("Decision:", result)
    print("Risk Score:", round(prob * 100, 2), "%")
    
    return result, prob, explanation


    print("\n=== EXPLANATION (XAI) ===")

    if result == "SAFE":
        print("\nFactors contributing to the email being classified as SAFE:")

        for feat, val, imp in explanation:
            if imp < 0:
                print(f"- {feat} = {val}  (impact: {imp:.4f})")

        print("\nFactors pushing the email towards PHISHING:")

        for feat, val, imp in explanation:
            if imp > 0:
                print(f"- {feat} = {val}  (impact: +{imp:.4f})")

    else:
        print("\nFactors contributing to the email being classified as PHISHING:")

        for feat, val, imp in explanation:
            if imp > 0:
                print(f"- {feat} = {val}  (impact: +{imp:.4f})")

        print("\nFactors pushing the email towards SAFE:")

        for feat, val, imp in explanation:
            if imp < 0:
                print(f"- {feat} = {val}  (impact: {imp:.4f})")


if __name__ == "__main__":
    email = input("Enter the email text to analyze:\n")
    explain_email(email)
