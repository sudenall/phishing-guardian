import pandas as pd
import joblib
from features_v2 import extract_features

MODEL_PATH = "outputs/model_v2.joblib"
ENRON_PATH = "data/enron/emails.csv"

print("Model yükleniyor...")
model = joblib.load(MODEL_PATH)

print("Enron dataset okunuyor...")
df = pd.read_csv(ENRON_PATH)

print("Toplam mail sayısı:", len(df))

results = []

print("Mailler analiz ediliyor...")

for i, row in df.iterrows():
    text = str(row["message"])

    feats = extract_features(text)
    feature_vector = pd.DataFrame([feats])

    pred = model.predict(feature_vector)[0]
    prob = model.predict_proba(feature_vector)[0][1]

    results.append({
        "index": i,
        "prediction": "PHISHING" if pred == 1 else "SAFE",
        "risk_score": prob,
        "text_preview": text[:200]
    })

    if i % 1000 == 0:
        print(f"{i} mail işlendi...")

res_df = pd.DataFrame(results)

print("\n==== GENEL SONUÇLAR ====")
print(res_df["prediction"].value_counts())

res_df.to_csv("outputs/enron_predictions.csv", index=False)

print("\nSonuç dosyası oluşturuldu: outputs/enron_predictions.csv")
