import pandas as pd

# Etiketli phishing dataset yolunu tanımla
path = "data/labeled/phishing.csv"

# Dosyayı oku
df = pd.read_csv(path)

print("==== DATASET BİLGİSİ ====")
print("Satır sayısı:", df.shape[0])
print("Sütun sayısı:", df.shape[1])

print("\nSütun isimleri:")
print(df.columns)

print("\nİlk 5 satır:")
print(df.head())

print("\nLabel dağılımı:")
# Label sütunu genelde son sütun olur
print(df.iloc[:, -1].value_counts())
