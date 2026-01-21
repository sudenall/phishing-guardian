import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os
print("ANALYSIS DOSYASI ÇALIŞIYOR MU TESTİ")

MODEL_PATH = "outputs/model.joblib"
FEATURE_PATH = "data/labeled/features.csv"
OUTPUT_IMAGE = "outputs/feature_importance.png"

print("==== ANALYSIS BAŞLIYOR ====")

print("Dosyalar kontrol ediliyor...")

print("Model yolu:", MODEL_PATH, "var mı?", os.path.exists(MODEL_PATH))
print("Feature yolu:", FEATURE_PATH, "var mı?", os.path.exists(FEATURE_PATH))

print("\nModel yükleniyor...")
model = joblib.load(MODEL_PATH)

print("Feature dataset yükleniyor...")
df = pd.read_csv(FEATURE_PATH)

print("Dataset boyutu:", df.shape)

X = df.drop(columns=["label"])

feature_names = list(X.columns)
importances = model.feature_importances_

print("\nÖzellik önem değerleri hesaplandı:")

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

print("\n=== FEATURE IMPORTANCE TABLOSU ===")
print(importance_df)

print("\nGrafik oluşturuluyor...")

plt.figure(figsize=(8, 5))
plt.barh(importance_df["feature"], importance_df["importance"])
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Features")

plt.tight_layout()

plt.savefig(OUTPUT_IMAGE)

print("\nGrafik başarıyla kaydedildi:")
print(OUTPUT_IMAGE)

print("\n==== ANALYSIS BİTTİ ====")


