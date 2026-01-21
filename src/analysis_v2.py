import pandas as pd
import joblib
import matplotlib.pyplot as plt

MODEL_PATH = "outputs/model_v2.joblib"
FEATURE_PATH = "data/labeled/features_v2.csv"

print("Model ve veriler yükleniyor...")

model = joblib.load(MODEL_PATH)
df = pd.read_csv(FEATURE_PATH)

X = df.drop(columns=["label"])

importance = model.feature_importances_

importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": importance
}).sort_values(by="importance", ascending=False)

print("\nFEATURE IMPORTANCE (V2):")
print(importance_df)

plt.figure(figsize=(8, 6))
plt.barh(importance_df["feature"], importance_df["importance"])
plt.title("Feature Importance V2")
plt.xlabel("Importance")

plt.tight_layout()
plt.savefig("outputs/feature_importance_v2.png")

print("\nGrafik kaydedildi: outputs/feature_importance_v2.png")
