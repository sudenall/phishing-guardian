import pandas as pd
import re

INPUT_PATH = "data/labeled/clean_phishing.csv"
OUTPUT_PATH = "data/labeled/features.csv"

print("Temiz dataset okunuyor...")
df = pd.read_csv(INPUT_PATH)

def extract_features(text):
    features = {}

    text = str(text).lower()

    # Basit özellikler
    features["length"] = len(text)
    features["num_words"] = len(text.split())

    # URL sayısı
    urls = re.findall(r"http[s]?://", text)
    features["num_urls"] = len(urls)

    # Şüpheli kelime sayıları
    suspicious_words = ["verify", "login", "urgent", "password", "bank", "account"]
    features["suspicious_words"] = sum(text.count(w) for w in suspicious_words)

    # Özel karakter oranı
    special_chars = len(re.findall(r"[^a-zA-Z0-9 ]", text))
    features["special_char_ratio"] = special_chars / (len(text) + 1)

    return features


print("Özellikler çıkarılıyor...")

feature_rows = []

for index, row in df.iterrows():
    feats = extract_features(row["text"])
    feats["label"] = row["label"]
    feature_rows.append(feats)

features_df = pd.DataFrame(feature_rows)

features_df.to_csv(OUTPUT_PATH, index=False)

print("Özellik dosyası oluşturuldu:", OUTPUT_PATH)
print("\nİlk satırlar:")
print(features_df.head())
