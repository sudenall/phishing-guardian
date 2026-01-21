import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import train_test_split

MODEL_PATH = "outputs/model_v2.joblib"
FEATURE_PATH = "data/labeled/features_v2.csv"

df = pd.read_csv(FEATURE_PATH)

X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = joblib.load(MODEL_PATH)

preds = model.predict(X_test)

cm = confusion_matrix(y_test, preds)

print("Confusion Matrix V2:")
print(cm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()

plt.title("Confusion Matrix V2")
plt.savefig("outputs/confusion_matrix_v2.png")

print("Grafik kaydedildi: outputs/confusion_matrix_v2.png")
