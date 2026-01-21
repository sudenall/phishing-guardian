import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("outputs", exist_ok=True)

print("Enron tahmin sonuçları okunuyor...")

df = pd.read_csv("outputs/enron_predictions.csv")

print("\n==== GENEL İSTATİSTİKLER ====")
print(df["prediction"].value_counts())

# 1) Pie Chart - Safe vs Phishing
counts = df["prediction"].value_counts()

plt.figure(figsize=(6,6))
plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
plt.title("Safe vs Phishing Ratio (Enron)")
plt.savefig("outputs/enron_pie_chart.png")
plt.close()

print("Pasta grafiği oluşturuldu: enron_pie_chart.png")

# 2) Risk Score Histogram
plt.figure(figsize=(10,6))
plt.hist(df["risk_score"], bins=50)
plt.title("Enron Mail Risk Score Distribution")
plt.xlabel("Risk Score")
plt.ylabel("Mail Count")
plt.savefig("outputs/enron_risk_distribution.png")
plt.close()

print("Risk dağılım grafiği oluşturuldu: enron_risk_distribution.png")

# 3) High Risk Ratio Chart
high_risk_ratio = len(df[df["risk_score"] > 0.8]) / len(df)

plt.figure(figsize=(6,4))
plt.bar(["High Risk (>0.8)", "Others"], [high_risk_ratio, 1 - high_risk_ratio])
plt.title("High Risk Mail Ratio")
plt.savefig("outputs/high_risk_ratio.png")
plt.close()

print("Yüksek risk oran grafiği oluşturuldu: high_risk_ratio.png")

# 4) Top Risky Mails
top_risky = df.sort_values(by="risk_score", ascending=False).head(100)

top_risky.to_csv("outputs/most_risky_mails.csv", index=False)

print("\nEn riskli 100 mail kaydedildi: outputs/most_risky_mails.csv")

# 5) High Risk List
high_risk = df[df["risk_score"] > 0.8]

print("\nRisk skoru 0.8 üzeri mail sayısı:", len(high_risk))

high_risk.to_csv("outputs/high_risk_mails.csv", index=False)

print("Yüksek riskli mailler kaydedildi: outputs/high_risk_mails.csv")
