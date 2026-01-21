import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split

MODEL_PATH = "outputs/model.joblib"
FEATURE_PATH = "data/labeled/features.csv"

print("V1 verileri yükleniyor...")

df = pd.read_csv(FEATURE_PATH)

X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = joblib.load(MODEL_PATH)

probs = model.predict_proba(X_test)[:, 1]

fpr, tpr, _ = roc_curve(y_test, probs)
roc_auc = auc(fpr, tpr)

print("ROC-AUC V1:", roc_auc)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.title("ROC Curve V1")
plt.legend()

plt.savefig("outputs/roc_curve_v1.png")

print("Grafik kaydedildi: outputs/roc_curve_v1.png")
