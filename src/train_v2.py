import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

INPUT_PATH = "data/labeled/features_v2.csv"
MODEL_PATH = "outputs/model_v2.joblib"

print("Yeni feature dataset okunuyor...")

df = pd.read_csv(INPUT_PATH)

X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Geliştirilmiş model eğitiliyor...")

model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

print("\nTest sonuçları:")
preds = model.predict(X_test)

print(classification_report(y_test, preds))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, preds))

joblib.dump(model, MODEL_PATH)

print("\nYeni model kaydedildi:", MODEL_PATH)
