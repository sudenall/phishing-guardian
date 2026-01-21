import joblib
import pandas as pd
import shap
import numpy as np

MODEL_PATH = "outputs/model_v2.joblib"
FEATURE_PATH = "data/labeled/features_v2.csv"

print("Model yükleniyor...")

model = joblib.load(MODEL_PATH)

print("Dataset okunuyor...")
df = pd.read_csv(FEATURE_PATH)

X = df.drop(columns=["label"])

sample_index = 5
sample = X.iloc[[sample_index]]

print("SHAP Explainer oluşturuluyor...")
explainer = shap.TreeExplainer(model)

print("Sadece seçilen örnek için SHAP hesaplanıyor...")
shap_values = explainer.shap_values(sample)

print("\nÖrnek mail için açıklama:\n")

feature_names = list(X.columns)
sample_features = sample.iloc[0]

# SHAP çıktısının formatını güvenli şekilde al
if isinstance(shap_values, list):
    values = shap_values[1][0]
else:
    values = shap_values[0]

explanation = []

for i, feature in enumerate(feature_names):
    value = sample_features.iloc[i]

    # impact değerini tek sayıya indir
    impact = values[i]

    if isinstance(impact, (list, np.ndarray)):
        impact = float(np.array(impact).flatten()[0])
    else:
        impact = float(impact)

    effect = "PHISHING'e yönlendiriyor" if impact > 0 else "SAFE'e yönlendiriyor"

    explanation.append((feature, value, impact, effect))

explanation = sorted(explanation, key=lambda x: abs(x[2]), reverse=True)

for feat, val, imp, eff in explanation[:10]:
    print(f"{feat} = {val}  --> etki: {imp:.4f}  ({eff})")

print("\nXAI açıklama tamamlandı.")
