
import pandas as pd

# Dosyayı sadece ilk 5 satırı okuyarak aç
df = pd.read_csv("data/emails.csv", nrows=5)

print("Sütun isimleri:")
print(df.columns)

print("\nİlk 5 satır:")
print(df)

# Dosyanın boyutunu tahmini görmek için
import os
size = os.path.getsize("data/emails.csv") / (1024 * 1024)
print("\nDosya boyutu (MB):", round(size, 2))
