import joblib
import re

MODEL_PATH = "outputs/model.joblib"

print("Model yükleniyor...")
model = joblib.load(MODEL_PATH)


def extract_features(text):
    features = {}

    text = str(text).lower()

    features["length"] = len(text)
    features["num_words"] = len(text.split())

    urls = re.findall(r"http[s]?://", text)
    features["num_urls"] = len(urls)

    suspicious_words = ["verify", "login", "urgent", "password", "bank", "account"]
    features["suspicious_words"] = sum(text.count(w) for w in suspicious_words)

    special_chars = len(re.findall(r"[^a-zA-Z0-9 ]", text))
    features["special_char_ratio"] = special_chars / (len(text) + 1)

    return features


def predict_email(text):
    print("\nTahmin yapılıyor...\n")

    feats = extract_features(text)

    feature_values = [[
        feats["length"],
        feats["num_words"],
        feats["num_urls"],
        feats["suspicious_words"],
        feats["special_char_ratio"]
    ]]

    prediction = model.predict(feature_values)[0]
    probability = model.predict_proba(feature_values)[0][1]

    result = "PHISHING" if prediction == 1 else "SAFE"

    print("=== SONUÇ ===")
    print("Karar:", result)
    print("Risk Skoru:", round(probability * 100, 2))

    print("\n=== Çıkarılan Özellikler ===")
    for k, v in feats.items():
        print(f"{k}: {v}")


print("\nÖrnek mail test ediliyor...")

sample = """
Dear customer,

Your bank account has been temporarily suspended.
Please verify your account immediately.

Click the link below to login and confirm your password:
http://fake-bank-login.com

Urgent action required!
"""

predict_email(sample)
