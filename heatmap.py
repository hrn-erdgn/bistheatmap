import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf






# Hisse senedi verilerini içeren bir DataFrame oluşturduğunuzu varsayalım.
# Örnek olarak random verilerle gösterim yapıyorum.
# Normalde BIST 30 hisselerinin tarihsel fiyatlarını bu DataFrame'e yüklemelisiniz.


secim = input("BIST30 heatmapi gelsin istiyorsaniz 1, Hisseleri kendiniz girmek istiyorsaniz 2 girin. [Varsayilan 1] (1/2) : ")


if secim.lower() == "2":
    hisseler = input("Lütfen hisse senedi isimlerini ',' ile ayırarak girin (Örn: GARAN, AKBNK): ").split(',')
    hisseler = [hisse.strip().upper() + ".IS" for hisse in hisseler]

else:
    hisseler = [
    "AKBNK.IS", "ALARK.IS", "ASELS.IS", "ASTOR.IS", "BIMAS.IS",
    "BRSAN.IS", "DOAS.IS" , "EKGYO.IS", "ENKAI.IS", "EREGL.IS",
    "FROTO.IS", "GARAN.IS", "GUBRF.IS", "HEKTS.IS", "ISCTR.IS",
    "KCHOL.IS", "KONTR.IS", "KOZAL.IS", "KRDMD.IS", "OYAKC.IS",
    "PETKM.IS", "PGSUS.IS", "SAHOL.IS", "SASA.IS" , "SISE.IS" ,
    "TCELL.IS", "THYAO.IS", "TOASO.IS", "TUPRS.IS", "YKBNK.IS"
    ]

hisseler.extend(["XU030.IS", "XU100.IS"])




gun = input("Kaç günlük veri almak istiyorsunuz? (Varsayılan: 365 gün): ")


if not gun.isdigit():
    gun = 365
else:
    gun = int(gun)


baslangic = (datetime.today() - timedelta(days=gun)).strftime('%Y-%m-%d')
bugun = datetime.today().strftime('%Y-%m-%d')



data = yf.download(hisseler, start=baslangic, end=bugun)['Adj Close']

# Korelasyon matrisini hesapla
correlation_matrix = data.corr()



ordered_cols = ["XU030.IS", "XU100.IS"] + [col for col in correlation_matrix.columns if col not in ["XU030.IS", "XU100.IS"]]
correlation_matrix = correlation_matrix[ordered_cols].loc[ordered_cols]


correlation_matrix.columns = [col.replace(".IS", "") for col in correlation_matrix.columns]
correlation_matrix.index = [index.replace(".IS", "") for index in correlation_matrix.index]

# Heatmap'i oluştur
plt.figure(figsize=(15, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)

plt.figtext(0.99 ,0.5 , 'Tarih: ' + bugun, ha='center', va='center', fontsize=15, color='gray',  weight='bold', rotation=90)
plt.figtext(0.9 ,0.03 , 'Credits: Harun Erdoğan Github:hrn-erdgn Twitter:harun_erdgn ', ha='center', va='center', fontsize=8, color='gray', alpha=0.7 )
plt.xticks(fontsize=12, weight='bold')
plt.yticks(fontsize=12, weight='bold')
plt.title('BIST Heatmap')
plt.tight_layout()
plt.show()
