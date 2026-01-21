import pandas as pd

# Girdi ve çıktı dosya yolları
INPUT_PATH = "data/labeled/phishing.csv"
OUTPUT_PATH = "data/labeled/clean_phishing.csv"

print("Dataset okunuyor...")

# Dataseti oku
df = pd.read_csv(INPUT_PATH)

print("Orijinal sütunlar:")
print(df.columns)

# Gereksiz index sütununu sil
df = df.drop(columns=["Unnamed: 0"])

# Sütun isimlerini sadeleştir
df = df.rename(columns={
    "Email Text": "text",
    "Email Type": "label"
})

# Label'ı sayısal forma çevir
df["label"] = df["label"].map({
    "Safe Email": 0,
    "Phishing Email": 1
})

print("\nYeni sütunlar:")
print(df.columns)

print("\nLabel dağılımı:")
print(df["label"].value_counts())

# Temizlenmiş dosyayı kaydet
df.to_csv(OUTPUT_PATH, index=False)

print("\nTemiz dataset kaydedildi:", OUTPUT_PATH)
