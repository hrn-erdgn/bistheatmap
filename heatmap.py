import pandas as pd                        # Veri işleme için pandas kütüphanesini import ediyoruz.
import seaborn as sns                      # Korelasyon heatmap'i oluşturmak için seaborn kütüphanesini import ediyoruz.
import matplotlib.pyplot as plt            # Grafik çizimlerini yapabilmek için matplotlib kütüphanesini import ediyoruz.
from datetime import datetime, timedelta   # Dinamik günleri çekmek için
import yfinance as yf                      # Yahoo Finance API'sini Python'da kullanmak için yfinance kütüphanesini import ediyoruz. Kapanış verileri için






secim = input("BIST30 heatmapi gelsin istiyorsaniz 1, Hisseleri kendiniz girmek istiyorsaniz 2 girin. [Varsayilan 1] (1/2) : ") # Kullanıcıya Seçim Sunuyoruz


if secim.lower() == "2":    # Seçin 2 ise girilen hisseleri parse ediyoruz
    hisseler = input("Lütfen hisse senedi isimlerini ',' ile ayırarak girin (Örn: GARAN, AKBNK): ").split(',') # hisseleri parse ediyoruz
    hisseler = [hisse.strip().upper() + ".IS" for hisse in hisseler] # Girilen hisselerin sonuna .IS ekliyoruz yahoo finance tickerları örn GARAN.IS olarak girmemizi istiyor

else:                    # Varsayılan olarak BIST30 Tickerlarımız
    hisseler = [
    "AKBNK.IS", "ALARK.IS", "ASELS.IS", "ASTOR.IS", "BIMAS.IS",
    "BRSAN.IS", "DOAS.IS" , "EKGYO.IS", "ENKAI.IS", "EREGL.IS",
    "FROTO.IS", "GARAN.IS", "GUBRF.IS", "HEKTS.IS", "ISCTR.IS",
    "KCHOL.IS", "KONTR.IS", "KOZAL.IS", "KRDMD.IS", "OYAKC.IS",
    "PETKM.IS", "PGSUS.IS", "SAHOL.IS", "SASA.IS" , "SISE.IS" ,
    "TCELL.IS", "THYAO.IS", "TOASO.IS", "TUPRS.IS", "YKBNK.IS"
    ]

hisseler.extend(["XU030.IS", "XU100.IS"])        # Korelasyon ısı haritasına bist30 ve bist 100 endekslerinide ekliyoruz.




gun = input("Kaç günlük veri almak istiyorsunuz? (Varsayılan: 365 gün): ") # kaç günlük veri alınsın kullanıcıya soruyoruz


if not gun.isdigit():
    gun = 365         # Varsayılan olarak 365
else:
    gun = int(gun)


baslangic = (datetime.today() - timedelta(days=gun)).strftime('%Y-%m-%d')    # Girilen gün kadar geriye gidiyoruz.
bugun = datetime.today().strftime('%Y-%m-%d') # Bugünü alıyoruz



data = yf.download(hisseler, start=baslangic, end=bugun)['Adj Close']    # Yahoo finance'den hisseler listemizdeki hisselerin kapanış verilerini alıyoruz.

# Korelasyon matrisini hesapla
correlation_matrix = data.corr()



ordered_cols = ["XU030.IS", "XU100.IS"] + [col for col in correlation_matrix.columns if col not in ["XU030.IS", "XU100.IS"]] # Bist30  ve bist100 hisselerini listenin başına alıyoruz
correlation_matrix = correlation_matrix[ordered_cols].loc[ordered_cols] #


correlation_matrix.columns = [col.replace(".IS", "") for col in correlation_matrix.columns]    # Tickerlardan .IS kısmını siliyoruz
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
