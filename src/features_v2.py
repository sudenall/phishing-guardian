import pandas as pd
import re

INPUT_PATH = "data/labeled/clean_phishing.csv"
OUTPUT_PATH = "data/labeled/features_v2.csv"

print("Dataset okunuyor...")
df = pd.read_csv(INPUT_PATH)

def extract_features(text):
    features = {}

    text = str(text).lower()

    features["length"] = len(text)
    words = text.split()
    features["num_words"] = len(words)

    # URL özellikleri
    urls = re.findall(r"http[s]?://", text)
    features["num_urls"] = len(urls)

    features["has_ip_url"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", text) else 0

    # Karakter tabanlı özellikler
    features["num_exclamations"] = text.count("!")
    features["num_dollars"] = text.count("$")
    features["num_percents"] = text.count("%")

    special_chars = len(re.findall(r"[^a-zA-Z0-9 ]", text))
    features["special_char_ratio"] = special_chars / (len(text) + 1)

    # Büyük harf oranı
    upper_chars = len(re.findall(r"[A-Z]", text))
    features["upper_ratio"] = upper_chars / (len(text) + 1)

    # Rakam oranı
    digits = len(re.findall(r"[0-9]", text))
    features["digit_ratio"] = digits / (len(text) + 1)

    # Kelime çeşitliliği
    features["unique_word_ratio"] = len(set(words)) / (len(words) + 1)

    # Şüpheli kelime sayıları
    suspicious_words = [
        "verify", "login", "urgent", "password",
        "bank", "account", "confirm", "click",
        "security", "update", "limited", "suspend"
    ]

    features["suspicious_words"] = sum(text.count(w) for w in suspicious_words)

    return features


print("Yeni özellikler çıkarılıyor...")

rows = []

for i, row in df.iterrows():
    feats = extract_features(row["text"])
    feats["label"] = row["label"]
    rows.append(feats)

new_df = pd.DataFrame(rows)

new_df.to_csv(OUTPUT_PATH, index=False)

print("Yeni feature dosyası oluşturuldu:", OUTPUT_PATH)
print("\nÖrnek satırlar:")
print(new_df.head())
