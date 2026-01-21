import pandas as pd
import joblib
import shap
import numpy as np
from features_v2 import extract_features

MODEL_PATH = "outputs/model_v2.joblib"
RISKY_PATH = "outputs/most_risky_mails.csv"

print("Model yükleniyor...")
model = joblib.load(MODEL_PATH)

explainer = shap.TreeExplainer(model)

print("En riskli mailler okunuyor...")
df = pd.read_csv(RISKY_PATH)

reports = []

for i, row in df.iterrows():
    text = row["text_preview"]

    feats = extract_features(text)
    feature_vector = pd.DataFrame([feats])

    shap_vals = explainer.shap_values(feature_vector)

    if isinstance(shap_vals, list):
        values = shap_vals[1][0]
    else:
        values = shap_vals[0]

    explanation = []

    for j, col in enumerate(feature_vector.columns):
        impact = values[j]

        if isinstance(impact, (list, np.ndarray)):
            impact = float(np.array(impact).flatten()[0])
        else:
            impact = float(impact)

        explanation.append((col, impact))

    explanation = sorted(explanation, key=lambda x: abs(x[1]), reverse=True)

    top_reasons = explanation[:5]

    reason_text = "; ".join([f"{feat}:{imp:.3f}" for feat, imp in top_reasons])

    reports.append({
        "index": row["index"],
        "risk_score": row["risk_score"],
        "top_reasons": reason_text
    })

    print(f"{i+1}/50 mail açıklandı")

out = pd.DataFrame(reports)

out.to_csv("outputs/enron_xai_reports.csv", index=False)

print("\nXAI raporları oluşturuldu: outputs/enron_xai_reports.csv")
